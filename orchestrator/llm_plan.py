import os
import re
import textwrap
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from openai import OpenAI  # type: ignore[import]
except Exception:  # pragma: no cover - optional
    OpenAI = None  # type: ignore[assignment]

try:
    import anthropic  # type: ignore[import]
except Exception:  # pragma: no cover - optional
    anthropic = None  # type: ignore[assignment]


_default_root = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(os.getenv("REPO_ROOT", str(_default_root)))

# Where we look for the blueprint files, in order
BP_DIRS = [
    REPO_ROOT / "ProjectBlueprint",
    REPO_ROOT / "docs" / "blueprints",
]

# Exact filenames you told me about
NT_NAME = "Combined_Master_PLAIN_Non_Tech_001.docx"
TD_NAME = "TechnicalDevelopmentPlan.odt"

# WBS IDs like WBS-1.0, WBS-2.3.4, etc.
WBS_RE = re.compile(r"\bWBS-\d+(?:\.\d+)*", re.IGNORECASE)


def _find_file(name: str) -> Path:
    """
    Find a blueprint file by name in BP_DIRS, returning the first that exists.
    If none exist, return the first candidate path anyway (for clear error messages).
    """
    for root in BP_DIRS:
        p = root / name
        if p.exists():
            return p
    return BP_DIRS[0] / name


def _extract_paragraphs_from_xml(root: ET.Element) -> List[str]:
    """
    Generic paragraph extractor from OOXML/ODF XML:
    treat elements with localname 'p' or 'h' as paragraph boundaries.
    """
    paras: List[str] = []
    current: List[str] = []

    def flush():
        if current:
            text = "".join(current).strip()
            if text:
                paras.append(text)
            current.clear()

    for elem in root.iter():
        tag = elem.tag.split("}", 1)[-1]  # localname
        if tag in ("p", "h"):
            flush()
        if elem.text:
            current.append(elem.text)
        if elem.tail:
            current.append(elem.tail)
    flush()
    return [p for p in paras if p.strip()]


def _docx_paragraphs(path: Path) -> List[str]:
    """
    Read a .docx file via zip + word/document.xml and return paragraphs.
    """
    try:
        with zipfile.ZipFile(path, "r") as z:
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
        return _extract_paragraphs_from_xml(tree.getroot())
    except Exception:
        return []


def _odt_paragraphs(path: Path) -> List[str]:
    """
    Read an .odt file via zip + content.xml and return paragraphs.
    """
    try:
        with zipfile.ZipFile(path, "r") as z:
            with z.open("content.xml") as f:
                tree = ET.parse(f)
        return _extract_paragraphs_from_xml(tree.getroot())
    except Exception:
        return []


def _extract_wbs(paragraphs: List[str], source: str, patterns: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Scan paragraphs for WBS IDs like WBS-1.2.3, filter by prefixes in patterns,
    and return a dict: {id: {id, title, source, raw}}.
    """
    items: Dict[str, Dict[str, str]] = {}
    for para in paragraphs:
        for m in WBS_RE.finditer(para):
            wid = m.group(0).upper()
            if not any(wid.startswith(p) for p in patterns):
                continue
            if wid in items:
                continue
            title = re.sub(m.group(0), "", para, flags=re.IGNORECASE).strip(" :-–—.")
            items[wid] = {
                "id": wid,
                "title": title or f"{source} {wid}",
                "source": source,
                "raw": para.strip(),
            }
    return items


def _build_context(patterns: List[str]) -> Tuple[str, Dict[str, Dict[str, str]]]:
    """
    Build a human-readable snapshot of blueprint/WBS context plus a structured WBS dict.
    """
    nt_path = _find_file(NT_NAME)
    td_path = _find_file(TD_NAME)

    notes: List[str] = []
    wbs_items: Dict[str, Dict[str, str]] = {}

    notes.append("Blueprint roots (searched in order):")
    for root in BP_DIRS:
        notes.append(f"  - {root}")

    notes.append(f"NT doc expected at: {nt_path} (exists={nt_path.exists()})")
    notes.append(f"TD doc expected at: {td_path} (exists={td_path.exists()})")

    # Non-technical plan (DOCX)
    if nt_path.exists():
        paras_nt = _docx_paragraphs(nt_path)
        nt_items = _extract_wbs(paras_nt, "NT", patterns)
        wbs_items.update(nt_items)
        if paras_nt:
            intro = "\n".join(paras_nt[:8])
            notes.append("NT intro (first paragraphs, truncated):\n" + intro[:2000])
    else:
        notes.append("NT doc not found; WBS from NT will be empty.")

    # Technical development plan (ODT)
    if td_path.exists():
        paras_td = _odt_paragraphs(td_path)
        td_items = _extract_wbs(paras_td, "TD", patterns)
        for wid, item in td_items.items():
            if wid not in wbs_items:
                wbs_items[wid] = item
        if paras_td:
            intro_td = "\n".join(paras_td[:8])
            notes.append("TD intro (first paragraphs, truncated):\n" + intro_td[:2000])
    else:
        notes.append("TD doc not found; WBS from TD will be empty.")

    # Summarize WBS
    if not wbs_items:
        notes.append("No WBS items matching patterns were auto-extracted from either blueprint.")
    else:
        lines = ["WBS snapshot extracted from blueprints (filtered):"]
        for wid in sorted(wbs_items.keys()):
            item = wbs_items[wid]
            raw = item["raw"]
            snippet = raw if len(raw) <= 220 else raw[:200] + "..."
            lines.append(f"- {wid} ({item['source']}) — {item['title']}")
            lines.append(f"    raw: {snippet}")
        notes.append("\n".join(lines))

    context = "\n\n".join(notes)
    return context, wbs_items


def _system_prompt(patterns: List[str]) -> str:
    pattern_text = ", ".join(patterns)
    return textwrap.dedent(
        f"""
        You are the internal project orchestrator for the RastUp repository.

        You must respect the project's blueprint-first contract:

        • The Non-Technical master plan (NT) lives in `Combined_Master_PLAIN_Non_Tech_001.docx`.
        • The Technical Development Plan (TD) lives in `TechnicalDevelopmentPlan.odt`.
        • Both are large (~400k–500k words total); you only see a small extracted snapshot.

        Your job for this call:
        • Look at the extracted WBS snapshot for IDs starting with {pattern_text}.
        • Plan the next 3–5 days of focused work that advances only those WBS items.
        • Treat the NT plan as authoritative for scope, business logic, UX, and domain intent.
        • Treat the TD plan as authoritative for architecture, technology choices, and constraints.
        • If the TD plan is silent or incomplete on something, fall back to the NT plan's intent.

        Constraints:
        • Assume one primary human engineer, with AI tools and agents assisting.
        • 6–8 hours of focused work per day.
        • Respect dependency ordering implied by WBS IDs (e.g. WBS-1.2 cannot complete before WBS-1.1).
        • Do NOT invent totally new top-level WBS IDs; stay within the ones you see.
        • It is okay to suggest new sub-IDs (e.g. WBS-1.3.1) if they are sensible refinements.

        Output format (Markdown):
        • Optional short section: Gaps / observations (e.g. “TD has no coverage for X, falling back to NT”).
        • Then a section per day: Day 1, Day 2, Day 3, ... (3–5 days).
        • Under each day, 3–6 tasks with:
          – WBS id(s)
          – Short title
          – Owner (e.g. "human", "human+AI", "AI tool only")
          – Expected duration
          – Explicit definition of done.

        If no WBS items could be extracted, clearly say so and recommend concrete next steps
        to bring the blueprints into a state where planning is possible.
        """
    ).strip()


def _call_openai(user_content: str, patterns: List[str]) -> str:
    if OpenAI is None:
        raise RuntimeError("openai library is not installed in this environment.")
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY (or OPENAI_KEY) is not set.")
    client = OpenAI(api_key=api_key)
    model = os.getenv("ORCH_OPENAI_MODEL", "gpt-4.1-mini")
    temperature = float(os.getenv("ORCH_LLM_TEMPERATURE", "0.25"))
    max_tokens = int(os.getenv("ORCH_LLM_MAX_TOKENS", "1400"))

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _system_prompt(patterns)},
            {"role": "user", "content": user_content},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = completion.choices[0].message.content
    return content or ""


def _call_anthropic(user_content: str, patterns: List[str]) -> str:
    if anthropic is None:
        raise RuntimeError("anthropic library is not installed in this environment.")
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY (or ANTHROPIC_KEY) is not set.")
    client = anthropic.Anthropic(api_key=api_key)
    model = os.getenv("ORCH_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    temperature = float(os.getenv("ORCH_LLM_TEMPERATURE", "0.25"))
    max_tokens = int(os.getenv("ORCH_LLM_MAX_TOKENS", "1400"))

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": _system_prompt(patterns)},
            {"role": "user", "content": user_content},
        ],
    )
    chunks: List[str] = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            chunks.append(block.text)
    return "".join(chunks) if chunks else str(message)


def llm_plan_text(user_prompt: str, patterns: List[str] | None = None) -> str:
    """
    Main entry used by the Slack app.

    By default it plans for WBS-1.* and WBS-2.*,
    using WBS IDs auto-extracted from the NT+TD blueprint documents.
    """
    if patterns is None:
        patterns = ["WBS-1.", "WBS-2."]

    goal = user_prompt.strip() or "Plan the next 3–5 days of work for WBS-1.* and WBS-2.* based on the blueprints."
    context, _wbs_items = _build_context(patterns)

    user_content = (
        f"User request:\n{goal}\n\n"
        "Context snapshot (from blueprint files and extracted WBS):\n"
        f"{context}\n\n"
        "Now plan the next 3–5 days as described in the system prompt."
    )

    errors: List[str] = []

    # Try OpenAI first
    try:
        return _call_openai(user_content, patterns)
    except Exception as exc:
        errors.append(f"OpenAI: {exc}")

    # Fallback to Anthropic if configured
    try:
        return _call_anthropic(user_content, patterns)
    except Exception as exc:
        errors.append(f"Anthropic: {exc}")

    raise RuntimeError(" / ".join(errors))

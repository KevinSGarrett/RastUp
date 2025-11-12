# orchestrator/app.py
import json
import os
import re
import shlex
import sys
import subprocess
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ------------------------------------------------------------------------------
# Settings / Config
# ------------------------------------------------------------------------------
try:
    from orchestrator.config import SETTINGS
except Exception:
    class _Fallback:
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "")
        slack_app_token = os.environ.get("SLACK_APP_TOKEN", "")
        slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
        repo_root = os.environ.get("REPO_ROOT", r"C:\RastUp\RastUp")
        weekly_usd_cap = float(os.environ.get("WEEKLY_USD_CAP", "100"))
        soft_alert_pct = int(os.environ.get("SOFT_ALERT_PCT", "80"))
        boost_stop_loss = float(os.environ.get("BOOST_STOP_LOSS", "5"))
    SETTINGS = _Fallback()

from orchestrator.cursor_runner import run_cursor  # existing runner

REPO_ROOT  = Path(getattr(SETTINGS, "repo_root", r"C:\RastUp\RastUp"))
DOCS_DIR   = REPO_ROOT / "docs"
OPS_DIR    = REPO_ROOT / "ops"

LEDGER     = DOCS_DIR / "logs" / "cost-ledger.jsonl"
AGENTS_DIR = DOCS_DIR / "orchestrator" / "from-agents"

FLAGS_DIR  = OPS_DIR / "flags"
SAFE_FLAG  = FLAGS_DIR / "safe-mode.json"
BOOST_FILE = FLAGS_DIR / "boost.json"
BUDGET_FILE= FLAGS_DIR / "budget.json"   # {"weekly_cap":100,"soft_alert_pct":80}

APPROVALS_DIR = OPS_DIR / "approvals"
QUEUE_FILE    = OPS_DIR / "queue.jsonl"
ADMINS_FILE   = OPS_DIR / "admins" / "admins.json"  # ["Uxxxxx"]

DEFAULT_MODEL = os.environ.get("CURSOR_AGENT_MODEL", "gpt-5")
DEBUG = str(os.environ.get("RU_CONFIG_DEBUG", "")).lower() in {"1","true","yes"}

# ------------------------------------------------------------------------------
# Debug helpers
# ------------------------------------------------------------------------------
def _mask(s: Optional[str]) -> str:
    if not s: return ""
    s = str(s).strip()
    return s if len(s) < 12 else f"{s[:6]}…{s[-6:]}"

def _print_config_debug():
    if not DEBUG: return
    env_file = REPO_ROOT / ".env"
    raw = ""
    try:
        raw = env_file.read_text(encoding="utf-8", errors="ignore") if env_file.exists() else ""
    except Exception:
        pass
    file_has_bot = bool(re.search(r"^\s*SLACK_BOT_TOKEN\s*=", raw, re.M))
    file_has_app = bool(re.search(r"^\s*SLACK_APP_TOKEN\s*=", raw, re.M))
    bot = (getattr(SETTINGS, "slack_bot_token", "") or os.environ.get("SLACK_BOT_TOKEN","")).strip()
    app_token = (getattr(SETTINGS, "slack_app_token","") or os.environ.get("SLACK_APP_TOKEN","")).strip()
    print("[config]"
          f" repo_root= {REPO_ROOT}"
          f"  env_file= {env_file}"
          f"  file_has_bot= {file_has_bot}"
          f"  bot_present= {bool(bot)} {_mask(bot) if bot else ''}"
          f"  file_has_app= {file_has_app}"
          f"  app_present= {bool(app_token)} {_mask(app_token) if app_token else ''}")

# ------------------------------------------------------------------------------
# Slack App
# ------------------------------------------------------------------------------
app = App(token=SETTINGS.slack_bot_token, signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
_print_config_debug()

# ------------------------------------------------------------------------------
# Admin allow-list
# ------------------------------------------------------------------------------
def _load_admins() -> Optional[set]:
    p = ADMINS_FILE
    try:
        if p.exists():
            arr = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
            return set(str(x).strip() for x in arr if str(x).strip())
    except Exception:
        pass
    return None  # None = open (no restrictions)

def _is_admin(user_id: str) -> bool:
    s = _load_admins()
    if s is None:
        return True
    return user_id in s

# ------------------------------------------------------------------------------
# Ledger / budget helpers
# ------------------------------------------------------------------------------
def _parse_ts(o) -> Optional[datetime]:
    t = o.get("ts") or o.get("timestamp") or o.get("time")
    if t is None: return None
    try:
        if isinstance(t, (int, float)):
            return datetime.fromtimestamp(float(t), tz=timezone.utc)
        s = str(t).strip().replace("Z", "+00:00")
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except Exception:
        return None

def _ledger_entries() -> List[Dict[str, Any]]:
    if not LEDGER.exists(): return []
    out = []
    with LEDGER.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try: out.append(json.loads(line))
            except Exception: continue
    return out

def _sum_usd_since(days: int) -> float:
    ents = _ledger_entries()
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    have_ts, total = False, 0.0
    for e in ents:
        dt = _parse_ts(e)
        if dt is None: continue
        have_ts = True
        if dt >= cutoff:
            total += float(e.get("usd", 0.0))
    if not have_ts:
        return round(sum(float(e.get("usd",0.0)) for e in ents), 2)
    return round(total, 2)

def _append_ledger(kind: str, usd: float, note: str):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": datetime.now(timezone.utc).isoformat(), "kind": kind, "usd": float(usd), "note": note}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")

def _load_budget_overrides():
    cap = float(getattr(SETTINGS, "weekly_usd_cap", 100.0))
    soft = int(getattr(SETTINGS, "soft_alert_pct", 80))
    try:
        if BUDGET_FILE.exists():
            d = json.loads(BUDGET_FILE.read_text(encoding="utf-8", errors="ignore"))
            cap = float(d.get("weekly_cap", cap))
            soft = int(d.get("soft_alert_pct", soft))
    except Exception:
        pass
    return cap, soft

def _budget_snapshot() -> Dict[str, Any]:
    cap, soft = _load_budget_overrides()
    spent = _sum_usd_since(7)
    pct = 0.0 if cap <= 0 else (spent / cap) * 100.0
    mode = "NORMAL" if pct < soft else ("ECONOMY" if pct <= 100.0 else "THROTTLED")
    return {"cap": cap, "soft": soft, "spent_week": spent, "pct": pct, "mode": mode}

# ------------------------------------------------------------------------------
# SAFE / Boost
# ------------------------------------------------------------------------------
def _safe_mode() -> bool:
    return SAFE_FLAG.exists()

def _set_safe_mode(on: bool) -> None:
    SAFE_FLAG.parent.mkdir(parents=True, exist_ok=True)
    if on:
        SAFE_FLAG.write_text(json.dumps({
            "reason": "manual", "by": "orchestrator",
            "ts": datetime.now(timezone.utc).isoformat()
        }), encoding="utf-8")
    else:
        try: SAFE_FLAG.unlink()
        except FileNotFoundError: pass

def _get_boost() -> float:
    if not BOOST_FILE.exists(): return 0.0
    try:
        data = json.loads(BOOST_FILE.read_text(encoding="utf-8"))
        return float(data.get("remaining", 0.0))
    except Exception:
        return 0.0

def _set_boost(amount: float) -> None:
    BOOST_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOOST_FILE.write_text(json.dumps({
        "remaining": float(amount),
        "ts": datetime.now(timezone.utc).isoformat()
    }), encoding="utf-8")

# ------------------------------------------------------------------------------
# Queue
# ------------------------------------------------------------------------------
def _queue_append(obj: Dict[str, Any]) -> None:
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")

def _queue_read_all() -> List[Dict[str, Any]]:
    if not QUEUE_FILE.exists(): return []
    out=[]
    with QUEUE_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try: out.append(json.loads(line))
            except Exception: continue
    return out

def _queue_clear() -> None:
    try: QUEUE_FILE.unlink()
    except FileNotFoundError: pass

# ------------------------------------------------------------------------------
# Misc
# ------------------------------------------------------------------------------
def _last_log(agent: str) -> Optional[Path]:
    d = AGENTS_DIR / agent
    if not d.exists(): return None
    files = sorted(d.glob("run-*.log"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None

def _help_text() -> str:
    return (
        "Orchestrator commands\n"
        "• ping — quick liveness and SAFE/Boost\n"
        "• status — weekly budget snapshot (7d)\n"
        "• sync — recompute budget snapshot\n"
        "• health — regenerate HEALTH/SUMMARY/AUDIT locally\n"
        "• knowledge audit — quick blueprint/index health\n"
        "• safe on|off — toggle SAFE (OFF requires admin+approval)\n"
        "• boost <amount>|clear — set/clear Boost (requires admin+approval)\n"
        "• budget show|set <cap>|soft <pct> — overrides (admin)\n"
        "• heavy \"Reason\" <usd> — guarded ledger entry (SAFE/Boost/queue)\n"
        "• approvals list|propose|sign — manage two‑key files\n"
        "• squad run [--model m] [--slug pack] [--query q] — run 4 agents sequentially\n"
        "• sections rebuild — rebuild DOCX/ODT indices\n"
        "• tail [AGENT] [--lines N] — recent agent log\n"
        "• run \"Title\" --agent AGENT-1 --model gpt-5 [--slug WBS-x.y] [--query \"...\"]\n"
        "• queue — show queue; drain — execute queued items (SAFE must be OFF)\n"
        "• admin whoami|list — admin checks"
    )

def _parse_run(text: str) -> Tuple[str,str,str,Optional[str],Optional[str]]:
    parts = shlex.split(text or "")
    if not parts: return "Untitled run","AGENT-1",DEFAULT_MODEL,None,None
    if parts[0].lower() == "run": parts = parts[1:]
    title_tokens=[]; i=0
    while i < len(parts) and not parts[i].startswith("--"):
        title_tokens.append(parts[i]); i += 1
    title = " ".join(title_tokens) if title_tokens else "Untitled run"
    agent, model, slug, query = "AGENT-1", DEFAULT_MODEL, None, None
    while i < len(parts):
        tok = parts[i]
        if tok == "--agent" and i+1 < len(parts): agent = parts[i+1]; i += 2; continue
        if tok == "--model" and i+1 < len(parts): model = parts[i+1]; i += 2; continue
        if tok == "--slug"  and i+1 < len(parts): slug  = parts[i+1]; i += 2; continue
        if tok == "--query" and i+1 < len(parts): query = parts[i+1]; i += 2; continue
        i += 1
    return title, agent, model, slug, query

# ------------------------------------------------------------------------------
# Agent launch
# ------------------------------------------------------------------------------
def _launch_agent_run(title: str, agent: str, model: str, channel_id: str, respond,
                      slug: Optional[str]=None, query: Optional[str]=None) -> None:
    snap = _budget_snapshot()

    if _safe_mode() and _get_boost() <= 0.0:
        _queue_append({"type":"run","title":title,"agent":agent,"model":model,
                       "queued_at": datetime.now(timezone.utc).isoformat(),
                       "by":"slack"})
        _say_ephemeral(respond, None, ":inbox_tray: SAFE=ON & no Boost — run **queued**.")
        return

    if snap["cap"] > 0 and snap["spent_week"] >= snap["cap"]:
        _say_ephemeral(respond, None, ":no_entry: Weekly cap reached — raise cap or use Boost.")
        return

    extra = (f"  | slug: `{slug}`" if slug else "") + (f"  | query: `{query}`" if query else "")
    _say_ephemeral(respond, None, f":hourglass_flowing_sand: Starting *{agent}* — {title}\nModel: `{model}`{extra}")

    before = _sum_usd_since(7)

    def _bg():
        try:
            kwargs = dict(agent_name=agent, model=model)
            if slug:  kwargs["pack_slug"] = slug
            if query: kwargs["query"] = query
            try:
                res = run_cursor(str(REPO_ROOT), f"{title}", **kwargs)
            except TypeError:
                res = run_cursor(str(REPO_ROOT), f"{title}", agent_name=agent, model=model)

            log_path = (res.get("attach") or "").replace("\\","/")
            rc = int(res.get("retcode", 1))
            head = ":white_check_mark:" if rc==0 else ":x:"
            msg = f"{head} *{agent}* finished — exit_code={rc}\nAttach: `{log_path}`"

            after = _sum_usd_since(7)
            delta = max(0.0, after - before)
            stop_loss = float(getattr(SETTINGS, "boost_stop_loss", 5.0))
            if delta >= stop_loss and _get_boost() > 0.0:
                _set_boost(0.0)
                msg += f"\n:warning: Boost stop‑loss hit (Δ=${delta:.2f} ≥ ${stop_loss:.2f}); Boost cleared."

            app.client.chat_postMessage(channel=channel_id, text=msg)
        except Exception as e:
            try: _say_ephemeral(respond, None, f":x: *{agent}* failed: `{e}`")
            except Exception: pass

    threading.Thread(target=_bg, daemon=True).start()

# ------------------------------------------------------------------------------
# Multi‑agent squad (autopilot)
# ------------------------------------------------------------------------------
def _squad_agents() -> List[str]:
    return ["AGENT-1", "AGENT-2", "AGENT-3", "AGENT-4"]

def _launch_squad(title: str, model: str, channel_id: str, respond,
                  slug: Optional[str]=None, query: Optional[str]=None) -> None:
    """Run the 4-agent squad sequentially with baton handoff.
    Respects SAFE/Boost/budget. Queues if blocked.
    """
    snap = _budget_snapshot()

    if _safe_mode() and _get_boost() <= 0.0:
        _queue_append({
            "type": "squad",
            "title": title,
            "model": model,
            "slug": slug,
            "query": query,
            "queued_at": datetime.now(timezone.utc).isoformat(),
            "by": "slack",
        })
        _say_ephemeral(respond, None, ":inbox_tray: SAFE=ON & no Boost — squad run queued.")
        return

    if snap["cap"] > 0 and snap["spent_week"] >= snap["cap"]:
        _say_ephemeral(respond, None, ":no_entry: Weekly cap reached — raise cap or use Boost.")
        return

    _say_ephemeral(respond, None, f":hourglass_flowing_sand: Starting squad (4 agents) — {title}\nModel: `{model}`")

    def _bg():
        agents = _squad_agents()
        total_delta = 0.0
        before_all = _sum_usd_since(7)
        for idx, agent in enumerate(agents, start=1):
            try:
                kwargs = dict(agent_name=agent, model=model)
                if slug:  kwargs["pack_slug"] = slug
                if query: kwargs["query"] = query
                try:
                    res = run_cursor(str(REPO_ROOT), f"{title}", **kwargs)
                except TypeError:
                    res = run_cursor(str(REPO_ROOT), f"{title}", agent_name=agent, model=model)

                log_path = (res.get("attach") or "").replace("\\","/")
                rc = int(res.get("retcode", 1))
                head = ":white_check_mark:" if rc==0 else ":x:"
                app.client.chat_postMessage(channel=channel_id,
                    text=f"{head} [{idx}/4] {agent} finished — exit_code={rc}\nAttach: `{log_path}`")

                if rc != 0:
                    app.client.chat_postMessage(channel=channel_id,
                        text=f":stop_sign: Squad stopped after {agent} due to failure.")
                    break

                # Stop-loss vs Boost after each leg
                after_leg = _sum_usd_since(7)
                delta_leg = max(0.0, after_leg - before_all - total_delta)
                total_delta += delta_leg
                stop_loss = float(getattr(SETTINGS, "boost_stop_loss", 5.0))
                if delta_leg >= stop_loss and _get_boost() > 0.0:
                    _set_boost(0.0)
                    app.client.chat_postMessage(channel=channel_id,
                        text=f":warning: Boost stop‑loss hit on {agent} (Δ=${delta_leg:.2f} ≥ ${stop_loss:.2f}); Boost cleared.")
            except Exception as e:
                try:
                    _say_ephemeral(respond, None, f":x: Squad leg failed: `{e}`")
                except Exception:
                    pass
                break

        # Final summary
        try:
            after_all = _sum_usd_since(7)
            spent = max(0.0, after_all - before_all)
            app.client.chat_postMessage(channel=channel_id,
                text=f":checkered_flag: Squad complete — est. Δ=${spent:.2f} in last 7d window")
        except Exception:
            pass

    threading.Thread(target=_bg, daemon=True).start()

# ------------------------------------------------------------------------------
# Interactive approvals (buttons)
# ------------------------------------------------------------------------------
def _approval_blocks(slug: str, status: str, allowed: List[str]) -> List[Dict[str,Any]]:
    return [
        {"type":"section","text":{"type":"mrkdwn","text":f"*{slug}* — status: *{status}* — allowed: `{', '.join(allowed)}`"}},
        {"type":"actions","elements":[
            {"type":"button","text":{"type":"plain_text","text":"Approve"},"style":"primary",
             "action_id":"ru.approvals.approve","value":slug},
            {"type":"button","text":{"type":"plain_text","text":"Revoke"},"style":"danger",
             "action_id":"ru.approvals.revoke","value":slug}
        ]},
        {"type":"divider"}
    ]

@app.action("ru.approvals.approve")
def approve_action(ack, body, respond, logger):
    ack()
    try:
        slug = body["actions"][0]["value"]
        p = APPROVALS_DIR / (slug if slug.endswith(".json") else f"{slug}.json")
        if not p.exists():
            _say_ephemeral(respond, logger, f":warning: approval `{slug}` not found."); return
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        data["status"] = "approved"
        data.setdefault("used", 0)
        p.write_text(json.dumps(data, indent=2), encoding="utf-8")
        _say_ephemeral(respond, logger, f":white_check_mark: `{p.name}` approved.")
    except Exception as e:
        if logger: logger.error(e)
        _say_ephemeral(respond, logger, f":x: approve failed: {e}")

@app.action("ru.approvals.revoke")
def revoke_action(ack, body, respond, logger):
    ack()
    try:
        slug = body["actions"][0]["value"]
        p = APPROVALS_DIR / (slug if slug.endswith(".json") else f"{slug}.json")
        if not p.exists():
            _say_ephemeral(respond, logger, f":warning: approval `{slug}` not found."); return
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        data["status"] = "revoked"
        p.write_text(json.dumps(data, indent=2), encoding="utf-8")
        _say_ephemeral(respond, logger, f":stop_sign: `{p.name}` revoked.")
    except Exception as e:
        if logger: logger.error(e)
        _say_ephemeral(respond, logger, f":x: revoke failed: {e}")

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def _say_ephemeral(respond, logger, text: str):
    try: respond(text=text, response_type="ephemeral")
    except Exception as e:
        if logger: logger.error(f"respond error: {e}")

def _require_admin_or_bail(user_id: str, respond, logger) -> bool:
    if _is_admin(user_id): return True
    _say_ephemeral(respond, logger, ":no_entry: admin privileges required for this action.")
    return False

def _check_any_approval(names: set) -> bool:
    d = APPROVALS_DIR
    if not d.exists(): return False
    for p in d.glob("*.json"):
        try:
            j = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
            if str(j.get("status","")).lower() != "approved":
                continue
            allowed = {str(x).lower() for x in (j.get("allowed") or [])}
            if "all" in allowed or (allowed & {n.lower() for n in names}):
                return True
        except Exception:
            continue
    return False

def _slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+","-", s.strip()).strip("-").lower()
    return s or f"approval-{int(datetime.now().timestamp())}"

# ------------------------------------------------------------------------------
# /orchestrator
# ------------------------------------------------------------------------------
@app.command("/orchestrator")
def orchestrator_cmd(ack, body, respond, logger):
    ack()
    user_id = body.get("user_id")
    channel_id = body.get("channel_id")
    text = (body.get("text") or "").strip()
    t = text.lower()

    # Basics
    if not text or t.startswith("ping"):
        sm = "ON" if _safe_mode() else "OFF"
        _say_ephemeral(respond, logger, f":green_circle: alive — SAFE={sm}, BOOST={_get_boost():.1f}")
        return
    if t.startswith("help"):
        _say_ephemeral(respond, logger, _help_text()); return

    # Status / sync / health
    if t.startswith("status"):
        snap = _budget_snapshot()
        _say_ephemeral(respond, logger,
            "Orchestrator status\n"
            f"• Weekly Budget: ${snap['spent_week']:.2f}/${snap['cap']:.2f} ({snap['pct']:.1f}%) — mode: {snap['mode']}\n"
            f"• SAFE-MODE: {'ON' if _safe_mode() else 'OFF'}\n"
            f"• Active Boost: {_get_boost():.1f}")
        return
    if t.startswith("sync"):
        snap = _budget_snapshot()
        _say_ephemeral(respond, logger,
            f":arrows_counterclockwise: Sync — 7d ${snap['spent_week']:.2f} of ${snap['cap']:.2f} "
            f"({snap['pct']:.1f}%), soft {snap['soft']}% → {snap['mode']}")
        return
    if t.startswith("health"):
        try:
            py = sys.executable
            cmds = []
            for name in ("report_health.py","sync_budget.py","audit_rollup.py"):
                p = REPO_ROOT / "scripts" / "orchestrator" / name
                if p.exists(): cmds.append([py, str(p)])
            for c in cmds:
                subprocess.run(c, cwd=str(REPO_ROOT), check=False, capture_output=True, text=True)
            _say_ephemeral(respond, logger, ":white_check_mark: Health artifacts updated.")
        except Exception as e:
            _say_ephemeral(respond, logger, f":x: health failed: {e}")
        return

    # Knowledge audit
    if t.startswith("knowledge"):
        # `/orchestrator knowledge audit`
        nt = DOCS_DIR / "blueprints" / "Combined_Master_PLAIN_Non_Tech_001.docx"
        td = DOCS_DIR / "blueprints" / "TechnicalDevelopmentPlan.odt"
        sec = DOCS_DIR / "blueprints" / "sections.json"
        have_nt = "yes" if nt.exists() else "no"
        have_td = "yes" if td.exists() else "no"
        have_sec= "yes" if sec.exists() else "no"
        counts = ""
        try:
            if sec.exists():
                j = json.loads(sec.read_text(encoding="utf-8", errors="ignore"))
                cnt_nt = sum(1 for x in j if str(x.get("kind")).upper()=="NT")
                cnt_td = sum(1 for x in j if str(x.get("kind")).upper()=="TD")
                counts = f" — NT:{cnt_nt} TD:{cnt_td}"
        except Exception:
            pass
        _say_ephemeral(respond, logger,
            f"*Knowledge audit*\n"
            f"• NT doc present: {have_nt}\n"
            f"• TD doc present: {have_td}\n"
            f"• sections.json:  {have_sec}{counts}\n"
            f"• OUTLINE.md:     {'yes' if (DOCS_DIR/'OUTLINE.md').exists() else 'no'}\n"
            f"• PROGRESS.md:    {'yes' if (DOCS_DIR/'PROGRESS.md').exists() else 'no'}")
        return

    # Admin / SAFE / Boost / Budget / Heavy
    if t.startswith("admin"):
        if "whoami" in t:
            _say_ephemeral(respond, logger, f"You are `{'ADMIN' if _is_admin(user_id) else 'USER'}` (user_id={user_id}).")
            return
        if "list" in t:
            s = _load_admins()
            _say_ephemeral(respond, logger, f"Admins: {', '.join(sorted(s)) if s else '(open / no admins.json)'}")
            return
        _say_ephemeral(respond, logger, "Usage: `/orchestrator admin whoami|list`")
        return

    if t.startswith("safe"):
        if re.search(r"\bon\b", text, re.I):
            _set_safe_mode(True); _say_ephemeral(respond, logger, ":shield: SAFE-MODE **ON**"); return
        if re.search(r"\boff\b", text, re.I):
            if not _require_admin_or_bail(user_id, respond, logger): return
            if not _check_any_approval({"safe_off","write","all"}):
                _say_ephemeral(respond, logger, ":no_entry: SAFE-OFF requires approval (safe_off|write|all)."); return
            _set_safe_mode(False); _say_ephemeral(respond, logger, ":rocket: SAFE-MODE **OFF** (queue may drain)"); return
        _say_ephemeral(respond, logger, "Usage: `/orchestrator safe on|off`"); return

    if t.startswith("boost"):
        if "clear" in t:
            if not _require_admin_or_bail(user_id, respond, logger): return
            if not _check_any_approval({"boost_clear","write","all"}):
                _say_ephemeral(respond, logger, ":no_entry: Boost clear requires approval (boost_clear|write|all)."); return
            _set_boost(0.0); _say_ephemeral(respond, logger, ":boom: Boost cleared (0.0)"); return
        m = re.search(r"boost\s+([0-9]+(\.[0-9]+)?)", text, re.I)
        if m:
            if not _require_admin_or_bail(user_id, respond, logger): return
            if not _check_any_approval({"boost_set","write","all"}):
                _say_ephemeral(respond, logger, ":no_entry: Boost set requires approval (boost_set|write|all)."); return
            _set_boost(float(m.group(1))); _say_ephemeral(respond, logger, f":boom: Boost set to {float(m.group(1)):.2f}"); return
        _say_ephemeral(respond, logger, "Usage: `/orchestrator boost <amount>` or `boost clear`"); return

    if t.startswith("budget"):
        if not _require_admin_or_bail(user_id, respond, logger): return
        try:
            BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
            d = {}
            if BUDGET_FILE.exists():
                d = json.loads(BUDGET_FILE.read_text(encoding="utf-8", errors="ignore"))
            if "show" in t:
                cap, soft = _load_budget_overrides()
                _say_ephemeral(respond, logger, f"Budget overrides → weekly_cap=${cap:.2f}, soft_alert_pct={soft}%")
                return
            m = re.search(r"\bset\s+([0-9]+(\.[0-9]+)?)", t)
            if m:
                d["weekly_cap"] = float(m.group(1))
                BUDGET_FILE.write_text(json.dumps(d, indent=2), encoding="utf-8")
                _say_ephemeral(respond, logger, f":white_check_mark: weekly_cap set to ${d['weekly_cap']:.2f}")
                return
            m = re.search(r"\bsoft\s+([0-9]{1,3})", t)
            if m:
                d["soft_alert_pct"] = int(m.group(1))
                BUDGET_FILE.write_text(json.dumps(d, indent=2), encoding="utf-8")
                _say_ephemeral(respond, logger, f":white_check_mark: soft_alert_pct set to {d['soft_alert_pct']}%")
                return
            _say_ephemeral(respond, logger, "Usage: `/orchestrator budget show|set <cap>|soft <pct>`")
        except Exception as e:
            _say_ephemeral(respond, logger, f":x: budget error: {e}")
        return

    if t.startswith("heavy"):
        m = re.search(r'heavy\s+"([^"]+)"\s+([0-9]+(\.[0-9]+)?)', text)
        if not m:
            _say_ephemeral(respond, logger, 'Usage: `/orchestrator heavy "Reason" <usd>`'); return
        reason, usd = m.group(1), float(m.group(2))
        if _safe_mode() and _get_boost() < usd:
            _queue_append({"type":"heavy","reason":reason,"usd":usd,
                           "queued_at": datetime.now(timezone.utc).isoformat(),"by":"slack"})
            _say_ephemeral(respond, logger, ":inbox_tray: SAFE=ON & Boost insufficient — heavy **queued**."); return
        _append_ledger("heavy", usd, reason)
        if _safe_mode(): _set_boost(max(0.0, _get_boost()-usd))
        _say_ephemeral(respond, logger, f":moneybag: Logged heavy step ${usd:.2f} — {reason}")
        return

    # Approvals
    if t.startswith("approvals"):
        parts = shlex.split(text)
        if len(parts)==1 or parts[1].lower()=="list":
            if not APPROVALS_DIR.exists():
                _say_ephemeral(respond, logger, "No approvals directory found."); return
            blocks=[]
            for p in sorted(APPROVALS_DIR.glob("*.json")):
                try:
                    d = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
                    status = str(d.get("status","pending"))
                    allowed = [str(x) for x in (d.get("allowed") or [])]
                    blocks.extend(_approval_blocks(p.name, status, allowed))
                except Exception:
                    continue
            if not blocks:
                _say_ephemeral(respond, logger, "Approvals: (none)"); return
            try:
                app.client.chat_postEphemeral(channel=channel_id, user=user_id, blocks=blocks, text="Approvals")
            except Exception:
                _say_ephemeral(respond, logger, "Approvals prepared (failed to render blocks).")
            return

        sub = parts[1].lower()
        if sub == "propose":
            # /orchestrator approvals propose "Allow Boost + write" allowed=write,boost_set status=approved
            if not _require_admin_or_bail(user_id, respond, logger): return
            m = re.search(r'propose\s+"([^"]+)"(.*)$', text, re.I)
            if not m:
                _say_ephemeral(respond, logger, 'Usage: `/orchestrator approvals propose "Title" allowed=a,b [status=pending]`'); return
            title = m.group(1).strip()
            tail  = m.group(2)
            allowed = []
            status  = "pending"
            m1 = re.search(r'allowed\s*=\s*([A-Za-z_,\-]+)', tail, re.I)
            if m1: allowed = [x.strip() for x in m1.group(1).split(",") if x.strip()]
            m2 = re.search(r'status\s*=\s*(approved|pending|revoked)', tail, re.I)
            if m2: status = m2.group(1).lower()
            slug = _slugify(title)
            APPROVALS_DIR.mkdir(parents=True, exist_ok=True)
            data = {"slug": slug, "title": title, "status": status, "allowed": allowed,
                    "ts": datetime.now(timezone.utc).isoformat()}
            p = APPROVALS_DIR / f"{slug}.json"
            p.write_text(json.dumps(data, indent=2), encoding="utf-8")
            _say_ephemeral(respond, logger, f":memo: Proposed `{p.name}` — status: {status}; allowed: {', '.join(allowed) or '(none)'}")
            return

        if sub == "sign":
            # /orchestrator approvals sign <slug> approve|revoke
            if not _require_admin_or_bail(user_id, respond, logger): return
            if len(parts) < 4:
                _say_ephemeral(respond, logger, "Usage: `/orchestrator approvals sign <slug> approve|revoke`"); return
            slug, action = parts[2], parts[3].lower()
            p = APPROVALS_DIR / (slug if slug.endswith(".json") else f"{slug}.json")
            if not p.exists():
                _say_ephemeral(respond, logger, f":warning: `{slug}` not found."); return
            d = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
            d["status"] = "approved" if action=="approve" else "revoked"
            p.write_text(json.dumps(d, indent=2), encoding="utf-8")
            _say_ephemeral(respond, logger, f":white_check_mark: `{p.name}` → {d['status']}")
            return

        _say_ephemeral(respond, logger, "Usage: `/orchestrator approvals list|propose|sign`")
        return

    # Sections
    if t.startswith("sections"):
        if "rebuild" in t:
            try:
                py = sys.executable
                td = REPO_ROOT / "scripts" / "blueprints" / "build_td_windows.py"
                if td.exists(): subprocess.run([py, str(td)], cwd=str(REPO_ROOT), check=False)
                nt = REPO_ROOT / "scripts" / "blueprints" / "build_sections.py"
                if nt.exists(): subprocess.run([py, str(nt)], cwd=str(REPO_ROOT), check=False)
                _say_ephemeral(respond, logger, ":white_check_mark: Sections rebuilt (see docs/blueprints/sections.json).")
            except Exception as e:
                _say_ephemeral(respond, logger, f":x: sections rebuild failed: {e}")
            return
        _say_ephemeral(respond, logger, "Usage: `/orchestrator sections rebuild`")
        return

    # Queue / drain
    if t.startswith("queue"):
        items = _queue_read_all()
        runs = [x for x in items if x.get("type")=="run"]
        heavy= [x for x in items if x.get("type")=="heavy"]
        squads= [x for x in items if x.get("type")=="squad"]
        _say_ephemeral(respond, logger, f":inbox_tray: Queue size: {len(items)} (runs:{len(runs)}, squad:{len(squads)}, heavy:{len(heavy)})")
        return

    if t.startswith("drain"):
        if _safe_mode():
            _say_ephemeral(respond, logger, ":no_entry: Cannot drain while SAFE=ON."); return
        items = _queue_read_all()
        if not items:
            _say_ephemeral(respond, logger, ":inbox_tray: Queue empty."); return
        _queue_clear()
        _say_ephemeral(respond, logger, f":rocket: Draining {len(items)} queued item(s)…")
        for rec in items:
            if rec.get("type")=="run":
                _launch_agent_run(rec.get("title","Untitled run"), rec.get("agent","AGENT-1"),
                                  rec.get("model",DEFAULT_MODEL), channel_id, respond)
            elif rec.get("type")=="heavy":
                _append_ledger("heavy", float(rec.get("usd",0)), rec.get("reason","queued-heavy"))
            elif rec.get("type")=="squad":
                _launch_squad(rec.get("title","Untitled squad"), rec.get("model",DEFAULT_MODEL),
                              channel_id, respond, slug=rec.get("slug"), query=rec.get("query"))
        return

    # Tail
    if t.startswith("tail"):
        parts = shlex.split(text)
        agent = parts[1] if len(parts)>1 and not parts[1].startswith("--") else "AGENT-1"
        lines = 120
        for i, tok in enumerate(parts):
            if tok=="--lines" and i+1 < len(parts):
                try: lines = int(parts[i+1])
                except Exception: pass
        p = _last_log(agent)
        if not p:
            _say_ephemeral(respond, logger, f"No logs found for {agent}"); return
        try:
            content = p.read_text(encoding="utf-8", errors="ignore").splitlines()[-lines:]
            preview = "```\n" + "\n".join(content) + "\n```"
            if len(preview) > 2500:
                app.client.files_upload_v2(channel=channel_id, filename=p.name, title=f"{agent} — {p.name}",
                                           content=p.read_text(encoding="utf-8", errors="ignore"))
                _say_ephemeral(respond, logger, f"*{agent}* latest log: `{p.name}` (uploaded full log).")
            else:
                _say_ephemeral(respond, logger, f"*{agent}* latest log: `{p.name}`\n{preview}")
        except Exception as e:
            _say_ephemeral(respond, logger, f"Error reading log: {e}")
        return

    # Run
    if t.startswith("run"):
        title, agent, model, slug, query = _parse_run(text)
        _launch_agent_run(title, agent, model, channel_id, respond, slug=slug, query=query)
        return

    # Squad (autopilot)
    if t.startswith("squad") or t.startswith("autopilot"):
        # Example: /orchestrator squad run --model gpt-5 --slug wbs-1-3-knowledge --query "..."
        parts = shlex.split(text)
        # Default args
        model = DEFAULT_MODEL
        slug = None
        query = None
        # Parse flags
        for i, tok in enumerate(parts):
            if tok == "--model" and i+1 < len(parts): model = parts[i+1]
            if tok == "--slug"  and i+1 < len(parts): slug  = parts[i+1]
            if tok == "--query" and i+1 < len(parts): query = parts[i+1]
        if any(x in {"run","start"} for x in parts[1:2]):
            _launch_squad("Autopilot Squad", model, channel_id, respond, slug=slug, query=query)
            return
        _say_ephemeral(respond, logger, "Usage: `/orchestrator squad run [--model m] [--slug pack] [--query q]`")
        return

    # Fallback
    _say_ephemeral(respond, logger,
        "Unknown command. Try `help`, `status`, `sync`, `health`, `knowledge audit`, "
        "`safe on|off`, `boost <amt>|clear`, `budget show|set|soft`, `heavy \"Reason\" <usd>`, "
        "`approvals list|propose|sign`, `sections rebuild`, `queue`, `drain`, `tail`, `run`")

# ------------------------------------------------------------------------------
# /agent
# ------------------------------------------------------------------------------
@app.command("/agent")
def agent_cmd(ack, body, respond, logger):
    ack()
    channel_id = body.get("channel_id")
    text = (body.get("text") or "").strip()
    if not text or text.lower().startswith("help"):
        respond(text='Usage: `/agent run "Title" --agent AGENT-1 --model gpt-5 [--slug WBS-x.y] [--query "..."]`',
                response_type="ephemeral")
        return
    if text.lower().startswith("run"):
        title, agent, model, slug, query = _parse_run(text)
        _launch_agent_run(title, agent, model, channel_id, respond, slug=slug, query=query)
        return
    _launch_agent_run(text, "AGENT-1", DEFAULT_MODEL, channel_id, respond)

# ------------------------------------------------------------------------------
# Short command aliases (register these in Slack if desired)
# ------------------------------------------------------------------------------
def _forward(prefix: str, body, ack, respond, logger):
    ack()
    args = (body.get("text") or "").strip()
    channel_id = body.get("channel_id")
    orchestrator_cmd(ack=lambda: None,
                     body={"user_id": body.get("user_id"),
                           "channel_id": channel_id,
                           "text": f"{prefix} {args}".strip()},
                     respond=respond, logger=logger)

@app.command("/safe")
def _alias_safe(ack, body, respond, logger):
    _forward("safe", body, ack, respond, logger)

@app.command("/boost")
def _alias_boost(ack, body, respond, logger):
    _forward("boost", body, ack, respond, logger)

@app.command("/tail")
def _alias_tail(ack, body, respond, logger):
    _forward("tail", body, ack, respond, logger)

@app.command("/ru-safe")
def _alias_ru_safe(ack, body, respond, logger):
    _forward("safe", body, ack, respond, logger)

@app.command("/ru-boost")
def _alias_ru_boost(ack, body, respond, logger):
    _forward("boost", body, ack, respond, logger)

@app.command("/ru-tail")
def _alias_ru_tail(ack, body, respond, logger):
    _forward("tail", body, ack, respond, logger)

@app.command("/ru-agent")
def _alias_ru_agent(ack, body, respond, logger):
    ack()
    agent_cmd(ack=lambda: None, body=body, respond=respond, logger=logger)

@app.command("/squad")
def _alias_squad(ack, body, respond, logger):
    _forward("squad", body, ack, respond, logger)

# ------------------------------------------------------------------------------
# Main (local debug)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    SocketModeHandler(app, SETTINGS.slack_app_token).start()

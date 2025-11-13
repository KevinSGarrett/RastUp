# orchestrator/autopilot.py
from typing import List, Dict
from .llm import call_llm

DEFAULT_PROVIDER = "openai"   # or "anthropic"
DEFAULT_MODEL = "gpt-4.1-mini"  # change as you like


def make_plan(goal: str, steps: int = 8) -> List[Dict[str, str]]:
    system = (
        "You are the orchestrator brain for a software project. "
        "You create high-level task plans. Each step must have:\n"
        "- id: short slug\n"
        "- title: human-readable\n"
        "- agent: one of PLANNER, BUILDER, TESTER, RELEASER\n"
        "- instructions: 1-3 sentences\n"
        "Return as a YAML list."
    )
    user = f"Goal: {goal}\nSteps: {steps}"
    text = call_llm(DEFAULT_PROVIDER, DEFAULT_MODEL, system, user, max_tokens=1200)

    # For now, just return raw text; later we can parse YAML safely.
    return [{"raw_plan": text}]

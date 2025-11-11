import yaml, os
from orchestrator.logger_jsonl import append_cost

class Budget:
    def __init__(self, guardrails="ops/cost/guardrails.yaml", env="dev"):
        with open(guardrails, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)[env]
        self.cap = float(cfg["weekly_usd_cap"])
        self.soft = float(cfg["soft_alert_pct"])
        self.boost_stop = float(cfg["boost_stop_loss_usd"])
        self.week_spend = 0.0
        self.boosts_used = 0

    def record(self, model:str, usd:float, details=None):
        self.week_spend += float(usd)
        append_cost({"model":model,"usd":float(usd),"details":details or {}})

    def percent(self) -> float:
        return (self.week_spend / self.cap * 100) if self.cap else 0.0

    def economy_mode(self) -> bool:
        return self.percent() >= self.soft

    def can_boost(self) -> bool:
        return self.boosts_used < 3

    def start_boost(self, requested_cap=None):
        self.boosts_used += 1
        return requested_cap or self.boost_stop

    # --- demo / testing only ---
    def simulate(self, usd:float):
        """Increase spend for demo/testing; logs to cost ledger."""
        self.record("simulate", usd, {"fn":"simulate"})

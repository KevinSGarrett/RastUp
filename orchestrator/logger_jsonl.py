import json, os, datetime
LOG_PATH = os.path.join("docs","logs","event-stream.jsonl")
COST_PATH = os.path.join("docs","logs","cost-ledger.jsonl")

def append_event(obj: dict):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    obj = {"ts": datetime.datetime.utcnow().isoformat()+"Z", **obj}
    with open(LOG_PATH,"a",encoding="utf-8") as f: f.write(json.dumps(obj,ensure_ascii=False)+"\n")

def append_cost(obj: dict):
    os.makedirs(os.path.dirname(COST_PATH), exist_ok=True)
    obj = {"ts": datetime.datetime.utcnow().isoformat()+"Z", **obj}
    with open(COST_PATH,"a",encoding="utf-8") as f: f.write(json.dumps(obj,ensure_ascii=False)+"\n")

import os, json, re, sys

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("No GITHUB_EVENT_PATH; skipping.")
        return 0

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    pr = event.get("pull_request") or {}
    body = pr.get("body") or ""

    missing = []
    for tag in ("NT:", "TD:", "WBS:"):
        if re.search(rf"^{re.escape(tag)}\s*\S+", body, flags=re.M) is None:
            missing.append(tag)

    if missing:
        print("PR description is missing required trailers:")
        for t in missing:
            print(" -", t)
        print("\nFill the PR template fields NT:/TD:/WBS: with at least one ID each.")
        return 1

    print("PR trailers present.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

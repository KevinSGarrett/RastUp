import sys, json
from pathlib import Path

try:
    import yaml  # installed in workflow
except Exception:
    print("pyyaml required"); sys.exit(2)

def main():
    if len(sys.argv) != 3:
        print("Usage: check_licenses.py <policy.yml> <licenses.json>")
        sys.exit(2)

    policy = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    allowed = set(policy.get("allowed", []))
    denied = set(policy.get("denied", []))

    data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    bad, unknown = [], []

    for pkg in data:
        name = (pkg.get("Name") or "").strip()
        lic  = (pkg.get("License") or "").strip()
        if not lic or lic.upper() == "UNKNOWN":
            unknown.append(name)
        elif allowed and lic not in allowed:
            bad.append((name, lic))

    if bad or unknown:
        print("License check failed.")
        if bad:
            print("Denied or unapproved licenses:")
            for n, l in bad:
                print(f"  - {n}: {l}")
        if unknown:
            print("Unknown licenses (require review):")
            for n in unknown:
                print(f"  - {n}")
        sys.exit(1)

    print("License check passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()

import json, os, re, sys

SPLITS = [
    os.path.join("docs","blueprints","non-tech"),
    os.path.join("docs","blueprints","tech"),
]

def read_front(p):
    out = {}
    with open(p,'r',encoding='utf-8') as f:
        lines = f.read().splitlines()
    if not lines or lines[0].strip() != '---':
        return out
    i = 1
    while i < len(lines) and lines[i].strip() != '---':
        if ':' in lines[i]:
            k,v = lines[i].split(':',1)
            out[k.strip()] = v.strip().strip('\"')
        i += 1
    return out

def main():
    problems = []
    ids = set()
    id_to_path = {}

    # 1) Collect IDs from split files and verify anchors exist
    for folder in SPLITS:
        if not os.path.isdir(folder):
            continue
        for fn in os.listdir(folder):
            if not fn.lower().endswith('.md'):
                continue
            if fn.lower().endswith('all.md'):   # <-- skip pre-split aggregates
                continue
            p = os.path.join(folder, fn)
            fm = read_front(p)
            _id = fm.get('id')
            if not _id:
                problems.append(f"Missing id in front-matter: {p}")
                continue
            if _id in ids:
                problems.append(f"Duplicate id: {_id} at {p} and {id_to_path[_id]}")
            ids.add(_id)
            id_to_path[_id] = p
            with open(p,'r',encoding='utf-8') as f:
                txt = f.read()
            if f'<a id=\"{_id}\">' not in txt.replace('\\"','\"'):
                problems.append(f"Anchor <a id=\"{_id}\"></a> missing in {p}")

    # 2) id_map.json must contain all ids (flat schema)
    if not os.path.exists('id_map.json'):
        problems.append("id_map.json missing")
    else:
        try:
            with open('id_map.json','r',encoding='utf-8') as f:
                id_map = json.load(f)
            mapped_ids = { v.get('id') for v in id_map.values() if isinstance(v, dict) and v.get('id') }
            missing_in_map = sorted(i for i in ids if i not in mapped_ids)
            if missing_in_map:
                problems.append("IDs missing from id_map.json: " + ", ".join(missing_in_map[:50]) + (" ..." if len(missing_in_map)>50 else ""))
        except Exception as e:
            problems.append(f"id_map.json unreadable: {e}")

    # 3) Index files exist and paths/anchors make sense
    req = [
        os.path.join("docs","blueprints","nt-index.json"),
        os.path.join("docs","blueprints","td-index.json"),
        os.path.join("docs","blueprints","toc-cache.json"),
    ]
    for r in req:
        if not os.path.exists(r):
            problems.append(f"Missing index: {r}")

    if os.path.exists(req[0]):
        with open(req[0],'r',encoding='utf-8') as f: nti = json.load(f)
        for _id, meta in nti.items():
            p = meta.get('path')
            if p and not os.path.exists(p):
                problems.append(f"[NT] path not found for {_id}: {p}")
            if meta.get('anchor') != _id:
                problems.append(f"[NT] anchor mismatch for {_id}: {meta.get('anchor')}")

    if os.path.exists(req[1]):
        with open(req[1],'r',encoding='utf-8') as f: tdi = json.load(f)
        for _id, meta in tdi.items():
            p = meta.get('path')
            if p and not os.path.exists(p):
                problems.append(f"[TD] path not found for {_id}: {p}")
            if meta.get('anchor') != _id:
                problems.append(f"[TD] anchor mismatch for {_id}: {meta.get('anchor')}")

    # 4) Report
    os.makedirs(os.path.join("docs","reports"), exist_ok=True)
    with open(os.path.join("docs","reports","check_report.txt"),'w',encoding='utf-8') as f:
        f.write("OK" if not problems else "\n".join(problems))

    if problems:
        print("::error ::Blueprint checks failed. See docs/reports/check_report.txt")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    else:
        print("[check_blueprints] OK")

if __name__ == '__main__':
    main()

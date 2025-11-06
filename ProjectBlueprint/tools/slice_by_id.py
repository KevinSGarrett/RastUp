import json, sys

idx_path, md_path, sec_id = sys.argv[1], sys.argv[2], sys.argv[3]
with open(idx_path,'r',encoding='utf-8') as f: idx=json.load(f)
meta = idx.get(sec_id)
assert meta, f"ID not found: {sec_id}"
assert meta['path'].replace('\\\\','/') == md_path.replace('\\\\','/'), "ID/path mismatch"
start, end = int(meta['start_line']), int(meta['end_line'])
with open(md_path,'r',encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < start: continue
        if i >= end: break
        sys.stdout.write(line)

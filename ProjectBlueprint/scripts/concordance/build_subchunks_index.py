from __future__ import annotations
import json, os, math

NT_LINE = os.path.join('docs','blueprints','nt-line-index.json')
OUT_SUB = os.path.join('docs','blueprints','nt-sub-index.json')

# Tunables
TARGET_LINES = 180      # ~180 lines per sub-chunk (adjust as you like)
MIN_LINES    = 100      # don’t make tiny fragments

def main():
    with open(NT_LINE,'r',encoding='utf-8') as f:
        idx = json.load(f)

    sub = {}
    for sec_id, meta in idx.items():
        # only split H2s (no dot)
        if '.' in sec_id: 
            continue
        start = int(meta['start_line'])
        end   = int(meta['end_line'])
        total = max(0, end - start)
        if total <= 0:
            continue

        # number of chunks
        if total <= TARGET_LINES + MIN_LINES:
            # single chunk (still give it .1 so you can cite NT-3.1)
            sid = f"{sec_id}.1"
            sub[sid] = {"title": f"{sec_id} (part 1)",
                        "path": meta["path"],
                        "anchor": sid,
                        "parent": sec_id,
                        "start_line": start,
                        "end_line": end}
            continue

        chunks = max(2, math.ceil(total / TARGET_LINES))
        # even spread
        size = max(MIN_LINES, total // chunks)
        cur = start
        for i in range(1, chunks+1):
            nxt = start + round(i * total / chunks)
            # safety
            if nxt <= cur: nxt = cur + MIN_LINES
            if nxt > end:  nxt = end
            sid = f"{sec_id}.{i}"
            sub[sid] = {"title": f"{sec_id} (part {i})",
                        "path": meta["path"],
                        "anchor": sid,
                        "parent": sec_id,
                        "start_line": cur,
                        "end_line": nxt}
            cur = nxt
            if cur >= end: break

    # persist
    with open(OUT_SUB,'w',encoding='utf-8') as f:
        json.dump(sub, f, indent=2, ensure_ascii=False)
    print(f"[build_subchunks] wrote {OUT_SUB} with {len(sub)} sub-IDs")

if __name__ == '__main__':
    main()

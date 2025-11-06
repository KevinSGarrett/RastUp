from __future__ import annotations
import re, sys

H2_RE   = re.compile(r'^\s*(SubSection|Section)\s+(\d+(?:\.\d+)*)\b(.*)$')
H3_NUM  = re.compile(r'^\s*\d+\)\s+\S')       # 1) Title
H3_LET  = re.compile(r'^\s*[A-Z]\)\s+\S')     # A) Title  (optional)

def promote(src: str, dst: str) -> int:
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    out = []
    changed = 0
    in_code = False
    have_h2 = True

    for line in lines:
        # Track fenced code blocks (`), don't touch inside
        if line.strip().startswith("`"):
            in_code = not in_code
            out.append(line)
            continue

        # Already a heading or an explicit anchor? leave as-is
        if line.lstrip().startswith("#") or line.lstrip().startswith('<a id="'):
            out.append(line); continue

        if not in_code:
            m2 = H2_RE.match(line)
            if m2:
                tail = (m2.group(3) or '').strip()
                space = (' ' + tail) if tail else ''
                out.append(f"## {m2.group(1)} {m2.group(2)}{space}")
                have_h2 = True
                changed += 1
                continue

            # Promote numeric/letter bullets as H3 only if we've seen an H2
            if have_h2 and (H3_NUM.match(line) or H3_LET.match(line)):
                out.append(f"### {line.strip()}")
                changed += 1
                continue

        out.append(line)

    with open(dst, 'w', encoding='utf-8', newline='\n') as f:
        f.write("\n".join(out) + "\n")
    print(f"[promote_headings] promoted={changed}")
    return changed

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python promote_headings.py <in.md> <out.md>")
        sys.exit(2)
    promote(sys.argv[1], sys.argv[2])



import re

with open(r"G:\マイドライブ\antigravity\IDM\20261006\scripts\generate_paper_html.py", "r", encoding="utf-8") as f:
    code = f.read()

matches = re.findall(r"\$([^\$]+)\$", code)
print(f"Total $...$ in generate_paper_html.py: {len(matches)}")
for m in matches[:15]:
    print(repr(m))

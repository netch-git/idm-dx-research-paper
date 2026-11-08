import re

with open(r"G:\マイドライブ\antigravity\IDM\20261004\final_paper.md", "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r"\$([^\$]+)\$", text)
print(f"Total inline math matches: {len(matches)}")
unique_matches = sorted(list(set(matches)))
for m in unique_matches[:50]:
    print(repr(m))

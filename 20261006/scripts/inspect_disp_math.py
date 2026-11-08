import re

with open(r"G:\マイドライブ\antigravity\IDM\20261004\final_paper.md", "r", encoding="utf-8") as f:
    text = f.read()

disp = re.findall(r"\$\$([^\$]+)\$\$", text)
print(f"Total display matches: {len(disp)}")
for d in disp:
    print("--- DISPLAY ---")
    print(d.strip())

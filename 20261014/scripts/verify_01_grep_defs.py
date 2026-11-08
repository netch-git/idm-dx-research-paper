import sys, re, glob
sys.stdout.reconfigure(encoding="utf-8")
pat = re.compile(r"(read_parquet|read_csv|read_excel|KMeans|smf\.|sm\.Logit|sm\.OLS|anova_lm|\['ownership|\['friction|\['distributive|\['procedural|\['pmo|\['tech|\['own|\['dj|\['pj|\['fr|ownership\w* *=|friction\w* *=|distrib\w* *=|proced\w* *=|pmo\w* *=|tech\w* *=|fillna|dropna|formula)")
for f in sorted(glob.glob(r"G:\マイドライブ\antigravity\IDM\20261008\scripts\0[2-8]_*.py")):
    print("=====", f.split("\\")[-1])
    for i, line in enumerate(open(f, encoding="utf-8"), 1):
        s = line.strip()
        if pat.search(s) and not s.startswith(("print", "#", "md", "html", "f\"", "'", "\"")) and "<" not in s:
            print(f"{i}: {s[:220]}")

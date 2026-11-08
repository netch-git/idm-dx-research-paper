"""00_inspect_columns.py - 変数定義確定のための列・値の棚卸し（解析前の監査用）"""
import sys, os
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
CANDIDATES = [r"G:\マイドライブ\antigravity\IDM\data-cross.xlsx", r"G:\マイドライブ\IDM\data-cross.xlsx"]
path = next(p for p in CANDIDATES if os.path.exists(p))
df = pd.read_excel(path)
out = [f"source: {path}", f"shape: {df.shape}"]

out.append("\n== 終了判定 ==")
out.append(df["終了判定"].value_counts(dropna=False).to_string())

out.append("\n== first 40 column names ==")
out.extend([repr(c) for c in df.columns[:40]])

for key in ["SC2.", "SC7-2."]:
    matches = [c for c in df.columns if key in str(c)]
    out.append(f"\n== columns containing {key}: {len(matches)} ==")
    out.extend([repr(m) for m in matches])
    if not matches:
        continue
    col = matches[0]
    out.append(df[col].value_counts(dropna=False).to_string())
    out.append("-- 本調査終了のみ --")
    out.append(df.loc[df["終了判定"] == "本調査終了", col].value_counts(dropna=False).to_string())

for pre in ["SC15.", "SC18.", "SC20."]:
    cols = [c for c in df.columns if str(c).startswith(pre)]
    if not cols:
        out.append(f"\n== {pre}: none ==")
        continue
    out.append(f"\n== {pre} ({len(cols)} items) ==")
    for c in cols:
        nn_all = df[c].notna().sum()
        nn_main = df.loc[df["終了判定"] == "本調査終了", c].notna().sum()
        out.append(f"{c} | non-null all={nn_all} main={nn_main}")
    out.append("values: " + str(sorted(df[cols[0]].dropna().unique().tolist())))

# Other DX-attitude-like Likert blocks
out.append("\n== all column prefixes ==")
prefixes = sorted({c.split(".")[0] for c in df.columns})
out.append(", ".join(prefixes))

with open(os.path.join(os.path.dirname(__file__), "..", "reports", "00_column_inventory.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n".join(out))

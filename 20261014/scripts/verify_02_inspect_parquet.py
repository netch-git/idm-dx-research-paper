import sys, os, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding="utf-8")
A = r"G:\マイドライブ\antigravity\IDM\20261008\artifacts"
pq = pd.read_parquet(os.path.join(A, "analysis_data_n2035_final.parquet"))
print("parquet", pq.shape)
print(list(pq.columns))
for c in ["ownership_promotion","friction_prevention","procedural_justice","distributive_justice","outcome_q4_score","continuation_q6_score","age","is_large_firm","tier_a"]:
    if c in pq: print(c, pq[c].describe().round(3).to_dict() if pq[c].dtype!=object and str(pq[c].dtype)!="category" else pq[c].value_counts().to_dict())
print(pd.crosstab(pq["is_large_firm"], pq["tier_a"]))
csv = os.path.join(A, "analysis_dataset_n2035.csv")
if os.path.exists(csv):
    d = pd.read_csv(csv, low_memory=False, nrows=5)
    print("analysis_dataset_n2035.csv cols:", len(d.columns))
    for c in d.columns:
        print("  ", repr(c)[:120], "|", d[c].tolist()[:3])
raw_orig = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"
print("orig raw exists:", os.path.exists(raw_orig))
print(os.listdir(r"G:\マイドライブ\antigravity\IDM\data"))

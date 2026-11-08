# -*- coding: utf-8 -*-
"""原稿数値の出所特定: parquet 変数で原稿値が再現されるか / 生データでどの項目構成なら再現されるか"""
import sys, itertools, numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
from scipy import stats
sys.stdout.reconfigure(encoding="utf-8")
pq = pd.read_parquet(r"G:\マイドライブ\antigravity\IDM\20261008\artifacts\analysis_data_n2035_final.parquet")
pq["size"] = pq.is_large_firm.map({1: "L", 0: "S"}); pq["tier"] = pq.tier_a.astype(str)

def h1(d, y):
    a = sm.stats.anova_lm(smf.ols(f"{y} ~ C(size)*C(tier)", data=d).fit(), typ=2)
    cm = d.groupby(["size", "tier"])[y].mean().round(3).to_dict()
    return round(a.loc["C(size):C(tier)", "F"], 3), round(a.loc["C(size):C(tier)", "PR(>F)"], 4), cm

print("parquet ownership_promotion:", pq.ownership_promotion.mean().round(3), pq.ownership_promotion.std().round(3), h1(pq, "ownership_promotion"))
print("parquet friction:", pq.friction_prevention.mean().round(3), pq.friction_prevention.std().round(3))
print("r(own,fr) parquet:", stats.pearsonr(pq.ownership_promotion, pq.friction_prevention))
# parquet SC18 1-5 (6-x)
pq["own15"] = (6 - pq[[f"sc18_{i}" for i in range(1, 6)]]).mean(axis=1)
print("parquet SC18-1..5:", pq.own15.mean().round(3), pq.own15.std().round(3), h1(pq, "own15"))
for k in ["procedural_justice", "distributive_justice", "q9_sat_1"]:
    print(k, pq[k].mean().round(3), pq[k].std().round(3))
pq["pmo8"] = pq[[f"q9_sat_{i}" for i in range(2, 10)]].mean(axis=1)
print("parquet pmo8", pq.pmo8.mean().round(3), pq.pmo8.std().round(3))
print("parquet gap means:", [round(pq[f"gap_cap_{i}"].mean(), 3) for i in range(1, 10)])
print("parquet value sets q8_2:", pq.q8_2.value_counts().to_dict(), " sc15_5:", pq.sc15_5.value_counts().to_dict(), " sc9_3:", pq.sc9_3.value_counts().to_dict())
print("parquet tenure_code:", pq.tenure_code.value_counts().to_dict())
print("SC18-8 cells parquet:", (6 - pq.sc18_8).groupby([pq["size"], pq["tier"]]).mean().round(3).to_dict())

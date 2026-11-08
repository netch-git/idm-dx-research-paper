# -*- coding: utf-8 -*-
"""
20261014 検算 v2: 原稿値 / 既存parquet再現 / 生データ正規コーディング（定義A=原稿記載, 定義B=既存パイプラインの項目構成）を比較
"""
import sys, os, re, json
import numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"G:\マイドライブ\antigravity\IDM"
RAW = os.path.join(ROOT, "data", "data[企業規模-職制カラム追加].xlsx")
RAW_ORIG = os.path.join(ROOT, "data", "ローデータ（ICT活用の調査）1125.xlsx")
PARQ = os.path.join(ROOT, "20261008", "artifacts", "analysis_data_n2035_final.parquet")
OUT = os.path.join(ROOT, "20261014", "artifacts", "verify_v2_results.json")


def col(df, prefix, item=None):
    for c in df.columns:
        cs = c.strip()
        if cs.startswith(prefix) and (item is None or f":{item}." in cs):
            return c
    raise KeyError(prefix, item)


def likert(v):
    if pd.isna(v): return np.nan
    s = str(v).strip()
    if s.startswith("非常に"): return 5
    if s.startswith("やや") or s.startswith("ある程度"): return 4
    if s.startswith("わからない"): return 3
    if s.startswith("あまり"): return 2
    if s.startswith("まったく") or s.startswith("全く"): return 1
    return np.nan


def num010(v):
    if pd.isna(v): return np.nan
    if isinstance(v, (int, float, np.integer, np.floating)): return float(v)
    m = re.match(r"^\s*(\d+)", str(v)); return float(m.group(1)) if m else np.nan


def alpha(X):
    X = np.asarray(X, float); k = X.shape[1]
    return k / (k - 1) * (1 - X.var(axis=0, ddof=1).sum() / X.sum(axis=1).var(ddof=1))


def cohen_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / sp


# ======================================================== 生データ構築
raw = pd.read_excel(RAW, sheet_name=0)
df = raw[raw["終了判定"] == "本調査終了"].copy().reset_index(drop=True)
orig = pd.read_excel(RAW_ORIG, sheet_name="data").set_index("K_ID")
df["age"] = pd.to_numeric(df["K_ID"].map(orig["AGE"]), errors="coerce")
df["q4_orig_code"] = pd.to_numeric(df["K_ID"].map(orig["Q4"]), errors="coerce")
q6o = [c for c in orig.columns if str(c).upper() == "Q6"]
df["q6_orig_code"] = pd.to_numeric(df["K_ID"].map(orig[q6o[0]]), errors="coerce") if q6o else np.nan
df["size"] = np.where(df[col(df, "SC2-2")] == "大企業", "Large", "SMO")  # 既存処理に合わせ「わからない」1名はSMO
df["tier"] = df["SC7-2.職制グループ"].map({"1.経営層": "Exec", "2.部課長クラス": "Mid", "3.一般社員": "Gen"})
df["large"] = (df["size"] == "Large").astype(int)
df["mid"] = (df["tier"] == "Mid").astype(int)
df["gen"] = (df["tier"] == "Gen").astype(int)
df["female"] = (df["性別"] == "女性").astype(int)
for i in range(1, 10):
    for p, nm in [("SC18", "sc18"), ("SC15", "sc15"), ("Q8", "q8"), ("Q9", "q9")]:
        df[f"{nm}_{i}"] = df[col(df, p, i)].map(likert)
for i in range(1, 11):
    df[f"sc9_{i}"] = df[col(df, "SC9", i)].map(likert)
df["q4_given"] = df[col(df, "Q4")].map(num010)
df["q6"] = df[col(df, "Q6")].map(num010)
df["q4"] = df["q4_orig_code"] - 1  # 原データは 1..11 = 0..10点
chk = {
    "q4_given_equals_orig_minus1_on_nonmissing": bool((df.dropna(subset=["q4_given"]).eval("q4_given == q4_orig_code - 1")).all()),
    "q4_missing_given": int(df.q4_given.isna().sum()),
    "q4_missing_given_true_scores": df.loc[df.q4_given.isna(), "q4"].value_counts().to_dict(),
    "q6_given_equals_orig_minus1": bool((df["q6"] == df["q6_orig_code"] - 1).all()) if q6o else None,
    "age_M_SD": [df.age.mean(), df.age.std()],
    "size_unknown_n": int((df[col(df, "SC2-2")] == "わからない").sum()),
}

R = {"checks": chk}


def run_all(d, own, fr, dj, pj, q4, tag, dj_is_low=False):
    """d: DataFrame, own/fr/dj/pj/q4: column names"""
    out = {}
    # 基本
    out["own_M_SD"] = [d[own].mean(), d[own].std()]
    out["fr_M_SD"] = [d[fr].mean(), d[fr].std()]
    r_ = stats.pearsonr(d[own], d[fr]); out["r_own_fr"] = [r_[0], r_[1]]
    # H1
    a2 = sm.stats.anova_lm(smf.ols(f"{own} ~ C(size)*C(tier)", data=d).fit(), typ=2)
    pes = lambda k: a2.loc[k, "sum_sq"] / (a2.loc[k, "sum_sq"] + a2.loc["Residual", "sum_sq"])
    out["H1_size"] = [a2.loc["C(size)", "F"], a2.loc["C(size)", "PR(>F)"], pes("C(size)")]
    out["H1_tier"] = [a2.loc["C(tier)", "F"], a2.loc["C(tier)", "PR(>F)"], pes("C(tier)")]
    out["H1_int"] = [a2.loc["C(size):C(tier)", "F"], a2.loc["C(size):C(tier)", "PR(>F)"], pes("C(size):C(tier)")]
    out["H1_cells"] = {f"{a}_{b}": [v["count"], v["mean"], v["std"]] for (a, b), v in d.groupby(["size", "tier"])[own].agg(["count", "mean", "std"]).iterrows()}
    for t in ["Mid", "Gen"]:
        L = d[(d.tier == t) & (d["size"] == "Large")][own]; S = d[(d.tier == t) & (d["size"] == "SMO")][own]
        tt = stats.ttest_ind(L, S)
        out[f"H1_simple_{t}"] = [L.mean() - S.mean(), tt.statistic, tt.pvalue, cohen_d(L, S)]
    # H2
    Z = StandardScaler().fit_transform(d[[own, fr]])
    lab = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(Z)
    prof = d.assign(cl=lab).groupby("cl")[[own, fr]].mean()
    alien = prof[own].idxmin()
    al = (lab == alien).astype(int)
    out["H2_clusters"] = [[int((lab == c).sum()), prof.loc[c, own], prof.loc[c, fr]] for c in prof.index]
    out["H2_alien_n_pct"] = [int(al.sum()), al.mean() * 100]
    ctrl = ["age", "female", "large", "mid", "gen"]
    X1 = sm.add_constant(d[ctrl].astype(float)); l1 = sm.Logit(al, X1).fit(disp=0)
    X2 = sm.add_constant(d[ctrl + [dj]].astype(float)); l2 = sm.Logit(al, X2).fit(disp=0)
    X3 = sm.add_constant(d[ctrl + [dj, pj]].astype(float)); l3 = sm.Logit(al, X3).fit(disp=0)
    ci = np.exp(l2.conf_int().loc[dj])
    out["H2_m1"] = [l1.prsquared, l1.aic]
    out["H2_m2"] = [l2.prsquared, l2.aic, l2.params[dj], l2.bse[dj], np.exp(l2.params[dj]), ci[0], ci[1], l2.pvalues[dj],
                    np.exp(l2.params["mid"]), l2.pvalues["mid"], np.exp(l2.params["gen"]), l2.pvalues["gen"]]
    out["H2_m3_mid"] = [np.exp(l3.params["mid"]), l3.pvalues["mid"]]
    # H3
    d3 = d.copy()
    d3["fr_c"] = d3[fr] - d3[fr].mean(); d3["pj_c"] = d3[pj] - d3[pj].mean(); d3["fp"] = d3.fr_c * d3.pj_c
    f0 = f"{own} ~ age + female + large + mid + gen + fr_c + pj_c"
    m0 = smf.ols(f0, data=d3).fit(); m1 = smf.ols(f0 + " + fp", data=d3).fit()
    sy = d3[own].std()
    out["H3"] = {"R2": m1.rsquared, "adjR2": m1.rsquared_adj, "dR2": m1.rsquared - m0.rsquared,
                 "pj": [m1.params.pj_c, m1.params.pj_c * d3.pj_c.std() / sy, m1.tvalues.pj_c, m1.pvalues.pj_c],
                 "fr": [m1.params.fr_c, m1.params.fr_c * d3.fr_c.std() / sy, m1.tvalues.fr_c, m1.pvalues.fr_c],
                 "int": [m1.params.fp, m1.params.fp * d3.fp.std() / sy, m1.tvalues.fp, m1.pvalues.fp]}
    V = m1.cov_params(); s = d3.pj_c.std(); ss = {}
    for k, w in [("-1SD", -s), ("Mean", 0), ("+1SD", s)]:
        b = m1.params.fr_c + w * m1.params.fp
        se = np.sqrt(V.loc["fr_c", "fr_c"] + w * w * V.loc["fp", "fp"] + 2 * w * V.loc["fr_c", "fp"])
        ss[k] = [b, se, b / se, 2 * stats.t.sf(abs(b / se), m1.df_resid)]
    out["H3_slopes"] = ss
    # H4 regression
    d4 = d.dropna(subset=[q4])
    m4 = smf.ols(f"{q4} ~ age + female + large + mid + gen + tech + pmo", data=d4).fit()
    sq = d4[q4].std()
    out["H4_reg"] = {"n": len(d4), "R2": m4.rsquared, "adjR2": m4.rsquared_adj, "F": m4.fvalue, "df": [m4.df_model, m4.df_resid],
                     "tech": [m4.params.tech, m4.params.tech * d4.tech.std() / sq, m4.tvalues.tech, m4.pvalues.tech],
                     "pmo": [m4.params.pmo, m4.params.pmo * d4.pmo.std() / sq, m4.tvalues.pmo, m4.pvalues.pmo]}
    # H5
    dl = d[q6c] - d[q4]; tt = stats.ttest_rel(d[q6c], d[q4])
    out["H5"] = {"q6": [d[q6c].mean(), d[q6c].std()], "q4": [d[q4].mean(), d[q4].std()], "delta": [dl.mean(), dl.std()],
                 "t": tt.statistic, "p": tt.pvalue, "dz": dl.mean() / dl.std(), "pos": [int((dl > 0).sum()), (dl > 0).mean() * 100]}
    dd = d.assign(dl=dl)
    out["H5_cells"] = {f"{a}_{b}": [v["count"], v["mean"], v["std"], v["pos"]] for (a, b), v in
                       dd.groupby(["size", "tier"])["dl"].agg(count="count", mean="mean", std="std", pos=lambda x: (x > 0).mean() * 100).iterrows()}
    sm_ = dd[(dd["size"] == "SMO") & (dd.tier == "Mid")].dl; lm_ = dd[(dd["size"] == "Large") & (dd.tier == "Mid")].dl
    sg_ = dd[(dd["size"] == "SMO") & (dd.tier == "Gen")].dl
    out["H5_SMOmid_vs_Lmid"] = [sm_.mean() - lm_.mean(), *stats.ttest_ind(sm_, lm_), cohen_d(sm_, lm_)]
    out["H5_SMOmid_vs_SMOgen"] = [sm_.mean() - sg_.mean(), *stats.ttest_ind(sm_, sg_), cohen_d(sm_, sg_)]
    # 感度分析
    out["S_HC3"] = sm.stats.anova_lm(smf.ols(f"{own} ~ C(size)*C(tier)", data=d).fit(), typ=2, robust="hc3").loc["C(size):C(tier)", ["F", "PR(>F)"]].tolist()
    out["S_ANCOVA_age_sex"] = sm.stats.anova_lm(smf.ols(f"{own} ~ age + female + C(size)*C(tier)", data=d).fit(), typ=2).loc["C(size):C(tier)", ["F", "PR(>F)"]].tolist()
    return out


q6c = "q6"
# ---- 共通の能力指標（Q9 は既存処理でも正しく符号化されていることを確認済み）
df["tech"] = df.q9_1
df["pmo"] = df[[f"q9_{i}" for i in range(2, 10)]].mean(axis=1)

# 定義A: 原稿記載
df["A_own"] = df[[f"sc18_{i}" for i in range(1, 6)]].mean(axis=1)
df["A_fr"] = df[["sc15_1", "sc15_2", "sc15_4", "sc15_5", "sc15_6"]].mean(axis=1)
df["A_djlow"] = 6 - df[["sc18_1", "sc18_4"]].mean(axis=1)
df["A_pj"] = df[["sc18_8", "sc18_9"]].mean(axis=1)
# 定義B: 既存パイプラインの項目構成（正しい符号化）
df["B_own"] = df[["sc18_1", "sc18_2", "sc18_3", "sc18_6", "sc18_7"]].mean(axis=1)
df["B_fr"] = df[[f"sc15_{i}" for i in range(1, 10)]].mean(axis=1)
df["B_dj"] = ((6 - df.sc9_3) + df[[f"sc18_{i}" for i in range(1, 6)]].mean(axis=1)) / 2
df["B_pj"] = df[["sc18_7", "sc18_8", "sc18_9", "sc9_10"]].mean(axis=1)

R["alpha"] = {
    "A_own(SC18-1..5)": alpha(df[[f"sc18_{i}" for i in range(1, 6)]]),
    "B_own(SC18-1,2,3,6,7)": alpha(df[["sc18_1", "sc18_2", "sc18_3", "sc18_6", "sc18_7"]]),
    "A_fr(SC15-1,2,4,5,6)": alpha(df[["sc15_1", "sc15_2", "sc15_4", "sc15_5", "sc15_6"]]),
    "B_fr(SC15-1..9)": alpha(df[[f"sc15_{i}" for i in range(1, 10)]]),
    "PMO(Q9-2..9)": alpha(df[[f"q9_{i}" for i in range(2, 10)]]),
}
R["tech_M_SD"] = [df.tech.mean(), df.tech.std()]
R["pmo_M_SD"] = [df.pmo.mean(), df.pmo.std()]
gaps = {}
for i in range(1, 10):
    g = df[f"q8_{i}"] - df[f"q9_{i}"]; t = stats.ttest_rel(df[f"q8_{i}"], df[f"q9_{i}"])
    gaps[i] = [g.mean(), t.statistic, t.pvalue, g.mean() / g.std()]
R["H4_gaps_correct"] = gaps
rows = []
for i in range(1, 10):
    tab = sm.stats.anova_lm(smf.ols(f"sc18_{i} ~ C(size)*C(tier)", data=df).fit(), typ=2)
    rows.append([i, tab.loc["C(size):C(tier)", "F"], tab.loc["C(size):C(tier)", "PR(>F)"]])
holm = multipletests([x[2] for x in rows], method="holm")[1]
R["SC18_items"] = [[x[0], x[1], x[2], h] for x, h in zip(rows, holm)]
R["SC18_8_cells"] = {f"{a}_{b}": v for (a, b), v in df.groupby(["size", "tier"]).sc18_8.mean().items()}
R["SC18_1_cells"] = {f"{a}_{b}": v for (a, b), v in df.groupby(["size", "tier"]).sc18_1.mean().items()}

R["A_raw_correct"] = run_all(df, "A_own", "A_fr", "A_djlow", "A_pj", "q4", "A")
R["B_raw_correct"] = run_all(df, "B_own", "B_fr", "B_dj", "B_pj", "q4", "B")

# ======================================================== 既存 parquet 再現（原稿値の出所確認）
pq = pd.read_parquet(PARQ)
P = pd.DataFrame({
    "size": np.where(pq.is_large_firm == 1, "Large", "SMO"),
    "tier": pq.tier_a.astype(str).map({"経営層": "Exec", "管理職": "Mid", "一般職": "Gen"}),
    "age": pq.age.astype(float), "female": (pq.gender_code == 2).astype(int),
    "large": pq.is_large_firm.astype(int),
    "P_own": pq.ownership_promotion, "P_fr": pq.friction_prevention, "P_dj": pq.distributive_justice,
    "P_pj": pq.procedural_justice, "tech": pq.q9_sat_1, "pmo": pq[[f"q9_sat_{i}" for i in range(2, 10)]].mean(axis=1),
    "q4": pq.outcome_q4_score, "q6": pq.continuation_q6_score,
})
P["mid"] = (P.tier == "Mid").astype(int); P["gen"] = (P.tier == "Gen").astype(int)
R["P_parquet_reproduction"] = run_all(P, "P_own", "P_fr", "P_dj", "P_pj", "q4", "P")
R["P_parquet_gaps"] = [float(pq[f"gap_cap_{i}"].mean()) for i in range(1, 10)]
R["P_value_sets"] = {"q8_2": sorted(pq.q8_2.unique().tolist()), "q8_3": sorted(pq.q8_3.unique().tolist()),
                     "sc15_5": sorted(pq.sc15_5.unique().tolist()), "sc9_3": sorted(pq.sc9_3.unique().tolist()),
                     "sc18_1": sorted(pq.sc18_1.unique().tolist()), "q9_2": sorted(pq.q9_2.unique().tolist()),
                     "tenure_code": sorted(pq.tenure_code.unique().tolist())}


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (np.floating, float)): return None if np.isnan(o) else round(float(o), 5)
    return o


with open(OUT, "w", encoding="utf-8") as f:
    json.dump(clean(R), f, ensure_ascii=False, indent=1)
print("saved", OUT)

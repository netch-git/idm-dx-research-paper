# -*- coding: utf-8 -*-
"""
20261014 生データからの独立検算スクリプト
- 入力: data/data[企業規模-職制カラム追加].xlsx （生データ, 8,608行）
        data/ローデータ（ICT活用の調査）1125.xlsx （年齢 AGE のみ補助参照）
- 既存 parquet / 既存スクリプトには一切依存せず、文字列ラベルから直接再コーディングする。
- 原稿（20261014 本文原稿 確定版）の記載定義どおりに尺度を構成し、報告値と照合する。
"""
import sys, os, json, re
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from scipy import stats
from sklearn.cluster import KMeans

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"G:\マイドライブ\antigravity\IDM"
RAW = os.path.join(ROOT, "data", "data[企業規模-職制カラム追加].xlsx")
RAW_ORIG = os.path.join(ROOT, "data", "ローデータ（ICT活用の調査）1125.xlsx")
PARQ = os.path.join(ROOT, "20261008", "artifacts", "analysis_data_n2035_final.parquet")
OUT = os.path.join(ROOT, "20261014", "artifacts", "verify_raw_recalc_results.json")

R = {}  # results


def col(df, prefix, item=None):
    for c in df.columns:
        cs = c.strip()
        if cs.startswith(prefix) and (item is None or f":{item}." in cs):
            return c
    raise KeyError(prefix, item)


def likert(v):
    """高得点=肯定。選択肢の先頭語で判定（部分一致の誤判定を避ける）。"""
    if pd.isna(v):
        return np.nan
    s = str(v).strip()
    if s.startswith("非常に"):
        return 5
    if s.startswith("やや") or s.startswith("ある程度"):
        return 4
    if s.startswith("わからない"):
        return 3
    if s.startswith("あまり"):
        return 2
    if s.startswith("まったく") or s.startswith("全く"):
        return 1
    return np.nan


def num010(v):
    if pd.isna(v):
        return np.nan
    if isinstance(v, (int, float, np.integer, np.floating)):
        return float(v)
    m = re.match(r"^\s*(\d+)", str(v))
    return float(m.group(1)) if m else np.nan


def alpha(X):
    X = np.asarray(X, float)
    k = X.shape[1]
    return k / (k - 1) * (1 - X.var(axis=0, ddof=1).sum() / X.sum(axis=1).var(ddof=1))


def cohen_d(a, b):
    a, b = np.asarray(a), np.asarray(b)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / sp


# ------------------------------------------------------------------ 0. 読込
raw = pd.read_excel(RAW, sheet_name=0)
R["raw_rows"] = len(raw)
R["end_flag_counts"] = raw["終了判定"].value_counts().to_dict()
df = raw[raw["終了判定"] == "本調査終了"].copy().reset_index(drop=True)
R["N_main"] = len(df)

# ------------------------------------------------------------------ 1. 属性
size_c = col(df, "SC2-2")
tier_c = "SC7-2.職制グループ"
df["size"] = df[size_c].map({"大企業": "Large", "SMO": "SMO"})
df["tier"] = df[tier_c].map({"1.経営層": "Exec", "2.部課長クラス": "Mid", "3.一般社員": "Gen"})
R["size_raw_counts"] = df[size_c].value_counts(dropna=False).to_dict()
R["tier_raw_counts"] = df[tier_c].value_counts(dropna=False).to_dict()
R["cell_counts"] = pd.crosstab(df["size"], df["tier"]).to_dict()
df["large"] = (df["size"] == "Large").astype(int)
df["mid"] = (df["tier"] == "Mid").astype(int)
df["gen"] = (df["tier"] == "Gen").astype(int)
df["female"] = (df["性別"] == "女性").astype(int)
R["gender_counts"] = df["性別"].value_counts().to_dict()

# 年齢: 本ファイルの「年齢」列は全件空欄 → 1125 原データの AGE を K_ID で結合
R["age_col_in_given_file_nonnull"] = int(df["年齢"].notna().sum())
orig = pd.read_excel(RAW_ORIG, sheet_name="data")
age_map = orig.set_index("K_ID")["AGE"]
df["age"] = df["K_ID"].map(age_map)
R["age_matched"] = int(df["age"].notna().sum())
R["age_mean_sd"] = [round(df["age"].mean(), 3), round(df["age"].std(), 3)]

# SC2 の生ラベル（1,000人以上の判定確認）
sc2 = col(df, "SC2.")
R["SC2_by_size"] = pd.crosstab(df[sc2], df["size"]).to_dict()

# ------------------------------------------------------------------ 2. 項目コーディング
for i in range(1, 10):
    df[f"sc18_{i}"] = df[col(df, "SC18", i)].map(likert)
    df[f"sc15_{i}"] = df[col(df, "SC15", i)].map(likert)
    df[f"q8_{i}"] = df[col(df, "Q8", i)].map(likert)
    df[f"q9_{i}"] = df[col(df, "Q9", i)].map(likert)
for i in range(1, 11):
    df[f"sc9_{i}"] = df[col(df, "SC9", i)].map(likert)
q4c, q6c = col(df, "Q4"), col(df, "Q6")
df["q4"] = df[q4c].map(num010)
df["q6"] = df[q6c].map(num010)
R["q4_raw_value_counts"] = df[q4c].value_counts(dropna=False).sort_index().astype(int).to_dict()
R["q6_raw_value_counts"] = df[q6c].value_counts(dropna=False).astype(int).to_dict()
R["q4_missing_in_given_file"] = int(df["q4"].isna().sum())

# Q4 欠測の正体を 1125 原データで確認
q4_orig_cols = [c for c in orig.columns if str(c).upper().startswith("Q4")]
R["orig_q4_cols"] = [str(c) for c in q4_orig_cols][:5]
if q4_orig_cols:
    q4o = orig.set_index("K_ID")[q4_orig_cols[0]]
    df["q4_orig"] = df["K_ID"].map(q4o)
    R["orig_q4_value_counts_for_missing"] = df.loc[df["q4"].isna(), "q4_orig"].value_counts(dropna=False).astype(str).to_dict()
    R["orig_q4_value_counts_all"] = df["q4_orig"].value_counts(dropna=False).sort_index().astype(str).to_dict()

items_all = [f"sc18_{i}" for i in range(1, 10)] + [f"sc15_{i}" for i in range(1, 10)] + \
            [f"q8_{i}" for i in range(1, 10)] + [f"q9_{i}" for i in range(1, 10)]
R["likert_uncoded_cells"] = int(df[items_all].isna().sum().sum())

# ------------------------------------------------------------------ 3. 尺度（原稿記載定義）
own_items = [f"sc18_{i}" for i in range(1, 6)]
fr_items = ["sc15_1", "sc15_2", "sc15_4", "sc15_5", "sc15_6"]
df["own"] = df[own_items].mean(axis=1)
df["fr"] = df[fr_items].mean(axis=1)
df["dj"] = df[["sc18_1", "sc18_4"]].mean(axis=1)
df["dj_low"] = 6 - df["dj"]
df["pj"] = df[["sc18_8", "sc18_9"]].mean(axis=1)
df["tech"] = df["q9_1"]
df["pmo"] = df[[f"q9_{i}" for i in range(2, 10)]].mean(axis=1)
R["scales"] = {
    "own_M_SD_alpha": [df.own.mean(), df.own.std(), alpha(df[own_items])],
    "fr_M_SD_alpha": [df.fr.mean(), df.fr.std(), alpha(df[fr_items])],
    "fr_all9_M_SD_alpha": [df[[f"sc15_{i}" for i in range(1, 10)]].mean(axis=1).mean(),
                           df[[f"sc15_{i}" for i in range(1, 10)]].mean(axis=1).std(),
                           alpha(df[[f"sc15_{i}" for i in range(1, 10)]])],
    "tech_M_SD": [df.tech.mean(), df.tech.std()],
    "pmo_M_SD_alpha": [df.pmo.mean(), df.pmo.std(), alpha(df[[f"q9_{i}" for i in range(2, 10)]])],
    "pj_M_SD": [df.pj.mean(), df.pj.std()],
    "dj_M_SD": [df.dj.mean(), df.dj.std()],
}
r, p = stats.pearsonr(df.own, df.fr)
R["r_own_fr"] = [r, p]

# ------------------------------------------------------------------ 4. H1 二元配置分散分析
m = smf.ols("own ~ C(size, Sum) * C(tier, Sum)", data=df).fit()
a2 = sm.stats.anova_lm(smf.ols("own ~ C(size) * C(tier)", data=df).fit(), typ=2)
a3 = sm.stats.anova_lm(m, typ=3)
def pes(tab, key):
    return tab.loc[key, "sum_sq"] / (tab.loc[key, "sum_sq"] + tab.loc["Residual", "sum_sq"])
R["H1_typeII"] = {k: [a2.loc[k, "F"], a2.loc[k, "PR(>F)"], pes(a2, k)] for k in a2.index if k != "Residual"}
R["H1_typeIII"] = {k: [a3.loc[k, "F"], a3.loc[k, "PR(>F)"], pes(a3, k)] for k in a3.index if k not in ("Residual", "Intercept")}
R["H1_df_resid"] = m.df_resid
cells = df.groupby(["size", "tier"])["own"].agg(["count", "mean", "std"])
R["H1_cells"] = {f"{a}_{b}": list(v) for (a, b), v in cells.iterrows()}
for t in ["Mid", "Gen", "Exec"]:
    L = df[(df.tier == t) & (df.size == "Large")].own
    S = df[(df.tier == t) & (df.size == "SMO")].own
    tt = stats.ttest_ind(L, S)  # pooled
    tw = stats.ttest_ind(L, S, equal_var=False)
    R[f"H1_simple_{t}"] = {"diff_L_minus_S": L.mean() - S.mean(), "t_pooled": tt.statistic, "p_pooled": tt.pvalue,
                           "t_welch": tw.statistic, "p_welch": tw.pvalue, "d": cohen_d(L, S)}

# ------------------------------------------------------------------ 5. H2 k-means + logit
Z = df[["own", "fr"]].apply(lambda s: (s - s.mean()) / s.std())
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Z)
df["cl"] = km.labels_
prof = df.groupby("cl")[["own", "fr"]].mean()
prof["n"] = df.cl.value_counts()
R["H2_cluster_profiles"] = prof.round(4).reset_index().to_dict(orient="records")
# 低当事者意識・高摩擦 = own 平均が最小かつ fr が相対的に高いクラスタ
alien = prof.assign(score=prof.fr - prof.own).score.idxmax()
df["alien"] = (df.cl == alien).astype(int)
R["H2_alien_n_pct"] = [int(df.alien.sum()), df.alien.mean() * 100]
X1 = sm.add_constant(df[["large", "mid", "gen"]].astype(float))
X2 = sm.add_constant(df[["large", "mid", "gen", "dj_low"]].astype(float))
X3 = sm.add_constant(df[["large", "mid", "gen", "dj_low", "pj"]].astype(float))
l1 = sm.Logit(df.alien, X1).fit(disp=0)
l2 = sm.Logit(df.alien, X2).fit(disp=0)
l3 = sm.Logit(df.alien, X3).fit(disp=0)
def lsum(l):
    ci = np.exp(l.conf_int())
    return {"pseudoR2": l.prsquared, "AIC": l.aic,
            "coef": {k: {"B": l.params[k], "SE": l.bse[k], "OR": np.exp(l.params[k]),
                         "CI": [ci.loc[k, 0], ci.loc[k, 1]], "p": l.pvalues[k]} for k in l.params.index}}
R["H2_logit_m1"], R["H2_logit_m2"], R["H2_logit_m3_with_pj"] = lsum(l1), lsum(l2), lsum(l3)

# ------------------------------------------------------------------ 6. H3 調整重回帰
d3 = df.dropna(subset=["age"]).copy()
d3["fr_c"] = d3.fr - d3.fr.mean()
d3["pj_c"] = d3.pj - d3.pj.mean()
base = "own ~ fr_c + pj_c + age + female + large + mid + gen"
h3a = smf.ols(base, data=d3).fit()
h3b = smf.ols(base + " + fr_c:pj_c", data=d3).fit()
sdy = d3.own.std()
def beta(m_, var, data):
    x = data[var] if var in data else data.fr_c * data.pj_c
    return m_.params[var] * x.std() / sdy
R["H3_n"] = len(d3)
R["H3"] = {
    "R2": h3b.rsquared, "adjR2": h3b.rsquared_adj, "dR2": h3b.rsquared - h3a.rsquared,
    "pj": [h3b.params["pj_c"], beta(h3b, "pj_c", d3), h3b.tvalues["pj_c"], h3b.pvalues["pj_c"]],
    "fr": [h3b.params["fr_c"], beta(h3b, "fr_c", d3), h3b.tvalues["fr_c"], h3b.pvalues["fr_c"]],
    "int": [h3b.params["fr_c:pj_c"], h3b.params["fr_c:pj_c"] * (d3.fr_c * d3.pj_c).std() / sdy,
            h3b.tvalues["fr_c:pj_c"], h3b.pvalues["fr_c:pj_c"]],
}
V = h3b.cov_params()
sdpj = d3.pj_c.std()
ss = {}
for lab, w in [("-1SD", -sdpj), ("Mean", 0.0), ("+1SD", sdpj)]:
    b = h3b.params["fr_c"] + w * h3b.params["fr_c:pj_c"]
    se = np.sqrt(V.loc["fr_c", "fr_c"] + w ** 2 * V.loc["fr_c:pj_c", "fr_c:pj_c"] + 2 * w * V.loc["fr_c", "fr_c:pj_c"])
    t = b / se
    ss[lab] = [b, se, t, 2 * stats.t.sf(abs(t), h3b.df_resid)]
R["H3_simple_slopes"] = ss

# ------------------------------------------------------------------ 7. H4
gaps = {}
for i in range(1, 10):
    g = df[f"q8_{i}"] - df[f"q9_{i}"]
    t = stats.ttest_rel(df[f"q8_{i}"], df[f"q9_{i}"])
    gaps[i] = [g.mean(), t.statistic, t.pvalue, g.mean() / g.std()]
R["H4_gaps"] = gaps
d4 = df.dropna(subset=["age", "q4"]).copy()
h4 = smf.ols("q4 ~ age + female + large + mid + gen + tech + pmo", data=d4).fit()
R["H4_n"] = len(d4)
R["H4"] = {"R2": h4.rsquared, "adjR2": h4.rsquared_adj, "F": h4.fvalue, "df": [h4.df_model, h4.df_resid],
           "tech": [h4.params["tech"], h4.params["tech"] * d4.tech.std() / d4.q4.std(), h4.tvalues["tech"], h4.pvalues["tech"]],
           "pmo": [h4.params["pmo"], h4.params["pmo"] * d4.pmo.std() / d4.q4.std(), h4.tvalues["pmo"], h4.pvalues["pmo"]]}
# 参考: 欠測Q4を5で補完した場合（既存パイプラインの処理）
d4i = df.dropna(subset=["age"]).copy()
d4i["q4i"] = d4i.q4.fillna(5)
h4i = smf.ols("q4i ~ age + female + large + mid + gen + tech + pmo", data=d4i).fit()
R["H4_imputed5"] = {"R2": h4i.rsquared, "tech_beta": h4i.params["tech"] * d4i.tech.std() / d4i.q4i.std(), "tech_p": h4i.pvalues["tech"],
                    "pmo_beta": h4i.params["pmo"] * d4i.pmo.std() / d4i.q4i.std(), "pmo_p": h4i.pvalues["pmo"]}

# ------------------------------------------------------------------ 8. H5
for lab, q4col in [("listwise", "q4"), ("imputed5", "q4i5")]:
    dd = df.copy()
    dd["q4i5"] = dd.q4.fillna(5)
    dd = dd.dropna(subset=[q4col])
    dlt = dd.q6 - dd[q4col]
    t = stats.ttest_rel(dd.q6, dd[q4col])
    out = {"n": len(dd), "q6_M_SD": [dd.q6.mean(), dd.q6.std()], "q4_M_SD": [dd[q4col].mean(), dd[q4col].std()],
           "delta_M_SD": [dlt.mean(), dlt.std()], "t": t.statistic, "p": t.pvalue, "dz": dlt.mean() / dlt.std(),
           "pos_n_pct": [int((dlt > 0).sum()), (dlt > 0).mean() * 100]}
    dd["dlt"] = dlt
    cs = dd.groupby(["size", "tier"])["dlt"].agg(["count", "mean", "std", lambda s: (s > 0).mean() * 100])
    out["cells"] = {f"{a}_{b}": list(v) for (a, b), v in cs.iterrows()}
    sm_ = dd[(dd["size"] == "SMO") & (dd.tier == "Mid")].dlt
    lm_ = dd[(dd["size"] == "Large") & (dd.tier == "Mid")].dlt
    sg_ = dd[(dd["size"] == "SMO") & (dd.tier == "Gen")].dlt
    out["SMOmid_vs_Lmid"] = [sm_.mean() - lm_.mean(), stats.ttest_ind(sm_, lm_).statistic, stats.ttest_ind(sm_, lm_).pvalue, cohen_d(sm_, lm_)]
    out["SMOmid_vs_SMOgen"] = [sm_.mean() - sg_.mean(), stats.ttest_ind(sm_, sg_).statistic, stats.ttest_ind(sm_, sg_).pvalue, cohen_d(sm_, sg_)]
    R[f"H5_{lab}"] = out

# ------------------------------------------------------------------ 9. SC18 個別9項目
rows = []
for i in range(1, 10):
    tab = sm.stats.anova_lm(smf.ols(f"sc18_{i} ~ C(size) * C(tier)", data=df).fit(), typ=2)
    rows.append([i, tab.loc["C(size):C(tier)", "F"], tab.loc["C(size):C(tier)", "PR(>F)"]])
holm = multipletests([r_[2] for r_ in rows], method="holm")[1]
R["SC18_items"] = [[r_[0], r_[1], r_[2], h] for r_, h in zip(rows, holm)]
R["SC18_8_cells"] = df.groupby(["size", "tier"])["sc18_8"].mean().round(4).rename(lambda x: x).to_dict()
R["SC18_1_cells"] = df.groupby(["size", "tier"])["sc18_1"].mean().round(4).to_dict()
R["SC18_8_cells"] = {f"{a}_{b}": v for (a, b), v in R["SC18_8_cells"].items()}
R["SC18_1_cells"] = {f"{a}_{b}": v for (a, b), v in R["SC18_1_cells"].items()}

# ------------------------------------------------------------------ 10. 感度分析（再現可能なもの）
df["own9"] = df[[f"sc18_{i}" for i in range(1, 10)]].mean(axis=1)
sens = {}
sens["M4_SC18_all9"] = sm.stats.anova_lm(smf.ols("own9 ~ C(size) * C(tier)", data=df).fit(), typ=2).loc["C(size):C(tier)", ["F", "PR(>F)"]].tolist()
sens["M7_HC3"] = sm.stats.anova_lm(smf.ols("own ~ C(size) * C(tier)", data=df).fit(), typ=2, robust="hc3").loc["C(size):C(tier)", ["F", "PR(>F)"]].tolist()
da = df.dropna(subset=["age"])
sens["M3_ANCOVA_age_sex"] = sm.stats.anova_lm(smf.ols("own ~ age + female + C(size) * C(tier)", data=da).fit(), typ=2).loc["C(size):C(tier)", ["F", "PR(>F)"]].tolist()
R["sensitivity"] = sens

# ------------------------------------------------------------------ 11. 既存 parquet との突合（コーディング差の特定）
pq = pd.read_parquet(PARQ).set_index("resp_id")
mm = df.set_index("K_ID")
common = mm.index.intersection(pq.index)
R["parquet_id_match"] = len(common)
diag = {}
for i in [1, 4, 8]:
    # parquet は 1=肯定…5=否定 の逆向き → 6-x で揃える
    a_ = 6 - pq.loc[common, f"q8_{i}"]
    b_ = mm.loc[common, f"q8_{i}"]
    diag[f"q8_{i}_mismatch_n"] = int((a_ != b_).sum())
    diag[f"q8_{i}_crosstab_raw_vs_parquet"] = pd.crosstab(mm.loc[common, col(df, 'Q8', i)], pq.loc[common, f"q8_{i}"]).to_dict()
for i in [1, 5]:
    a_ = 6 - pq.loc[common, f"sc15_{i}"]
    b_ = mm.loc[common, f"sc15_{i}"]
    diag[f"sc15_{i}_mismatch_n"] = int((a_ != b_).sum())
    diag[f"sc15_{i}_crosstab_raw_vs_parquet"] = pd.crosstab(mm.loc[common, col(df, 'SC15', i)], pq.loc[common, f"sc15_{i}"]).to_dict()
for i in [1, 8]:
    a_ = 6 - pq.loc[common, f"sc18_{i}"]
    b_ = mm.loc[common, f"sc18_{i}"]
    diag[f"sc18_{i}_mismatch_n"] = int((a_ != b_).sum())
for i in [1, 3]:
    a_ = 6 - pq.loc[common, f"q9_{i}"]
    b_ = mm.loc[common, f"q9_{i}"]
    diag[f"q9_{i}_mismatch_n"] = int((a_ != b_).sum())
diag["tenure_code_unique"] = pq["tenure_code"].unique().tolist()
diag["industry_code_unique"] = pq["industry_code"].unique().tolist()[:5]
diag["region_code_unique"] = pq["region_code"].unique().tolist()[:5]
diag["firm_size_scale_unique"] = pq["firm_size_scale"].unique().tolist()[:5]
diag["parquet_q4_eq5_n"] = int((pq["outcome_q4_score"] == 5).sum())
diag["raw_q4_eq5_n"] = int((df["q4"] == 5).sum())
diag["parquet_ownership_def_check_SC18_12367"] = float(pq["ownership_promotion"].mean())
diag["parquet_friction_mean_sd"] = [float(pq["friction_prevention"].mean()), float(pq["friction_prevention"].std())]
diag["parquet_age_mean_sd"] = [float(pq["age"].mean()), float(pq["age"].std())]
R["parquet_diagnostics"] = diag


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if np.isnan(o) else round(float(o), 6)
    return o


with open(OUT, "w", encoding="utf-8") as f:
    json.dump(clean(R), f, ensure_ascii=False, indent=1)
print(json.dumps(clean(R), ensure_ascii=False, indent=1))

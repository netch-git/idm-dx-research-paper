"""
01_analysis.py — 全量決定論的 2×3 二元配置分散分析パイプライン
================================================================
入力 : data-cross.xlsx（G:\\マイドライブ\\antigravity\\IDM → G:\\マイドライブ\\IDM の順に探索）
出力 : artifacts/results_summary.json   … 論文本文バインド用マスターデータ（唯一の数値ソース）
       reports/statistical_audit_log.md  … 査読監査用再現性レポート

設計（20261004_1338 ダッシュボードと同一ロジック）
  解析母集団 : 終了判定 == '本調査終了'（本調査完了者）。母集団内での除外・間引きは一切行わない。
  IV1 企業規模: SC2 が 1,000人以上の4区分 → Large、それ以外（「わからない」を含む）→ SMO
  IV2 職制    : SC7-2.職制グループ（1.経営層 / 2.部課長クラス / 3.一般社員）
  DV 主解析   : SC18（DX推進意識・9項目）合成平均
  DV 副解析   : SC15（デジタル化に伴う懸念・9項目）合成平均
  検定       : Type II ANOVA（主）、Type III ANOVA・HC3頑健ANOVA（感度）、Tukey-Kramer HSD、
               Levene（Brown–Forsythe）、感度分析3種
乱数は使用しない（完全決定論）。
"""
import hashlib
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import scipy
import scipy.stats as st
import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ART = os.path.join(ROOT, "artifacts")
REP = os.path.join(ROOT, "reports")
CANDIDATES = [r"G:\マイドライブ\antigravity\IDM\data-cross.xlsx", r"G:\マイドライブ\IDM\data-cross.xlsx"]

LARGE_LEVELS = ["1,000人～2,999人", "3,000人～4,999人", "5,000人～9,999人", "10,000人以上"]
POS_LEVELS = ["1.経営層", "2.部課長クラス", "3.一般社員"]
POS_EN = {"1.経営層": "Executives", "2.部課長クラス": "Managers", "3.一般社員": "Staff"}
SIZE_LEVELS = ["Large", "SMO"]

MAP_SC15 = {"まったく当てはまらない": 1, "あまり当てはまらない": 2, "わからない・どちらともいえない": 3,
            "やや当てはまる": 4, "非常に当てはまる": 5}
MAP_SC18 = {"まったくそう思わない": 1, "あまりそう思わない": 2, "わからない・どちらともいえない": 3,
            "ややそう思う": 4, "非常にそう思う": 5}
MIDPOINT_LABEL = "わからない・どちらともいえない"
SCALES = {"SC18": ("SC18.", MAP_SC18, "DX推進意識（9項目）"), "SC15": ("SC15.", MAP_SC15, "デジタル化に伴う懸念（9項目）")}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cronbach(items: pd.DataFrame):
    x = items.dropna()
    k = x.shape[1]
    item_var = x.var(axis=0, ddof=1)
    total_var = x.sum(axis=1).var(ddof=1)
    alpha = k / (k - 1) * (1 - item_var.sum() / total_var)
    total = x.sum(axis=1)
    citc, aid = {}, {}
    for c in x.columns:
        rest = total - x[c]
        citc[c] = float(np.corrcoef(x[c], rest)[0, 1])
        sub = x.drop(columns=c)
        aid[c] = float((k - 1) / (k - 2) * (1 - sub.var(ddof=1).sum() / sub.sum(axis=1).var(ddof=1)))
    return {"alpha": float(alpha), "k": int(k), "n": int(len(x)), "sum_item_variances": float(item_var.sum()),
            "total_score_variance": float(total_var), "corrected_item_total_r": citc, "alpha_if_deleted": aid}


def short_item(col):
    return col.split(":", 1)[1] if ":" in col else col


def anova(df, dv, typ=2, robust=None):
    if typ == 3:
        formula = f"{dv} ~ C(size, Sum) * C(position, Sum)"
    else:
        formula = f"{dv} ~ C(size) * C(position)"
    model = ols(formula, data=df).fit()
    tab = sm.stats.anova_lm(model, typ=typ, robust=robust)
    res_ss = tab.loc["Residual", "sum_sq"]
    out = {}
    for idx, row in tab.iterrows():
        name = str(idx)
        key = ("Intercept" if "Intercept" in name else
               "interaction" if ":" in name else
               "size" if "size" in name else
               "position" if "position" in name else "residual")
        rec = {"sum_sq": float(row["sum_sq"]), "df": int(row["df"])}
        if key not in ("residual",):
            rec["F"] = float(row["F"])
            rec["p"] = float(row["PR(>F)"])
            if robust is None:
                rec["partial_eta_sq"] = float(row["sum_sq"] / (row["sum_sq"] + res_ss))
        else:
            rec["mean_sq"] = float(row["sum_sq"] / row["df"])
        out[key] = rec
    return out


def cell_desc(df, dv):
    rows = []
    for s in SIZE_LEVELS:
        for p in POS_LEVELS:
            v = df.loc[(df["size"] == s) & (df["position"] == p), dv].dropna().values
            n = len(v)
            m, sd = float(np.mean(v)), float(np.std(v, ddof=1))
            se = sd / np.sqrt(n)
            tcrit = float(st.t.ppf(0.975, n - 1))
            q = np.percentile(v, [25, 50, 75])
            rows.append({"size": s, "position": p, "position_en": POS_EN[p], "n": int(n), "mean": m, "sd": sd,
                         "se": float(se), "t_crit": tcrit, "ci95_low": float(m - tcrit * se),
                         "ci95_high": float(m + tcrit * se), "q1": float(q[0]), "median": float(q[1]),
                         "q3": float(q[2]), "min": float(v.min()), "max": float(v.max())})
    return rows


def marginal(df, dv, factor, levels):
    out = []
    for lv in levels:
        v = df.loc[df[factor] == lv, dv].values
        n = len(v)
        m, sd = float(v.mean()), float(v.std(ddof=1))
        se = sd / np.sqrt(n)
        tc = float(st.t.ppf(0.975, n - 1))
        out.append({"level": lv, "n": int(n), "mean": m, "sd": sd, "ci95_low": m - tc * se, "ci95_high": m + tc * se})
    return out


def tukey(df, dv, group_col):
    res = pairwise_tukeyhsd(df[dv].values, df[group_col].values, alpha=0.05)
    groups = res.groupsunique
    pairs = []
    k = 0
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            g1, g2 = str(groups[i]), str(groups[j])
            a = df.loc[df[group_col] == g1, dv].values
            b = df.loc[df[group_col] == g2, dv].values
            sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
            pairs.append({"group1": g1, "group2": g2, "meandiff": float(res.meandiffs[k]),
                          "p_adj": float(res.pvalues[k]), "ci95_low": float(res.confint[k][0]),
                          "ci95_high": float(res.confint[k][1]), "reject": bool(res.reject[k]),
                          "cohens_d": float((b.mean() - a.mean()) / sp)})
            k += 1
    return pairs


def simple_effects_size(df, dv):
    """各職制内での企業規模差（Welch t, Holm 補正, Hedges g）。交互作用の解釈用。"""
    rows, ps = [], []
    for p in POS_LEVELS:
        a = df.loc[(df["position"] == p) & (df["size"] == "Large"), dv].values
        b = df.loc[(df["position"] == p) & (df["size"] == "SMO"), dv].values
        t, pv = st.ttest_ind(a, b, equal_var=False)
        va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
        dfw = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
        sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
        d = (a.mean() - b.mean()) / sp
        g = d * (1 - 3 / (4 * (len(a) + len(b)) - 9))
        rows.append({"position": p, "position_en": POS_EN[p], "n_large": int(len(a)), "n_smo": int(len(b)),
                     "mean_diff_large_minus_smo": float(a.mean() - b.mean()), "welch_t": float(t),
                     "welch_df": float(dfw), "p_raw": float(pv), "hedges_g": float(g)})
        ps.append(pv)
    adj = multipletests(ps, method="holm")[1]
    for r, a in zip(rows, adj):
        r["p_holm"] = float(a)
    return rows


def levene_bf(df, dv):
    groups = [df.loc[(df["size"] == s) & (df["position"] == p), dv].values for s in SIZE_LEVELS for p in POS_LEVELS]
    w, p = st.levene(*groups, center="median")
    return {"W": float(w), "p": float(p), "df1": 5, "df2": int(len(df) - 6)}


def full_block(df, dv):
    return {
        "n": int(len(df)),
        "grand_mean": float(df[dv].mean()), "grand_sd": float(df[dv].std(ddof=1)),
        "cells": cell_desc(df, dv),
        "marginal_size": marginal(df, dv, "size", SIZE_LEVELS),
        "marginal_position": marginal(df, dv, "position", POS_LEVELS),
        "anova_type2": anova(df, dv, 2),
        "anova_type3": anova(df, dv, 3),
        "anova_type2_hc3": anova(df, dv, 2, robust="hc3"),
        "levene_brown_forsythe": levene_bf(df, dv),
        "tukey_cells": tukey(df, dv, "cell"),
        "tukey_position": tukey(df, dv, "position"),
        "simple_effects_size_within_position": simple_effects_size(df, dv),
    }


def prepare(df_raw, mask, midpoint_as_missing=False):
    d = df_raw.loc[mask].copy()
    sc2 = [c for c in d.columns if "SC2." in str(c)][0]
    d["size"] = np.where(d[sc2].isin(LARGE_LEVELS), "Large", "SMO")
    d.loc[d[sc2].isna(), "size"] = np.nan
    d["position"] = d["SC7-2.職制グループ"]
    item_cols = {}
    for key, (pre, mp, _) in SCALES.items():
        cols = [c for c in d.columns if str(c).startswith(pre)]
        item_cols[key] = cols
        num = pd.DataFrame({c: d[c].map(mp) for c in cols}, index=d.index)
        if midpoint_as_missing:
            num = num.where(num != 3)
        d[f"dv_{key}"] = num.mean(axis=1)
        for c in cols:
            d[f"num_{key}_{cols.index(c) + 1}"] = num[c]
    d["cell"] = d["size"].astype(str) + "|" + d["position"].astype(str)
    return d, item_cols, sc2


def main():
    src = next(p for p in CANDIDATES if os.path.exists(p))
    df_raw = pd.read_excel(src)
    main_mask = df_raw["終了判定"] == "本調査終了"
    d, item_cols, sc2 = prepare(df_raw, main_mask)

    # ---------- 欠損・フロー監査 ----------
    flow = {
        "raw_rows": int(len(df_raw)),
        "screen_only_rows_SC終了": int((df_raw["終了判定"] == "SC終了").sum()),
        "main_survey_rows_本調査終了": int(main_mask.sum()),
        "sc2_counts_main": {str(k): int(v) for k, v in d[sc2].value_counts(dropna=False).items()},
        "sc2_unknown_classified_as_SMO": int((d[sc2] == "わからない").sum()),
        "sc7_2_counts_main": {str(k): int(v) for k, v in d["position"].value_counts(dropna=False).items()},
        "missing_main": {
            "size": int(d["size"].isna().sum()), "position": int(d["position"].isna().sum()),
            **{f"{k}_items_any_missing_rows": int(d[[f'num_{k}_{i + 1}' for i in range(len(v))]].isna().any(axis=1).sum())
               for k, v in item_cols.items()},
            **{f"{k}_unmapped_values": int(sum((~df_raw.loc[main_mask, c].isin(list(SCALES[k][1].keys()))
                                                & df_raw.loc[main_mask, c].notna()).sum() for c in v))
               for k, v in item_cols.items()},
        },
        "midpoint_response_rate": {k: float((d[[f'num_{k}_{i + 1}' for i in range(len(v))]] == 3).values.mean())
                                   for k, v in item_cols.items()},
    }
    valid = d.dropna(subset=["size", "position", "dv_SC18", "dv_SC15"])
    flow["analysed_n"] = int(len(valid))
    flow["excluded_n"] = int(len(d) - len(valid))
    assert flow["excluded_n"] == 0, "解析母集団内で除外が発生しています（全量処理違反）"

    # ---------- 信頼性・項目統計 ----------
    reliability, items = {}, {}
    for k, cols in item_cols.items():
        num = valid[[f"num_{k}_{i + 1}" for i in range(len(cols))]]
        num.columns = [short_item(c) for c in cols]
        reliability[k] = cronbach(num)
        items[k] = []
        for i, c in enumerate(cols):
            col = f"num_{k}_{i + 1}"
            rec = {"no": i + 1, "label": short_item(c), "mean": float(valid[col].mean()), "sd": float(valid[col].std(ddof=1)),
                   "by_cell": {f"{s}|{p}": float(valid.loc[(valid['size'] == s) & (valid['position'] == p), col].mean())
                               for s in SIZE_LEVELS for p in POS_LEVELS}}
            items[k].append(rec)
    r_sc18_sc15 = st.pearsonr(valid["dv_SC18"], valid["dv_SC15"])

    # ---------- 主解析 ----------
    analyses = {k: full_block(valid, f"dv_{k}") for k in SCALES}

    # ---------- 感度分析 ----------
    sens = {}
    v_known = valid[valid[sc2] != "わからない"]
    sens["exclude_sc2_unknown"] = {k: {"n": int(len(v_known)), "anova_type2": anova(v_known, f"dv_{k}", 2)} for k in SCALES}
    d_mid, _, _ = prepare(df_raw, main_mask, midpoint_as_missing=True)
    sens["midpoint_as_missing"] = {}
    for k in SCALES:
        dm = d_mid.dropna(subset=["size", "position", f"dv_{k}"])
        sens["midpoint_as_missing"][k] = {"n": int(len(dm)), "n_all_items_midpoint": int(len(d_mid) - len(dm)),
                                          "anova_type2": anova(dm, f"dv_{k}", 2),
                                          "cells": [{"size": c["size"], "position": c["position"], "n": c["n"], "mean": c["mean"]}
                                                    for c in cell_desc(dm, f"dv_{k}")]}
    all_mask = pd.Series(True, index=df_raw.index)
    d_all, _, _ = prepare(df_raw, all_mask)
    sens["all_available_respondents"] = {}
    for k in SCALES:
        da = d_all.dropna(subset=["size", "position", f"dv_{k}"])
        sens["all_available_respondents"][k] = {
            "n": int(len(da)), "n_main_survey": int((da["終了判定"] == "本調査終了").sum()),
            "n_screening_only": int((da["終了判定"] == "SC終了").sum()),
            "anova_type2": anova(da, f"dv_{k}", 2),
            "cells": [{"size": c["size"], "position": c["position"], "n": c["n"], "mean": c["mean"]} for c in cell_desc(da, f"dv_{k}")]}

    summary = {
        "meta": {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_file": src, "source_sha256": sha256(src),
            "software": {"python": sys.version.split()[0], "pandas": pd.__version__, "numpy": np.__version__,
                         "scipy": scipy.__version__, "statsmodels": statsmodels.__version__},
            "population": "終了判定 == '本調査終了'",
            "iv_size_rule": "SC2 ∈ {" + ", ".join(LARGE_LEVELS) + "} → Large; otherwise (incl. 'わからない') → SMO",
            "iv_position_levels": POS_LEVELS,
            "dv": {k: v[2] for k, v in SCALES.items()},
            "likert_midpoint_label": MIDPOINT_LABEL,
            "primary_dv": "SC18", "secondary_dv": "SC15",
            "ci_method": "t-distribution, df = n - 1",
            "anova_primary": "Type II SS (statsmodels anova_lm typ=2)",
        },
        "flow": flow,
        "reliability": reliability,
        "items": items,
        "correlation_SC18_SC15": {"r": float(r_sc18_sc15[0]), "p": float(r_sc18_sc15[1]), "n": int(len(valid))},
        "analyses": analyses,
        "sensitivity": sens,
    }
    os.makedirs(ART, exist_ok=True)
    with open(os.path.join(ART, "results_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    valid[["size", "position", "dv_SC18", "dv_SC15"]].to_csv(os.path.join(ART, "analysis_dataset_scores.csv"),
                                                              encoding="utf-8-sig", index_label="row_index")
    write_audit_log(summary)
    print("OK: artifacts/results_summary.json, reports/statistical_audit_log.md")


def fp(p):
    return "< .001" if p < 0.001 else f"= {p:.3f}".replace("0.", ".")


def write_audit_log(S):
    L = []
    m, fl = S["meta"], S["flow"]
    L += ["# 統計解析 監査用再現性レポート（statistical_audit_log.md）", "",
          f"- 生成日時: {m['generated_at']}", f"- 入力ファイル: `{m['source_file']}`",
          f"- SHA-256: `{m['source_sha256']}`",
          f"- 実行環境: Python {m['software']['python']} / pandas {m['software']['pandas']} / numpy {m['software']['numpy']} / "
          f"scipy {m['software']['scipy']} / statsmodels {m['software']['statsmodels']}",
          "- 乱数: 不使用（完全決定論的）", "",
          "## 1. 標本フローと欠損値判定", "",
          "| 段階 | 件数 |", "|---|---:|",
          f"| 生データ総行数 | {fl['raw_rows']:,} |",
          f"| スクリーニングのみ（SC終了） | {fl['screen_only_rows_SC終了']:,} |",
          f"| 本調査完了（解析母集団） | {fl['main_survey_rows_本調査終了']:,} |",
          f"| 解析母集団内の除外 | {fl['excluded_n']} |",
          f"| **解析対象 N** | **{fl['analysed_n']:,}** |", "",
          f"- SC2「わからない」 {fl['sc2_unknown_classified_as_SMO']} 件は規則（1,000人以上以外＝SMO）に従いSMOに分類（感度分析で除外版も算出）。",
          f"- 欠損: {json.dumps(fl['missing_main'], ensure_ascii=False)}",
          f"- 中間選択肢「{m['likert_midpoint_label']}」の選択率: " +
          ", ".join(f"{k} {v * 100:.1f}%" for k, v in fl['midpoint_response_rate'].items()), "",
          "### 企業規模（SC2）内訳", "", "| 回答 | n |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in fl["sc2_counts_main"].items()]
    L += ["", "### 職制（SC7-2）内訳", "", "| 回答 | n |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in fl["sc7_2_counts_main"].items()]
    L += ["", "## 2. 尺度の信頼性", ""]
    for k, r in S["reliability"].items():
        L += [f"### {k}: {m['dv'][k]}  α = {r['alpha']:.4f}（k = {r['k']}, n = {r['n']}; Σσ²ᵢ = {r['sum_item_variances']:.4f}, σ²ₓ = {r['total_score_variance']:.4f}）", "",
              "| No. | 項目 | M | SD | 修正項目-全体相関 | 項目削除時α |", "|---:|---|---:|---:|---:|---:|"]
        for it in S["items"][k]:
            L.append(f"| {it['no']} | {it['label']} | {it['mean']:.3f} | {it['sd']:.3f} | "
                     f"{r['corrected_item_total_r'][it['label']]:.3f} | {r['alpha_if_deleted'][it['label']]:.3f} |")
        L.append("")
    c = S["correlation_SC18_SC15"]
    L += [f"SC18–SC15 合成得点間相関: r = {c['r']:.3f}, p {fp(c['p'])}, n = {c['n']}", ""]
    sec = 3
    for k, A in S["analyses"].items():
        L += [f"## {sec}. {k}（{m['dv'][k]}）", "", f"全体 M = {A['grand_mean']:.3f}, SD = {A['grand_sd']:.3f}", "",
              "### 記述統計（t分布95%CI）", "", "| 規模 | 職制 | n | M | SD | SE | 95%CI | Q1 | Mdn | Q3 |",
              "|---|---|---:|---:|---:|---:|---|---:|---:|---:|"]
        for r in A["cells"]:
            L.append(f"| {r['size']} | {r['position']} | {r['n']} | {r['mean']:.3f} | {r['sd']:.3f} | {r['se']:.3f} | "
                     f"[{r['ci95_low']:.3f}, {r['ci95_high']:.3f}] | {r['q1']:.3f} | {r['median']:.3f} | {r['q3']:.3f} |")
        for label, key in [("Type II（主解析）", "anova_type2"), ("Type III（感度）", "anova_type3"), ("Type II + HC3頑健（感度）", "anova_type2_hc3")]:
            T = A[key]
            L += ["", f"### ANOVA {label}", "", "| 要因 | SS | df | F | p | partial η² |", "|---|---:|---:|---:|---:|---:|"]
            for f_ in ["size", "position", "interaction"]:
                t = T[f_]
                pe = f"{t['partial_eta_sq']:.4f}" if "partial_eta_sq" in t else "—"
                L.append(f"| {f_} | {t['sum_sq']:.4f} | {t['df']} | {t['F']:.3f} | {t['p']:.3g} | {pe} |")
            L.append(f"| residual | {T['residual']['sum_sq']:.4f} | {T['residual']['df']} | | | |")
        lv = A["levene_brown_forsythe"]
        L += ["", f"Levene（Brown–Forsythe）: W({lv['df1']}, {lv['df2']}) = {lv['W']:.3f}, p = {lv['p']:.3g}", "",
              "### Tukey-Kramer HSD（6セル, 15対比）", "", "| 群1 | 群2 | 差(群2−群1) | p_adj | 95%CI | d | 判定 |",
              "|---|---|---:|---:|---|---:|---|"]
        for t in A["tukey_cells"]:
            L.append(f"| {t['group1']} | {t['group2']} | {t['meandiff']:+.3f} | {t['p_adj']:.4f} | "
                     f"[{t['ci95_low']:+.3f}, {t['ci95_high']:+.3f}] | {t['cohens_d']:+.3f} | {'有意' if t['reject'] else 'n.s.'} |")
        L += ["", "### Tukey-Kramer HSD（職制周辺）", "", "| 群1 | 群2 | 差 | p_adj | 95%CI |", "|---|---|---:|---:|---|"]
        for t in A["tukey_position"]:
            L.append(f"| {t['group1']} | {t['group2']} | {t['meandiff']:+.3f} | {t['p_adj']:.4g} | [{t['ci95_low']:+.3f}, {t['ci95_high']:+.3f}] |")
        L += ["", "### 単純効果: 職制内の規模差（Welch t, Holm補正）", "", "| 職制 | n(L) | n(S) | 差(L−S) | t | df | p_holm | g |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
        for t in A["simple_effects_size_within_position"]:
            L.append(f"| {t['position']} | {t['n_large']} | {t['n_smo']} | {t['mean_diff_large_minus_smo']:+.3f} | {t['welch_t']:.3f} | "
                     f"{t['welch_df']:.1f} | {t['p_holm']:.4g} | {t['hedges_g']:+.3f} |")
        L.append("")
        sec += 1
    L += [f"## {sec}. 感度分析", ""]
    for name, block in S["sensitivity"].items():
        L += [f"### {name}", "", "| DV | N | F(size) | p | F(position) | p | F(interaction) | p |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
        for k, b in block.items():
            T = b["anova_type2"]
            L.append(f"| {k} | {b['n']} | {T['size']['F']:.3f} | {T['size']['p']:.3g} | {T['position']['F']:.3f} | {T['position']['p']:.3g} | "
                     f"{T['interaction']['F']:.3f} | {T['interaction']['p']:.3g} |")
        L.append("")
    with open(os.path.join(REP, "statistical_audit_log.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()

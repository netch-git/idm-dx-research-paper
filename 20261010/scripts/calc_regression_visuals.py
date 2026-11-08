import pyarrow.parquet as pq
import statsmodels.api as sm
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
import itertools
import json

df = pd.read_parquet(r'G:\マイドライブ\antigravity\IDM\20261008\artifacts\analysis_data_n2035_final.parquet')
y_col = 'outcome_q4_score'
df['sat_tech'] = df['q9_sat_1']
df['sat_pmo'] = (df['q9_sat_2'] + df['q9_sat_3'] + df['q9_sat_4'] + df['q9_sat_5'] + df['q9_sat_6'] + df['q9_sat_7'] + df['q9_sat_8'] + df['q9_sat_9']) / 8.0
df['is_manager'] = (df['tier_a'] == '管理職').astype(int)
df['is_staff'] = (df['tier_a'] == '一般職').astype(int)
df['is_female'] = (df['gender_code'] == 2).astype(int)

# Macro Regression Model
f_macro = f"{y_col} ~ sat_pmo + sat_tech + is_large_firm + is_manager + is_staff + is_female + age"
m = ols(f_macro, data=df).fit()

# Standardized Beta calculation
y_sd = df[y_col].std()
vars_info = [
    ('sat_pmo', 'PMO組織変革機能総合 (Q9.2-9)', '#005BAC'),
    ('sat_tech', 'デジタル技術知識・スキル (Q9.1)', '#6C757D'),
    ('is_large_firm', '企業規模 (大企業ダミー)', '#00838F'),
    ('is_manager', '役職: 管理職ダミー', '#718096'),
    ('is_staff', '役職: 一般職ダミー', '#A0AEC0'),
    ('is_female', '性別: 女性ダミー', '#CBD5E0'),
    ('age', '年齢', '#E2E8F0')
]

forest_data = []
for term, label, color in vars_info:
    b = m.params[term]
    se = m.bse[term]
    p = m.pvalues[term]
    t = m.tvalues[term]
    ci_l = m.conf_int().loc[term, 0]
    ci_u = m.conf_int().loc[term, 1]
    x_sd = df[term].std()
    beta = b * (x_sd / y_sd)
    beta_ci_l = ci_l * (x_sd / y_sd)
    beta_ci_u = ci_u * (x_sd / y_sd)
    forest_data.append({
        'term': term,
        'label': label,
        'color': color,
        'b': round(float(b), 4),
        'se': round(float(se), 4),
        't': round(float(t), 3),
        'p': float(p),
        'beta': round(float(beta), 4),
        'ci95_low': round(float(ci_l), 4),
        'ci95_high': round(float(ci_u), 4),
        'beta_ci_low': round(float(beta_ci_l), 4),
        'beta_ci_high': round(float(beta_ci_u), 4)
    })

print("=== Forest Plot Parameters (Raw & Standardized) ===")
for item in forest_data:
    print(f"{item['label']:35s}: beta={item['beta']:+.4f} [{item['beta_ci_low']:+.4f}, {item['beta_ci_high']:+.4f}], p={item['p']:.4e}")

# Shapley Value / Dominance Decomposition
groups = {
    'PMO': ['sat_pmo'],
    'Tech': ['sat_tech'],
    'Size': ['is_large_firm'],
    'Controls': ['age', 'is_female', 'is_manager', 'is_staff']
}
g_names = list(groups.keys())

def get_r2(subset):
    if not subset:
        return 0.0
    cols = []
    for g in subset:
        cols.extend(groups[g])
    formula = f"{y_col} ~ " + " + ".join(cols)
    return ols(formula, data=df).fit().rsquared

perms = list(itertools.permutations(g_names))
shapley = {g: 0.0 for g in g_names}
for perm in perms:
    current = []
    r2_curr = 0.0
    for g in perm:
        next_subset = current + [g]
        r2_next = get_r2(next_subset)
        shapley[g] += (r2_next - r2_curr) / len(perms)
        current = next_subset
        r2_curr = r2_next

total_shapley = sum(shapley.values())
full_r2 = m.rsquared

shapley_results = []
g_labels = {
    'PMO': 'PMO組織変革機能総合 (Q9.2-9)',
    'Size': '企業規模 (大企業/SMO)',
    'Tech': 'デジタル技術知識・スキル (Q9.1)',
    'Controls': '個人属性統制変数 (年齢・性別・役職)'
}
g_colors = {
    'PMO': '#005BAC',
    'Size': '#00838F',
    'Tech': '#718096',
    'Controls': '#CBD5E0'
}

for g in ['PMO', 'Size', 'Tech', 'Controls']:
    val = shapley[g]
    pct = (val / total_shapley) * 100
    shapley_results.append({
        'group': g,
        'label': g_labels[g],
        'color': g_colors[g],
        'r2_contrib': round(float(val), 4),
        'percentage': round(float(pct), 2)
    })

print(f"\n=== Shapley Relative Importance (Full R2 = {full_r2:.4f}) ===")
for r in shapley_results:
    print(f"{r['label']:35s}: R2 = {r['r2_contrib']:.4f} ({r['percentage']:.2f}%)")

output_payload = {
    'forest_plot': forest_data,
    'shapley_decomposition': {
        'full_r2': round(float(full_r2), 4),
        'results': shapley_results
    }
}
with open(r'G:\マイドライブ\antigravity\IDM\20261010\artifacts\regression_visualization_data.json', 'w', encoding='utf-8') as f:
    json.dump(output_payload, f, ensure_ascii=False, indent=2)

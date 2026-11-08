import pandas as pd
import numpy as np
from scipy import stats

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
df = pd.read_excel(path, sheet_name='data', header=0)
df_data = df.iloc[1:].copy()

flag_col = 'SC_MAIN'
# Eligible group (DX implemented firms, reached SC20): N=2,845
# Compare 本調査 (N=2,035) vs SC終了 (N=810)
df_eligible = df_data[df_data['SC19'].isin([1, 2, 3])].copy()
group_main = df_eligible[df_eligible[flag_col] == 2]
group_sc = df_eligible[df_eligible[flag_col] == 1]

print(f"Comparing Eligible Sample (N=2,845): 本調査終了 (N={len(group_main)}) vs SC終了 (N={len(group_sc)})")

# Let's test SC18 items (DX consciousness & friction)
sc18_cols = [f'SC18.{i}' for i in range(1, 10)]
print("\n--- SC18 Items: Comparison between 本調査終了 and SC終了 ---")
for c in sc18_cols:
    v_main = pd.to_numeric(group_main[c], errors='coerce').dropna()
    v_sc = pd.to_numeric(group_sc[c], errors='coerce').dropna()
    m_main, s_main = v_main.mean(), v_main.std()
    m_sc, s_sc = v_sc.mean(), v_sc.std()
    t_val, p_val = stats.ttest_ind(v_main, v_sc, equal_var=False)
    # Cohen's d
    pooled_s = np.sqrt((s_main**2 + s_sc**2) / 2)
    d = (m_main - m_sc) / pooled_s
    print(f"{c:8s} | 本調査: {m_main:.3f} (SD={s_main:.3f}) | SC終了: {m_sc:.3f} (SD={s_sc:.3f}) | Diff: {m_main-m_sc:+.3f} | t={t_val:6.2f}, p={p_val:.4f}, d={d:+.3f}")

# Also check for SC9 items (Work attitude)
sc9_cols = [f'SC9.{i}' for i in range(1, 11)]
print("\n--- SC9 Items: Comparison between 本調査終了 and SC終了 ---")
for c in sc9_cols:
    v_main = pd.to_numeric(group_main[c], errors='coerce').dropna()
    v_sc = pd.to_numeric(group_sc[c], errors='coerce').dropna()
    m_main, s_main = v_main.mean(), v_main.std()
    m_sc, s_sc = v_sc.mean(), v_sc.std()
    t_val, p_val = stats.ttest_ind(v_main, v_sc, equal_var=False)
    pooled_s = np.sqrt((s_main**2 + s_sc**2) / 2)
    d = (m_main - m_sc) / pooled_s
    print(f"{c:8s} | 本調査: {m_main:.3f} (SD={s_main:.3f}) | SC終了: {m_sc:.3f} (SD={s_sc:.3f}) | Diff: {m_main-m_sc:+.3f} | t={t_val:6.2f}, p={p_val:.4f}, d={d:+.3f}")

# Also compare DXNon-Implemented group (SC19 in [4, 5], N=1,377) vs DX-Implemented group (N=2,845) on SC18
df_reached_sc18 = df_data[df_data['SC18.1'].notna()].copy()
df_non_dx = df_reached_sc18[df_reached_sc18['SC19'].isin([4, 5])]
print(f"\n--- SC18 Items: DX取組企業 (N={len(df_eligible)}) vs DX未取組企業 (N={len(df_non_dx)}) ---")
for c in sc18_cols:
    v_dx = pd.to_numeric(df_eligible[c], errors='coerce').dropna()
    v_nodx = pd.to_numeric(df_non_dx[c], errors='coerce').dropna()
    m_dx, s_dx = v_dx.mean(), v_dx.std()
    m_nodx, s_nodx = v_nodx.mean(), v_nodx.std()
    t_val, p_val = stats.ttest_ind(v_dx, v_nodx, equal_var=False)
    pooled_s = np.sqrt((s_dx**2 + s_nodx**2) / 2)
    d = (m_dx - m_nodx) / pooled_s
    print(f"{c:8s} | DX実施: {m_dx:.3f} (SD={s_dx:.3f}) | DX未実施: {m_nodx:.3f} (SD={s_nodx:.3f}) | Diff: {m_dx-m_nodx:+.3f} | t={t_val:6.2f}, p={p_val:.4f}, d={d:+.3f}")


import pandas as pd
import numpy as np

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
df = pd.read_excel(path, sheet_name='data', header=0)
df_data = df.iloc[1:].copy()

flag_col = 'SC_MAIN'
# Filter to those with SC19 in [1, 2, 3] (DX implemented firms)
df_eligible = df_data[df_data['SC19'].isin([1, 2, 3])].copy()
print(f"Eligible respondents (DX implemented, reached SC20): {len(df_eligible)}")
print("Breakdown of SC_MAIN:")
print(df_eligible[flag_col].value_counts())

# Let's check distribution by Company Size (SC2) and Position (SC7)
# SC2: 従業員規模
# SC7: 役職
print("\n--- Cross-tab: SC2 (Company size) vs SC_MAIN ---")
ct_sc2 = pd.crosstab(df_eligible['SC2'], df_eligible[flag_col], margins=True, normalize='index') * 100
print(ct_sc2.round(1))

print("\n--- Cross-tab: SC7 (Position) vs SC_MAIN ---")
ct_sc7 = pd.crosstab(df_eligible['SC7'], df_eligible[flag_col], margins=True, normalize='index') * 100
print(ct_sc7.round(1))

# Check Demographics: SEX, AGE
print("\n--- Cross-tab: SEX vs SC_MAIN ---")
print(pd.crosstab(df_eligible['SEX'], df_eligible[flag_col], margins=True))

print("\n--- Cross-tab: AGE brackets vs SC_MAIN ---")
print(pd.crosstab(df_eligible['AGE'], df_eligible[flag_col], margins=True))

# Check combined cells: Size x Position
# Let's see the count of 本調査 (2) vs SC終了 (1) in each cell of (SC2 x SC7)
cell_counts = df_eligible.groupby(['SC2', 'SC7', flag_col]).size().unstack(fill_value=0)
cell_counts.columns = ['SC終了', '本調査終了']
cell_counts['合計'] = cell_counts['SC終了'] + cell_counts['本調査終了']
cell_counts['本調査率(%)'] = (cell_counts['本調査終了'] / cell_counts['合計'] * 100).round(1)
cell_counts.to_csv(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\eligible_cells_sc2_sc7.csv', encoding='utf-8-sig')

print("\nSample of Size x Position cells (first 20 rows):")
print(cell_counts.head(20))

# Also check date/time or SEQ if sequential completion caused quota fill!
print("\n--- Checking SEQ (order of survey response) ---")
print("Min SEQ by flag:")
print(df_eligible.groupby(flag_col)['SEQ'].agg(['min', 'max', 'mean', 'median']))


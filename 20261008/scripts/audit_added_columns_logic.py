import pandas as pd
import numpy as np
import json
import os

cleaned_path = r"G:\マイドライブ\antigravity\IDM\data\data[企業規模-職制カラム追加].xlsx"
raw_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"
out_dir = r"G:\マイドライブ\antigravity\IDM\20261008"

df_cleaned = pd.read_excel(cleaned_path, sheet_name="data_utf8")

# Let's inspect the exact column names of df_cleaned[:12]
print("Cleaned column names (repr):")
for i, c in enumerate(df_cleaned.columns[:12]):
    print(f"Col {i:2d}: {repr(c)}")

# Check col 6 (which is SC7-2) and col 14 (which is SC7)
col_sc7_2 = df_cleaned.columns[6]
col_sc7 = [c for c in df_cleaned.columns if 'SC7.' in c][0]

print(f"\nCrosstab between SC7 (役職) and SC7-2 (役職グループ):\n")
ct_sc7 = pd.crosstab(df_cleaned[col_sc7], df_cleaned[col_sc7_2], dropna=False)
print(ct_sc7)

# Check other added columns:
# col 1: DX認知×DX取組
col_c1 = df_cleaned.columns[1]
print(f"\nCol 1: {repr(col_c1)} value counts:\n{df_cleaned[col_c1].value_counts(dropna=False)}")

# col 2: 利益×ライフステージ
col_c2 = df_cleaned.columns[2]
print(f"\nCol 2: {repr(col_c2)} value counts:\n{df_cleaned[col_c2].value_counts(dropna=False)}")

# col 3: 従業員×売上
col_c3 = df_cleaned.columns[3]
print(f"\nCol 3: {repr(col_c3)} value counts:\n{df_cleaned[col_c3].value_counts(dropna=False)}")

# col 4: 年代グループ
col_c4 = df_cleaned.columns[4]
print(f"\nCol 4: {repr(col_c4)} value counts:\n{df_cleaned[col_c4].value_counts(dropna=False)}")

# col 5: 役職グループ or something else?
col_c5 = df_cleaned.columns[5]
print(f"\nCol 5: {repr(col_c5)} value counts:\n{df_cleaned[col_c5].value_counts(dropna=False)}")


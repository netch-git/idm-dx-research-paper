import pandas as pd
import numpy as np

cleaned_path = r"G:\マイドライブ\antigravity\IDM\data\data[企業規模-職制カラム追加].xlsx"
raw_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"

df_cleaned = pd.read_excel(cleaned_path, sheet_name="data_utf8")
df_raw_num = pd.read_excel(raw_path, sheet_name="data", header=0)
df_raw_num_data = df_raw_num.iloc[1:].copy()
df_raw_num_data.reset_index(drop=True, inplace=True)

df_raw_text = pd.read_excel(raw_path, sheet_name="data_text", header=0)
df_raw_text_data = df_raw_text.iloc[1:].copy()
df_raw_text_data.reset_index(drop=True, inplace=True)

print("--- AGE Investigation ---")
print("df_raw_num['AGE'] non-null count:", df_raw_num_data['AGE'].notna().sum())
print("df_raw_num['AGE'] unique values (first 10):", df_raw_num_data['AGE'].unique()[:10])
print("df_raw_text['AGE'] non-null count:", df_raw_text_data['AGE'].notna().sum())
print("df_raw_text['AGE'] unique values (first 10):", df_raw_text_data['AGE'].unique()[:10])

# Cleaned columns containing '役職'
yakushoku_cols = [c for c in df_cleaned.columns if '役職' in c]
print("\nCleaned columns with '役職':", yakushoku_cols)
for c in yakushoku_cols:
    print(f"\n{c} value counts:\n", df_cleaned[c].value_counts(dropna=False))

# Crosstab between yakushoku columns
if len(yakushoku_cols) >= 2:
    print(f"\nCrosstab between {yakushoku_cols[0]} and {yakushoku_cols[1]}:\n")
    print(pd.crosstab(df_cleaned[yakushoku_cols[0]], df_cleaned[yakushoku_cols[1]], dropna=False))

# SC2-2 vs SC2 crosstab
sc2_col = [c for c in df_cleaned.columns if 'SC2.' in c and 'SC2-2' not in c][0]
sc2_2_col = [c for c in df_cleaned.columns if 'SC2-2' in c][0]
print(f"\nCrosstab between SC2 and SC2-2:\n")
print(pd.crosstab(df_cleaned[sc2_col], df_cleaned[sc2_2_col], dropna=False))

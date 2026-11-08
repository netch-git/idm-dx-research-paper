import pandas as pd
import numpy as np

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'

print("Loading data sheet (numeric codes)...")
df = pd.read_excel(path, sheet_name='data', header=0)
q_labels = df.iloc[0]
df_data = df.iloc[1:].copy()

print(f"Total rows: {len(df_data)}")
flag_col = 'SC_MAIN'

# In data sheet, what are the values of SC_MAIN?
print("SC_MAIN value counts in numeric sheet:")
print(df_data[flag_col].value_counts(dropna=False))

# Identify SC columns and demographics columns
sc_cols = [c for c in df_data.columns if c.startswith('SC') and c != 'SC_MAIN']
demo_cols = ['SEX', 'AGE', 'CHIIKI', 'MARRIAGE', 'CHILD', 'JOB', 'FAMILY', 'EDUCATION', 'INCOME', 'HOME', 'LICENSE', 'CAR']
q_cols = [c for c in df_data.columns if c.startswith('Q')]

# Check missingness pattern across columns for SC_MAIN == 'SC終了' vs '本調査終了'
# In numeric sheet, values might be 1, 2 or string. Let's inspect.
print("\nUnique values of SC_MAIN:", df_data[flag_col].unique())

# Map flag to clean label
# If 1 is SC終了 and 2 is 本調査終了, or vice versa
counts_by_val = df_data[flag_col].value_counts()
print("Counts by val:", counts_by_val.to_dict())

# Let's inspect which value corresponds to 2035 (本調査終了) and 6573 (SC終了)
val_main = counts_by_val[counts_by_val == 2035].index[0]
val_sc = counts_by_val[counts_by_val == 6573].index[0]
print(f"Value for 本調査終了 (2,035): {val_main}")
print(f"Value for SC終了 (6,573): {val_sc}")

# Let's check non-null counts for each SC question by group
summary_missing = []
for c in sc_cols:
    n_main = df_data[df_data[flag_col] == val_main][c].notna().sum()
    n_sc = df_data[df_data[flag_col] == val_sc][c].notna().sum()
    pct_main = n_main / 2035 * 100
    pct_sc = n_sc / 6573 * 100
    summary_missing.append({
        'column': c,
        'label': str(q_labels[c])[:40],
        'n_main': n_main,
        'pct_main': f"{pct_main:.1f}%",
        'n_sc': n_sc,
        'pct_sc': f"{pct_sc:.1f}%"
    })

df_missing = pd.DataFrame(summary_missing)
df_missing.to_csv(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\sc_missingness_by_flag.csv', index=False, encoding='utf-8-sig')

print("\n--- Missingness transition points in SC questions for SC終了 ---")
for idx, r in df_missing.iterrows():
    if idx == 0 or r['n_sc'] != df_missing.iloc[idx-1]['n_sc']:
        print(f"{r['column']} ({r['label']}): SC終了 non-null = {r['n_sc']} ({r['pct_sc']}), 本調査 non-null = {r['n_main']} ({r['pct_main']})")


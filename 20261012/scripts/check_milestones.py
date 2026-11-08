import pandas as pd

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
df = pd.read_excel(path, sheet_name='data', header=0)
q_labels = df.iloc[0]
df_data = df.iloc[1:].copy()

flag_col = 'SC_MAIN'
val_main = 2
val_sc = 1

# Check SC17, SC18, SC19, SC20, Q1, etc.
check_cols = ['SC1', 'SC2', 'SC7', 'SC8', 'SC11', 'SC14', 'SC17', 'SC18.1', 'SC19', 'SC20.1', 'Q1', 'Q4', 'Q6']

print("=== Non-null count by Question ===")
for c in check_cols:
    if c in df_data.columns:
        n_sc = df_data[df_data[flag_col] == val_sc][c].notna().sum()
        n_main = df_data[df_data[flag_col] == val_main][c].notna().sum()
        print(f"{c:8s} | SC終了 (N=6573): {n_sc:4d} ({n_sc/6573*100:5.1f}%) | 本調査 (N=2035): {n_main:4d} ({n_main/2035*100:5.1f}%) | Label: {str(q_labels[c])[:30]}")


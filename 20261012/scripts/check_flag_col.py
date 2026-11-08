import pandas as pd
import numpy as np

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'

# Read first few rows to find exact header and flag column
df_header = pd.read_excel(path, sheet_name='data_text', nrows=5)
print("Shape of header read:", df_header.shape)

# Find columns related to flag
flag_cols = [c for c in df_header.columns if 'フラグ' in str(c) or 'SC' in str(c)]
print("Flag cols in columns:", flag_cols)

# Also check row values in case row 0 is header
for c in df_header.columns:
    val_set = set(df_header[c].dropna().astype(str).tolist())
    if any('本調査終了' in v or 'SC終了' in v for v in val_set):
        print(f"Col {c} has flag values: {val_set}")


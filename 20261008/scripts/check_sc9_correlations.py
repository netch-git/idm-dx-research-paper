import pandas as pd
import numpy as np

excel_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"
df_raw = pd.read_excel(excel_path, sheet_name="data", header=0)
df_data = df_raw.iloc[1:].copy()
df_main = df_data[df_data['Q1'].notna()].copy()

sc9_cols = [f"SC9.{i}" for i in range(1, 11)]
df_sc9 = df_main[sc9_cols].apply(pd.to_numeric)

# Note: raw codes: 1=非常に当てはまる ... 5=全く当てはまらない
# If we convert to 5-point agreement score (agree=5, disagree=1): 6 - raw
df_sc9_agree = 6 - df_sc9

corr_matrix = df_sc9_agree.corr()
print("Correlation Matrix (Agree scores, 5=Strongly Agree):")
print(corr_matrix.round(2))

# Check item means
means = df_sc9_agree.mean().round(2)
print("\nMeans (Agree scores):")
for col, m in means.items():
    print(f"{col}: {m}")

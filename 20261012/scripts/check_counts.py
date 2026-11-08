import pandas as pd
import numpy as np

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'

print("Loading data_text sheet...")
df = pd.read_excel(path, sheet_name='data_text', header=0)
print(f"Total rows (including question text row): {len(df)}")

# Row 0 is question label in japanese
q_labels = df.iloc[0]
df_data = df.iloc[1:].copy()
print(f"Data rows: {len(df_data)}")

# Check SC_MAIN values
flag_counts = df_data['SC_MAIN'].value_counts(dropna=False)
print("\n--- SC_MAIN counts ---")
print(flag_counts)

# Let's save column names and question labels to a reference file
summary_cols = []
for col in df.columns:
    summary_cols.append({
        'col_id': col,
        'label': str(q_labels[col])[:50]
    })
pd.DataFrame(summary_cols).to_csv(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\columns_reference.csv', index=False, encoding='utf-8-sig')
print("\nColumns saved to columns_reference.csv")

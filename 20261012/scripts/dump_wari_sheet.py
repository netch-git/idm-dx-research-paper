import openpyxl
import pandas as pd

path = r'G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx'
wb = openpyxl.load_workbook(path, data_only=True)
sheet_names = wb.sheetnames
ws_wari = wb[sheet_names[3]] # 割付 sheet

rows = []
for r in ws_wari.iter_rows(values_only=True):
    rows.append([str(x) if x is not None else "" for x in r])

df_wari = pd.DataFrame(rows)
df_wari.to_csv(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\wari_sheet_dump.csv', index=False, header=False, encoding='utf-8-sig')

# Let's inspect non-empty rows and columns
print(f"Dumped wari sheet: {df_wari.shape}")
for idx, r in df_wari.iterrows():
    vals = [v for v in r if v != ""]
    if len(vals) > 0 and idx < 30:
        print(f"Row {idx}: {vals[:10]}")

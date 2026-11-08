import openpyxl
import pandas as pd
import json
import os

excel_path = r"G:\マイドライブ\antigravity\IDM\data\ローデータ（ICT活用の調査）1125.xlsx"

# Inspect sheet 4 name accurately
wb = openpyxl.load_workbook(excel_path, read_only=True)
sheet_names = wb.sheetnames
wb.close()

print(f"Sheet names raw: {[s for s in sheet_names]}")
for s in sheet_names:
    print(repr(s), [hex(ord(c)) for c in s])

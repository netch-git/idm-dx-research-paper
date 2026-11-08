import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"G:\マイドライブ\antigravity\IDM\citation\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
xl = pd.ExcelFile(excel_path)
print("Sheet names:", xl.sheet_names)

for sheet in xl.sheet_names:
    df = xl.parse(sheet)
    print(f"\n--- Sheet: {sheet} (Rows: {len(df)}, Cols: {len(df.columns)}) ---")
    print("Columns:", list(df.columns)[:10])
    if len(df) > 0:
        print("Sample row 0:")
        row_dict = df.iloc[0].dropna().to_dict()
        for k, v in list(row_dict.items())[:5]:
            print(f"  {k}: {str(v)[:60]}")

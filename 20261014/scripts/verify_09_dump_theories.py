import sys, os, pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
excel_path = r"G:\マイドライブ\antigravity\IDM\data\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
df = pd.read_excel(excel_path, "理論基盤文献＆公的白書")
print("Shape:", df.shape)
for i, row in df.iterrows():
    vals = [str(x) for x in row.values if pd.notna(x)]
    print(f"Row {i:2d}:", " | ".join(vals[:4]))

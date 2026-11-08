import sys, os, pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
REF_XLSX = r"G:\マイドライブ\antigravity\IDM\data\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"

xl = pd.ExcelFile(REF_XLSX)
for s in xl.sheet_names:
    df = pd.read_excel(xl, s)
    print(f"\n--- Sheet: {s} ---")
    for col in df.columns:
        vals = df[col].dropna().astype(str).tolist()
        for v in vals:
            for kw in ["Armenakis", "Herscovitch", "経済産業", "Kerzner", "Nonaka", "野中", "Pfeffer", "Rizzo", "Siemsen", "中小企業", "白書", "DXレポート"]:
                if kw.lower() in v.lower():
                    print(f"  [{s}] Col '{col}': {v[:80]}")

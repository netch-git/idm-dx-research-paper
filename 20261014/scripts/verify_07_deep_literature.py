import sys, os, pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
REF_XLSX = r"G:\マイドライブ\antigravity\IDM\data\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
MD_PATH = r"G:\マイドライブ\antigravity\IDM\20261014\reports\20261014_学術論文ドラフト_本文原稿_確定版.md"

xl = pd.ExcelFile(REF_XLSX)
sheets = {}
for s in xl.sheet_names:
    sheets[s] = pd.read_excel(xl, s)

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_text = f.read()

ref_idx = md_text.find("# 参考文献")
ref_section = md_text[ref_idx:]
ref_lines = [line.strip()[2:] for line in ref_section.split("\n") if line.strip().startswith("- ")]

print(f"Total manuscript refs: {len(ref_lines)}\n")

for i, ref in enumerate(ref_lines, 1):
    matched_sheets = []
    # 各シートで文字列検索
    # 検索キーとして著者のラストネームを抽出
    first_token = ref.split("(")[0].replace(",", " ").strip().split()[0]
    
    for s_name, df_s in sheets.items():
        found = False
        text_dump = df_s.astype(str).to_string()
        if first_token.lower() in text_dump.lower():
            matched_sheets.append(s_name)
            
    print(f"{i:2d}. {first_token} -> Matched in: {', '.join(matched_sheets) if matched_sheets else 'NOT FOUND'}")

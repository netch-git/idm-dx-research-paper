import sys, os, pandas as pd, re

sys.stdout.reconfigure(encoding="utf-8")
REF_XLSX = r"G:\マイドライブ\antigravity\IDM\data\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
MD_PATH = r"G:\マイドライブ\antigravity\IDM\20261014\reports\20261014_学術論文ドラフト_本文原稿_確定版.md"

xl = pd.ExcelFile(REF_XLSX)
print("Excel sheet names:", xl.sheet_names)

# 各シートの文献リストを取得
db_sheet = pd.read_excel(xl, "【全引用文献】要約和訳DB")
print(f"DB sheet rows: {len(db_sheet)}")

# 本文原稿の参考文献セクションを抽出
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_text = f.read()

ref_idx = md_text.find("# 参考文献")
ref_section = md_text[ref_idx:]
ref_lines = [line.strip()[2:] for line in ref_section.split("\n") if line.strip().startswith("- ")]
print(f"Manuscript references count: {len(ref_lines)}")

# 照合
print("\n=== Manuscript References vs Excel Verification ===")
for i, ref in enumerate(ref_lines, 1):
    # 著者名やキーとなる単語を抽出
    first_author = ref.split("(")[0].strip()
    year_match = re.search(r"\((\d{4})\)", ref)
    year = year_match.group(1) if year_match else ""
    
    # DB sheet で照合
    matched = False
    for _, row in db_sheet.iterrows():
        excel_author = str(row.get("著者名 (Authors)", ""))
        excel_year = str(row.get("発行年", ""))
        excel_title = str(row.get("文献タイトル (Title)", ""))
        
        # 簡易マッチング
        if (first_author.split(",")[0].strip().lower() in excel_author.lower() or 
            first_author.split(" ")[0].strip().lower() in excel_author.lower()) and (year in excel_year):
            matched = True
            break
            
    status = "OK (Matched in Excel DB)" if matched else "Check Details"
    print(f"{i:2d}. [{status}] {first_author} ({year})")

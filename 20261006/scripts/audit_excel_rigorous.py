import openpyxl
import json
import urllib.request
import time
import os
import sys

wb_path = r"G:\マイドライブ\antigravity\IDM\20261006\reports\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
wb = openpyxl.load_workbook(wb_path, data_only=True)
ws1 = wb.worksheets[0]

rows1 = []
for row in ws1.iter_rows(values_only=True):
    rows1.append(row)

header_idx = -1
for idx, r in enumerate(rows1):
    if r and any("No." in str(c) for c in r if c):
        header_idx = idx
        break

audit_items = []
for r in rows1[header_idx+1:]:
    if not r or not r[0]:
        continue
    item = {
        "no": r[0],
        "status": r[1],
        "citation": r[2],
        "first_author": r[3],
        "year": r[4],
        "title": r[5],
        "journal": r[6],
        "vol_page": r[7],
        "doi": r[8],
        "prestige": r[9],
        "context": r[10] if len(r) > 10 else ""
    }
    audit_items.append(item)

discrepancies = []

for item in audit_items:
    doi = str(item["doi"]).strip()
    if doi.startswith("http"):
        doi_clean = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    else:
        doi_clean = doi
    
    # URLまたはMIT Sloan等の例外処理
    if not doi_clean.startswith("10."):
        discrepancies.append({
            "no": item["no"],
            "citation": item["citation"],
            "excel_doi": doi,
            "issues": ["Non-DOI URL (Manual verification required for MIT Sloan or books)"],
            "cr_data": {}
        })
        continue

    url = f"https://api.crossref.org/works/{doi_clean}"
    req = urllib.request.Request(url, headers={"User-Agent": "IDM-Adversarial-Audit/1.0 (mailto:audit@idm-dx.org)"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            msg = data.get("message", {})
            
            cr_title = msg.get("title", [""])[0]
            cr_journal = msg.get("container-title", [""])[0]
            
            published_print = msg.get("published-print", {}).get("date-parts", [[None]])[0][0]
            published_online = msg.get("published-online", {}).get("date-parts", [[None]])[0][0]
            created_year = msg.get("created", {}).get("date-parts", [[None]])[0][0]
            issued_year = msg.get("issued", {}).get("date-parts", [[None]])[0][0]
            
            cr_vol = msg.get("volume", "")
            cr_issue = msg.get("issue", "")
            cr_page = msg.get("page", "")
            
            authors = msg.get("author", [])
            cr_authors_list = []
            for a in authors:
                family = a.get("family", "")
                given = a.get("given", "")
                if family:
                    cr_authors_list.append(f"{family}, {given[:1]}." if given else family)
            
            issues = []
            
            # 年の厳格チェック
            year_val = item["year"]
            all_years = [y for y in [published_print, published_online, issued_year, created_year] if y is not None]
            if year_val not in all_years:
                issues.append(f"CRITICAL: Year {year_val} not in Crossref dates (print={published_print}, online={published_online}, issued={issued_year})")
            elif published_print and published_online and published_print != published_online:
                issues.append(f"NOTE: Published online in {published_online}, print volume in {published_print}. (Excel has {year_val})")

            # 著者名のチェック
            if cr_authors_list:
                first_family = authors[0].get("family", "")
                if first_family.lower() not in str(item["first_author"]).lower() and first_family.lower() not in str(item["citation"]).lower():
                    issues.append(f"CRITICAL: First author mismatch! Excel='{item['first_author']}', Crossref='{first_family}'")

            # ジャーナル名のチェック
            j_excel = str(item["journal"]).lower().strip()
            j_cr = str(cr_journal).lower().strip()
            if j_cr and j_cr not in j_excel and j_excel not in j_cr:
                issues.append(f"WARNING: Journal name discrepancy: Excel='{item['journal']}' vs Crossref='{cr_journal}'")

            discrepancies.append({
                "no": item["no"],
                "citation": item["citation"],
                "excel_doi": doi,
                "issues": issues,
                "cr_data": {
                    "title": cr_title,
                    "journal": cr_journal,
                    "published_print": published_print,
                    "published_online": published_online,
                    "issued": issued_year,
                    "volume": cr_vol,
                    "issue": cr_issue,
                    "page": cr_page,
                    "authors": cr_authors_list
                }
            })
    except Exception as e:
        discrepancies.append({
            "no": item["no"],
            "citation": item["citation"],
            "excel_doi": doi,
            "issues": [f"API Error: {e}"],
            "cr_data": {}
        })
    time.sleep(0.2)

out_audit_json = r"G:\マイドライブ\antigravity\IDM\20261006\artifacts\adversarial_audit_results.json"
os.makedirs(os.path.dirname(out_audit_json), exist_ok=True)
with open(out_audit_json, "w", encoding="utf-8") as f:
    json.dump(discrepancies, f, ensure_ascii=False, indent=2)

print(f"Audit completed for {len(discrepancies)} items. Saved to {out_audit_json}")
for d in discrepancies:
    print(f"[{d['no']}] Issues count: {len(d['issues'])}")
    for iss in d['issues']:
        print(f"    - {iss}")

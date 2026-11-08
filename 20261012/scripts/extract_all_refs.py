# -*- coding: utf-8 -*-
"""
Excelの全シート＋section_refs.pyから全文献を統合リスト化するスクリプト
"""
import openpyxl
import re

excel_path = r'G:\マイドライブ\antigravity\IDM\data\IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx'
wb = openpyxl.load_workbook(excel_path)

refs_master = {}

def normalize_title(title):
    if not title: return ""
    t = re.sub(r'[\s\-_:–—\.,\?]+', ' ', title).strip().lower()
    return t

# 1. 各シートから抽出
for sname in wb.sheetnames:
    if sname == '文献照合マニュアル': continue
    ws = wb[sname]
    header_row = 1
    for r in range(1, 4):
        vals = [ws.cell(r, c).value for c in range(1, ws.max_column+1)]
        if any('タイトル' in str(v) or 'タイトル' in str(v) for v in vals if v):
            header_row = r
            break
    headers = [str(ws.cell(header_row, c).value).strip() if ws.cell(header_row, c).value else '' for c in range(1, ws.max_column+1)]
    
    t_idx = -1; d_idx = -1; a_idx = -1; y_idx = -1; j_idx = -1; c_idx = -1
    for idx, h in enumerate(headers):
        if 'タイトル' in h or 'レポート名' in h: t_idx = idx + 1
        elif 'DOI' in h or 'DLリンク' in h: d_idx = idx + 1
        elif '著者' in h or '機関' in h: a_idx = idx + 1
        elif '年' in h: y_idx = idx + 1
        elif 'ジャーナル' in h or '出版' in h or '掲載' in h: j_idx = idx + 1
        elif '区分' in h or '格付け' in h or '位置づけ' in h: c_idx = idx + 1
        
    for r in range(header_row + 1, ws.max_row + 1):
        title = ws.cell(r, t_idx).value if t_idx > 0 else None
        doi = ws.cell(r, d_idx).value if d_idx > 0 else None
        author = ws.cell(r, a_idx).value if a_idx > 0 else None
        year = ws.cell(r, y_idx).value if y_idx > 0 else None
        journal = ws.cell(r, j_idx).value if j_idx > 0 else None
        category = ws.cell(r, c_idx).value if c_idx > 0 else None
        
        if title:
            norm_t = normalize_title(str(title))
            if norm_t not in refs_master:
                refs_master[norm_t] = {
                    'title': str(title).strip(),
                    'doi': str(doi).strip() if doi else '',
                    'author': str(author).strip() if author else '',
                    'year': str(year).strip() if year else '',
                    'journal': str(journal).strip() if journal else '',
                    'category': str(category).strip() if category else '',
                    'sources': [sname]
                }
            else:
                refs_master[norm_t]['sources'].append(sname)
                if not refs_master[norm_t]['doi'] and doi: refs_master[norm_t]['doi'] = str(doi).strip()
                if not refs_master[norm_t]['author'] and author: refs_master[norm_t]['author'] = str(author).strip()
                if not refs_master[norm_t]['year'] and year: refs_master[norm_t]['year'] = str(year).strip()
                if not refs_master[norm_t]['journal'] and journal: refs_master[norm_t]['journal'] = str(journal).strip()

print(f"Total extracted from Excel: {len(refs_master)}")

# 2. section_refs.py からも追加抽出
with open(r'G:\マイドライブ\antigravity\IDM\20261012\scripts\section_refs.py', 'r', encoding='utf-8') as f:
    text = f.read()

# ref-item からパース
items = re.findall(r'<p class="ref-item">(.*?)</p>', text, re.DOTALL)
print(f"Items in section_refs.py: {len(items)}")

for item in items:
    clean = re.sub(r'<[^>]+>', '', item).strip()
    # e.g., Adams, J. S. (1965). Inequity in social exchange. In ... https://doi...
    m = re.match(r'^(.*?)\s*\((\d{4}[a-z]?)\)\.\s*(.*?)\.\s*(.*)$', clean)
    if m:
        author = m.group(1).strip()
        year = m.group(2).strip()
        rest_title = m.group(3).strip()
        rest_pub = m.group(4).strip()
        doi_m = re.search(r'https?://[^\s]+', rest_pub)
        doi = doi_m.group(0) if doi_m else ""
        norm_t = normalize_title(rest_title)
        
        # 既存チェック
        matched = False
        for k in refs_master:
            if norm_t in k or k in norm_t or (len(norm_t) > 10 and norm_t[:20] in k):
                refs_master[k]['sources'].append('section_refs.py')
                matched = True
                break
        if not matched:
            refs_master[norm_t] = {
                'title': rest_title,
                'doi': doi,
                'author': author,
                'year': year,
                'journal': rest_pub,
                'category': '投稿論文引用文献 (最新版)',
                'sources': ['section_refs.py']
            }

print(f"Total unified unique refs: {len(refs_master)}")

import json
with open(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\all_unified_refs.json', 'w', encoding='utf-8') as f:
    json.dump(list(refs_master.values()), f, ensure_ascii=False, indent=2)

print("Saved to 20261012/artifacts/all_unified_refs.json")

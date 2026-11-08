#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - 文献ファイル・引用箇所・Excel台帳 完全名寄せ＆過不足監査スクリプト
"""

import os
import sys
import json
import re
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"G:\マイドライブ\antigravity\IDM")
CITATION_DIR = BASE_DIR / "citation"
PAPERS_20261004 = BASE_DIR / "20261004" / "papers_pdf"
PAPERS_20261009 = BASE_DIR / "20261009" / "papers_pdf"
PAPERS_20261028 = BASE_DIR / "20261028" / "papers_pdf"
EXCEL_PATH = CITATION_DIR / "IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"

# 論文確定版Markdown（20261014/reports/確定版_3.md または 20261008）
DRAFT_MD_PATH = BASE_DIR / "20261014" / "reports" / "20261014_学術論文ドラフト_本文_確定版_3.md"
if not DRAFT_MD_PATH.exists():
    # 候補を探す
    for p in BASE_DIR.rglob("*確定版*.md"):
        if "本文" in p.name:
            DRAFT_MD_PATH = p
            break

print(f"Using draft paper: {DRAFT_MD_PATH}")

with open(DRAFT_MD_PATH, 'r', encoding='utf-8') as f:
    draft_text = f.read()

# 本文末尾の参考文献セクションを抽出
ref_sec_start = draft_text.find("## 参考文献")
if ref_sec_start == -1:
    ref_sec_start = draft_text.find("## 7. 参考文献")

ref_sec_text = draft_text[ref_sec_start:] if ref_sec_start != -1 else ""

# 24編のリスト
DRAFT_24_KEYS = [
    "Adams (1965)",
    "Aiken & West (1991)",
    "Armenakis et al. (1993)",
    "Balogun & Johnson (2004)",
    "Besson & Rowe (2012)",
    "Colquitt (2001)",
    "Dean et al. (1998)",
    "Festinger (1957)",
    "Folger (1977)",
    "Greenberg (1990)",
    "Herscovitch & Meyer (2002)",
    "Huy (2002)",
    "IPA (2023)",
    "Kane et al. (2015)",
    "経済産業省 (2018)",
    "Kerzner (2018)",
    "Leventhal (1980)",
    "Nonaka & Takeuchi (1995)",
    "Pfeffer & Salancik (1978)",
    "Rizzo et al. (1970)",
    "Siemsen et al. (2010)",
    "中小企業庁 (2022)",
    "Thibaut & Walker (1975)",
    "Vial (2019)"
]

# 本文中の出現箇所カウント
results = []
for k in DRAFT_24_KEYS:
    # 簡易キー（著者名のみ、または短縮）
    author_main = k.split()[0].replace("&", "").strip()
    count_in_draft = draft_text.count(k)
    # 参考文献セクション以外でのカウント
    body_text_only = draft_text[:ref_sec_start]
    count_in_body = body_text_only.count(k)
    
    # 本文のどの章にあるか
    chapters = []
    for ch_num in range(1, 7):
        ch_marker = f"# 第{ch_num}章"
        next_marker = f"# 第{ch_num+1}章" if ch_num < 6 else "## 参考文献"
        p1 = body_text_only.find(ch_marker)
        p2 = body_text_only.find(next_marker)
        if p1 != -1:
            ch_sub = body_text_only[p1:p2] if p2 != -1 else body_text_only[p1:]
            if k in ch_sub or author_main in ch_sub:
                chapters.append(f"第{ch_num}章")
                
    results.append({
        "key": k,
        "body_mentions": count_in_body,
        "chapters": chapters,
        "in_ref_list": k in ref_sec_text
    })

print(f"Audited {len(results)} references against draft paper.")
for r in results[:10]:
    print(r)

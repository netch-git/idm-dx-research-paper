#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - 文献名寄せ＆過不足マッピング完全照合スクリプト
"""

import os
import sys
import json
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"G:\マイドライブ\antigravity\IDM")
CITATION_DIR = BASE_DIR / "citation"
EXCEL_PATH = CITATION_DIR / "IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"

# 全PDFファイルのインデックス作成
all_pdfs = {}
for p in BASE_DIR.rglob("*.pdf"):
    # figures や presentation は除外
    if "figures" in str(p) or "発表資料" in str(p):
        continue
    rel_path = str(p.relative_to(BASE_DIR)).replace("\\", "/")
    all_pdfs[p.name] = {
        "rel_path": rel_path,
        "size_kb": round(p.stat().st_size / 1024, 1),
        "parent": p.parent.name
    }

print(f"Total relevant PDFs indexed: {len(all_pdfs)}")

# 本文引用24編の定義と手元ファイル探索
REF_24 = [
    {"id": "REF-01", "key": "Adams (1965)", "author": "Adams, J. S.", "year": 1965, "type": "論文 (Journal)", "title": "Inequity in social exchange"},
    {"id": "REF-02", "key": "Aiken & West (1991)", "author": "Aiken, L. S., & West, S. G.", "year": 1991, "type": "書籍 (Book)", "title": "Multiple regression: Testing and interpreting interactions"},
    {"id": "REF-03", "key": "Armenakis et al. (1993)", "author": "Armenakis, A. A., et al.", "year": 1993, "type": "論文 (Journal)", "title": "Creating readiness for organizational change"},
    {"id": "REF-04", "key": "Balogun & Johnson (2004)", "author": "Balogun, J., & Johnson, G.", "year": 2004, "type": "論文 (Journal)", "title": "Organizational restructuring and middle manager sensemaking"},
    {"id": "REF-05", "key": "Besson & Rowe (2012)", "author": "Besson, P., & Rowe, F.", "year": 2012, "type": "論文 (Journal)", "title": "Strategizing information systems-enabled organizational transformation"},
    {"id": "REF-06", "key": "Colquitt (2001)", "author": "Colquitt, J. A.", "year": 2001, "type": "論文 (Journal)", "title": "On the dimensionality of organizational justice"},
    {"id": "REF-07", "key": "Dean et al. (1998)", "author": "Dean, J. W., et al.", "year": 1998, "type": "論文 (Journal)", "title": "Organizational cynicism"},
    {"id": "REF-08", "key": "Festinger (1957)", "author": "Festinger, L.", "year": 1957, "type": "書籍 (Book)", "title": "A theory of cognitive dissonance"},
    {"id": "REF-09", "key": "Folger (1977)", "author": "Folger, R.", "year": 1977, "type": "論文 (Journal)", "title": "Distributive and procedural justice: Combined impact of voice"},
    {"id": "REF-10", "key": "Greenberg (1990)", "author": "Greenberg, J.", "year": 1990, "type": "論文 (Journal)", "title": "Organizational justice: Yesterday, today, and tomorrow"},
    {"id": "REF-11", "key": "Herscovitch & Meyer (2002)", "author": "Herscovitch, L., & Meyer, J. P.", "year": 2002, "type": "論文 (Journal)", "title": "Commitment to organizational change: Extension of a three-component model"},
    {"id": "REF-12", "key": "Huy (2002)", "author": "Huy, Q. N.", "year": 2002, "type": "論文 (Journal)", "title": "Emotional balancing of organizational continuity and radical change"},
    {"id": "REF-13", "key": "IPA (2023)", "author": "情報処理推進機構 (IPA)", "year": 2023, "type": "公的白書 (Report)", "title": "DX白書2023：進む変革、進まぬ変革"},
    {"id": "REF-14", "key": "Kane et al. (2015)", "author": "Kane, G. C., et al.", "year": 2015, "type": "調査報告 (Report)", "title": "Strategy, not technology, drives digital transformation"},
    {"id": "REF-15", "key": "経済産業省 (2018)", "author": "経済産業省", "year": 2018, "type": "公的白書 (Report)", "title": "DXレポート：ITシステム「2025年の崖」克服とDXの本格的な展開"},
    {"id": "REF-16", "key": "Kerzner (2018)", "author": "Kerzner, H.", "year": 2018, "type": "書籍 (Book)", "title": "Project management best practices: Achieving global excellence"},
    {"id": "REF-17", "key": "Leventhal (1980)", "author": "Leventhal, G. S.", "year": 1980, "type": "書籍の章 (Book Chapter)", "title": "What should be done with equity theory?"},
    {"id": "REF-18", "key": "Nonaka & Takeuchi (1995)", "author": "Nonaka, I., & Takeuchi, H.", "year": 1995, "type": "書籍 (Book)", "title": "The knowledge-creating company"},
    {"id": "REF-19", "key": "Pfeffer & Salancik (1978)", "author": "Pfeffer, J., & Salancik, G. R.", "year": 1978, "type": "書籍 (Book)", "title": "The external control of organizations"},
    {"id": "REF-20", "key": "Rizzo et al. (1970)", "author": "Rizzo, J. R., et al.", "year": 1970, "type": "論文 (Journal)", "title": "Role conflict and ambiguity in complex organizations"},
    {"id": "REF-21", "key": "Siemsen et al. (2010)", "author": "Siemsen, E., et al.", "year": 2010, "type": "論文 (Journal)", "title": "Common method bias in regression models"},
    {"id": "REF-22", "key": "中小企業庁 (2022)", "author": "中小企業庁", "year": 2022, "type": "公的白書 (Report)", "title": "中小企業白書2022年版：新たな時代を切り拓く中小企業"},
    {"id": "REF-23", "key": "Thibaut & Walker (1975)", "author": "Thibaut, J. W., & Walker, L.", "year": 1975, "type": "書籍 (Book)", "title": "Procedural justice: A psychological analysis"},
    {"id": "REF-24", "key": "Vial (2019)", "author": "Vial, G.", "year": 2019, "type": "論文 (Journal)", "title": "Understanding digital transformation: A review and a research agenda"}
]

# 本文確定版の読込
DRAFT_MD_PATH = BASE_DIR / "20261014" / "reports" / "20261014_学術論文ドラフト_本文原稿_確定版.md"
with open(DRAFT_MD_PATH, 'r', encoding='utf-8') as f:
    draft_text = f.read()

# 各文献のファイル照合
for r in REF_24:
    matched_files = []
    author_last = r["author"].split(",")[0].split()[0]
    # ファイル名探索
    for fname, finfo in all_pdfs.items():
        # 著者名やキーワードで照合
        if author_last.lower() in fname.lower() and (str(r["year"]) in fname or len(author_last) > 4):
            matched_files.append(finfo["rel_path"])
        elif "ipa" in author_last.lower() and "ipa" in fname.lower():
            matched_files.append(finfo["rel_path"])
        elif "経済産業省" in author_last and "経済産業省" in fname:
            matched_files.append(finfo["rel_path"])
            
    r["matched_files"] = list(set(matched_files))
    
    # 本文出現チェック
    mentions = []
    # 英語表記・日本語表記
    patterns = [
        r["key"],
        f"{author_last} ({r['year']})",
        f"{author_last}（{r['year']}）",
        f"{author_last}, {r['year']}",
        f"{author_last} et al., {r['year']}",
        f"{author_last} et al. ({r['year']})"
    ]
    if "IPA" in r["key"]:
        patterns.extend(["IPA (2023)", "IPA（2023）", "情報処理推進機構（2023）", "情報処理推進機構 (2023)"])
    if "経済産業省" in r["key"]:
        patterns.extend(["経済産業省（2018）", "経済産業省 (2018)", "経産省（2018）"])
    if "中小企業庁" in r["key"]:
        patterns.extend(["中小企業庁（2022）", "中小企業庁 (2022)"])

    found_count = 0
    for pat in patterns:
        found_count += draft_text.count(pat)
        
    r["citation_count"] = found_count

print("\n=== 本文引用24編の照合結果 ===")
for r in REF_24:
    status = "✅ PDFあり" if r["matched_files"] else ("📖 書籍/未取得" if r["type"] == "書籍 (Book)" else "⚠️ PDF未配置")
    print(f"{r['id']} | {r['key']} | {r['type']} | 本文出現: {r['citation_count']}回 | 状態: {status} | Files: {r['matched_files'][:1]}")

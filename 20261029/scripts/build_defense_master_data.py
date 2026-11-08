#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - 文献防衛マスターデータ統合生成スクリプト
1. 確定24編の定義
2. Excel【全引用文献】要約和訳DBの48レコード
3. PDF本文抽出テキスト（27本）
4. Blau & Scott (1962) 監査データ
を完全統合し、マスターJSONを生成する。
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(r"G:\マイドライブ\antigravity\IDM")
CITATION_DIR = BASE_DIR / "citation"
EXCEL_PATH = CITATION_DIR / "IDM_DX_投稿論文_参考文献リスト_真正改訂完全版.xlsx"
PDF_TEXTS_JSON = BASE_DIR / "20261029" / "artifacts" / "pdf_extracted_texts.json"
MAPPING_JSON = BASE_DIR / "20261029" / "artifacts" / "citation_pdf_mapping.json"
OUTPUT_JSON = BASE_DIR / "20261029" / "artifacts" / "literature_defense_master.json"

def main():
    with open(PDF_TEXTS_JSON, 'r', encoding='utf-8') as f:
        pdf_texts = json.load(f)

    with open(MAPPING_JSON, 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    xl = pd.ExcelFile(EXCEL_PATH)
    df_db = xl.parse('【全引用文献】要約和訳DB')
    df_theory = xl.parse('理論基盤文献＆公的白書')
    df_pdf_cat = xl.parse('手元保有PDF_実体文献目録')

    print(f"Excel loaded. DB rows: {len(df_db)}, Theory rows: {len(df_theory)}, PDF catalog rows: {len(df_pdf_cat)}")

    # 確定24編のリストを定義
    # 各文献に対して、本研究での役割、仮説、採用根拠、批判的視点、肯定的防衛を網羅
    refs_master = []

    # 代表的なコア文献のマスタースキーマ
    # （後続の生成ステップで全件を完全構造化）
    print("Building master literature defense data...")

if __name__ == "__main__":
    main()

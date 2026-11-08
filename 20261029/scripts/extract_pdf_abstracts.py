#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDM Project - citation フォルダ内 PDF 本文抽出スクリプト（トークン節約型）
各PDFの先頭数ページ（Abstract, Introduction, Method）から
テキストを抽出し、構造化サマリーを生成する。
"""

import os
import sys
import json
import pdfplumber
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CITATION_DIR = Path(r"G:\マイドライブ\antigravity\IDM\citation")
OUTPUT_JSON = Path(r"G:\マイドライブ\antigravity\IDM\20261029\artifacts\pdf_extracted_texts.json")

def extract_pdf_core_text(pdf_path: Path) -> dict:
    info = {
        'filename': pdf_path.name,
        'filesize_kb': round(pdf_path.stat().st_size / 1024, 1),
        'total_pages': 0,
        'first_pages_text': '',
        'abstract_snippet': '',
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            info['total_pages'] = len(pdf.pages)
            # 最初の1〜3ページからテキストを抽出（Abstractや導入部）
            extracted_text = []
            for p_num in range(min(3, len(pdf.pages))):
                text = pdf.pages[p_num].extract_text()
                if text:
                    extracted_text.append(text)
            
            combined = "\n".join(extracted_text)
            info['first_pages_text'] = combined[:4000] # トークン節約のため4000文字以内
            
            # Abstract の探索
            lower_text = combined.lower()
            abs_idx = lower_text.find("abstract")
            if abs_idx != -1:
                info['abstract_snippet'] = combined[abs_idx:abs_idx+1500].strip()
            else:
                info['abstract_snippet'] = combined[:1500].strip()
                
    except Exception as e:
        info['error'] = str(e)
        
    return info

def main():
    pdf_files = sorted([f for f in CITATION_DIR.glob("*.pdf")])
    print(f"抽出対象 PDF: {len(pdf_files)} 件")
    
    results = {}
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] 解析中: {pdf_path.name} ...")
        res = extract_pdf_core_text(pdf_path)
        results[pdf_path.name] = res
        
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"\n全 {len(pdf_files)} 件のPDF本文抽出完了: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()

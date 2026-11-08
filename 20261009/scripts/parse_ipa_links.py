# -*- coding: utf-8 -*-
import os
import sys
import re
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

DEST_DIR = r"G:\マイドライブ\antigravity\IDM\20261009\papers_pdf"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml,application/pdf;q=0.9,*/*;q=0.8"
}

# 1. IPA 2023 解析
ipa_html_path = r"C:\Users\kynet\.gemini\antigravity\brain\8e2eb12e-e27d-4799-9a6e-94cc4172ade7\.system_generated\steps\176\content.md"
with open(ipa_html_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
print("=== IPA 2023 PDF Links ===")
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.endswith(".pdf"):
        text = a.get_text(strip=True)
        print(f"{href} -> {text}")
        # 全編一括ダウンロードリンクを探す
        full_url = urllib.parse.urljoin("https://www.ipa.go.jp/publish/wp-dx/dx-2023.html", href)
        if "全編" in text or "一括" in text:
            print(f"  Target Full PDF Found: {full_url}")
            dest_file = os.path.join(DEST_DIR, "IPA_2023_DX白書2023_全編一括.pdf")
            try:
                req = urllib.request.Request(full_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = resp.read()
                    with open(dest_file, "wb") as out:
                        out.write(data)
                print(f"  Downloaded Full PDF: {len(data):,} bytes")
            except Exception as e:
                print(f"  Failed: {e}")

# -*- coding: utf-8 -*-
"""
find_and_download_pdfs.py
IPA2023, 中小機構2024, 学術論文のOAリポジトリPDFを自動ダウンロードするスクリプト
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

DEST_DIR = r"G:\マイドライブ\antigravity\IDM\20261009\papers_pdf"
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml,application/pdf;q=0.9,*/*;q=0.8"
}

def download_file(url, dest_path, min_size=50000):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()
            if len(data) < min_size:
                print(f"  [WARN] Downloaded size too small ({len(data)} bytes) from {url}")
                return False
            # PDFマジックナンバーチェック
            if not data.startswith(b"%PDF"):
                print(f"  [WARN] Content does not start with %PDF from {url} (Content-Type: {content_type})")
                return False
            with open(dest_path, "wb") as f:
                f.write(data)
            print(f"  [SUCCESS] Saved {len(data):,} bytes to {os.path.basename(dest_path)}")
            return True
    except Exception as e:
        print(f"  [FAIL] Error downloading {url}: {e}")
        return False

# 1. IPA 2023白書のPDF URL探索
print("=== 1. Checking IPA 2023 ===")
ipa_html_path = r"C:\Users\kynet\.gemini\antigravity\brain\8e2eb12e-e27d-4799-9a6e-94cc4172ade7\.system_generated\steps\176\content.md"
if os.path.exists(ipa_html_path):
    with open(ipa_html_path, "r", encoding="utf-8") as f:
        html = f.read()
    pdf_matches = re.findall(r'href=[\"\']([^\"\']+\.pdf)[\"\']', html, re.I)
    print(f"Found {len(pdf_matches)} PDF links in IPA page:")
    for p in set(pdf_matches):
        print(" ", p)
        # 本編・全編のPDFを探す
        full_url = urllib.parse.urljoin("https://www.ipa.go.jp/publish/wp-dx/dx-2023.html", p)
        if "all" in p.lower() or "dx-2023" in p.lower() or "full" in p.lower() or "honpen" in p.lower() or "hakusho" in p.lower():
            target_dest = os.path.join(DEST_DIR, "IPA_2023_DX白書2023_本編.pdf")
            if download_file(full_url, target_dest):
                break
    else:
        # 見つからなかった場合、最初の大きなPDFを試す
        for p in set(pdf_matches):
            full_url = urllib.parse.urljoin("https://www.ipa.go.jp/publish/wp-dx/dx-2023.html", p)
            target_dest = os.path.join(DEST_DIR, f"IPA_2023_{os.path.basename(p)}")
            if download_file(full_url, target_dest):
                break

# 2. 中小機構 2024調査報告書の探索
print("\n=== 2. Checking SMRJ 2024 ===")
smrj_page_url = "https://www.smrj.go.jp/research_report/survey/entrepreneur/index.html"
try:
    req = urllib.request.Request(smrj_page_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        smrj_html = resp.read().decode("utf-8", errors="ignore")
    smrj_pdfs = re.findall(r'href=[\"\']([^\"\']+\.pdf)[\"\']', smrj_html, re.I)
    print(f"Found {len(smrj_pdfs)} PDF links in SMRJ page:")
    for p in set(smrj_pdfs):
        if "dx" in p.lower() or "2024" in p or "r06" in p:
            print("  Candidate:", p)
            full_url = urllib.parse.urljoin(smrj_page_url, p)
            target_dest = os.path.join(DEST_DIR, "中小機構_2024_中小企業のDX推進に関する調査報告書.pdf")
            if download_file(full_url, target_dest):
                break
except Exception as e:
    print(f"Error checking SMRJ page: {e}")

# 3. Kane et al. 2015 Deloitte/MIT SMR レポート探索
print("\n=== 3. Checking Kane et al. 2015 ===")
kane_candidates = [
    "https://sloanreview.mit.edu/wp-content/uploads/2015/07/MIT-SMR-Deloitte-Digital-Transformation-2015.pdf",
    "https://www2.deloitte.com/content/dam/Deloitte/cn/Documents/technology-media-telecommunications/deloitte-cn-tmt-strategy-not-technology-drives-digital-transformation-en-150714.pdf",
    "https://www.alnap.org/system/files/content/resource/files/main/mit-smr-deloitte-digital-transformation-2015.pdf"
]
for url in kane_candidates:
    dest = os.path.join(DEST_DIR, "Kane_2015_Strategy_not_technology_drives_digital_transformation.pdf")
    if download_file(url, dest):
        break

# 4. Huy (2002)
print("\n=== 4. Checking Huy 2002 ===")
huy_candidates = [
    "https://flora.insead.edu/fichiersti_wp/inseadwp2001/2001-38ob.pdf",
    "https://flora.insead.edu/fichiersti_wp/inseadwp2000/2000-88ob.pdf",
    "https://flora.insead.edu/fichiersti_wp/inseadwp2001/2001-38.pdf"
]
for url in huy_candidates:
    dest = os.path.join(DEST_DIR, "Huy_2002_Emotional_Balancing.pdf")
    if download_file(url, dest):
        break

# 5. Pierce et al. (2001)
print("\n=== 5. Checking Pierce et al. 2001 ===")
pierce_candidates = [
    "https://www.researchgate.net/profile/Jon-Pierce/publication/228148858_Toward_a_Theory_of_Psychological_Ownership_in_Organizations/links/00b7d519b7a4855fe1000000/Toward-a-Theory-of-Psychological-Ownership-in-Organizations.pdf",
    "https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=10.1.1.464.7171"
]
for url in pierce_candidates:
    dest = os.path.join(DEST_DIR, "Pierce_2001_Psychological_Ownership.pdf")
    if download_file(url, dest):
        break

# 6. Teece (2007)
print("\n=== 6. Checking Teece 2007 ===")
teece_candidates = [
    "https://www.business.rutgers.edu/sites/default/files/images/faculty/Teece%202007%20SMJ.pdf",
    "https://www.researchgate.net/profile/David-Teece/publication/227633282_Explicating_Dynamic_Capabilities_The_Nature_and_Microfoundations_of_Sustainable_Enterprise_Performance/links/00b4952d7e5bcf279b000000/Explicating-Dynamic-Capabilities-The-Nature-and-Microfoundations-of-Sustainable-Enterprise-Performance.pdf"
]
for url in teece_candidates:
    dest = os.path.join(DEST_DIR, "Teece_2007_Explicating_Dynamic_Capabilities.pdf")
    if download_file(url, dest):
        break

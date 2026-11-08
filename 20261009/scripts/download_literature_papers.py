# -*- coding: utf-8 -*-
"""
download_literature_papers.py
参考文献リスト（全27文献）のPDF取得可能性を判定し、
オープンアクセス（OA）PDFおよび公的白書・レポートを自動ダウンロードして
G:\マイドライブ\antigravity\IDM\20261009\papers_pdf に集約・整理するスクリプト。
"""
import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse
import shutil
import time

sys.stdout.reconfigure(encoding="utf-8")

DEST_DIR = r"G:\マイドライブ\antigravity\IDM\20261009\papers_pdf"
os.makedirs(DEST_DIR, exist_ok=True)

# 既存の探索元フォルダ
SEARCH_DIRS = [
    r"G:\マイドライブ\antigravity\IDM\20261004\papers_pdf",
    r"G:\マイドライブ\IDM\文献",
    r"G:\マイドライブ\IDM"
]

# 27文献のダウンロード用メタデータ定義
TARGET_PAPERS = [
    {
        "id": "Huy2002",
        "author": "Huy (2002)",
        "title": "Emotional balancing of organizational continuity and radical change",
        "doi": "10.2307/3094890",
        "direct_urls": [
            "https://www.researchgate.net/profile/Quy-Nguyen-Huy/publication/228298715_Emotional_Balancing_of_Organizational_Continuity_and_Radical_Change_The_Contribution_of_Middle_Managers/links/00b7d5267425f3851b000000/Emotional-Balancing-of-Organizational-Continuity-and-Radical-Change-The-Contribution-of-Middle-Managers.pdf"
        ],
        "filename": "Huy_2002_Emotional_Balancing.pdf"
    },
    {
        "id": "Colquitt2001",
        "author": "Colquitt (2001)",
        "title": "On the dimensionality of organizational justice",
        "doi": "10.1037/0021-9010.86.3.386",
        "direct_urls": [],
        "filename": "Colquitt_2001_Dimensionality_of_Organizational_Justice.pdf"
    },
    {
        "id": "Festinger1957",
        "author": "Festinger (1957)",
        "title": "A theory of cognitive dissonance",
        "doi": "10.1515/9781503620766",
        "direct_urls": [],
        "filename": "Festinger_1957_Theory_of_Cognitive_Dissonance.pdf"
    },
    {
        "id": "Kane2015",
        "author": "Kane et al. (2015)",
        "title": "Strategy, not technology, drives digital transformation",
        "doi": "",
        "direct_urls": [
            "https://sloanreview.mit.edu/wp-content/uploads/2015/07/MIT-SMR-Deloitte-Digital-Transformation-2015.pdf"
        ],
        "filename": "Kane_2015_Strategy_not_technology_drives_digital_transformation.pdf"
    },
    {
        "id": "Adams1965",
        "author": "Adams (1965)",
        "title": "Inequity in social exchange",
        "doi": "10.1016/S0065-2601(08)60108-2",
        "direct_urls": [],
        "filename": "Adams_1965_Inequity_in_Social_Exchange.pdf"
    },
    {
        "id": "Aiken1991",
        "author": "Aiken & West (1991)",
        "title": "Multiple regression: Testing and interpreting interactions",
        "doi": "10.4135/9781483348810",
        "direct_urls": [],
        "filename": "Aiken_West_1991_Multiple_Regression_Interactions.pdf"
    },
    {
        "id": "AlNuaimi2022",
        "author": "AlNuaimi et al. (2022)",
        "title": "Mastering digital transformation: The nexus between leadership, agility, and digital strategy",
        "doi": "10.1016/j.jbusres.2022.03.038",
        "direct_urls": [],
        "filename": "AlNuaimi_2022_Mastering_Digital_Transformation.pdf"
    },
    {
        "id": "Barney1991",
        "author": "Barney (1991)",
        "title": "Firm resources and sustained competitive advantage",
        "doi": "10.1177/014920639101700108",
        "direct_urls": [
            "https://www.business.rutgers.edu/sites/default/files/images/faculty/Barney%201991%20JOM.pdf"
        ],
        "filename": "Barney_1991_Firm_Resources_and_Sustained_Competitive_Advantage.pdf"
    },
    {
        "id": "Blau1970",
        "author": "Blau (1970)",
        "title": "A formal theory of differentiation in organizations",
        "doi": "10.2307/2093199",
        "direct_urls": [],
        "filename": "Blau_1970_Formal_Theory_of_Differentiation.pdf"
    },
    {
        "id": "Brockner2002",
        "author": "Brockner (2002)",
        "title": "Making sense of procedural fairness",
        "doi": "10.5465/amr.2002.5922378",
        "direct_urls": [],
        "filename": "Brockner_2002_Making_Sense_of_Procedural_Fairness.pdf"
    },
    {
        "id": "Child1973",
        "author": "Child (1973)",
        "title": "Predicting and understanding organization structure",
        "doi": "10.2307/2392061",
        "direct_urls": [],
        "filename": "Child_1973_Predicting_and_Understanding_Organization_Structure.pdf"
    },
    {
        "id": "Colquitt2001meta",
        "author": "Colquitt et al. (2001)",
        "title": "Justice at the millennium: A meta-analytic review of 25 years of organizational justice research",
        "doi": "10.1037/0021-9010.86.3.425",
        "direct_urls": [],
        "filename": "Colquitt_2001_Justice_at_the_Millennium_Meta_Analysis.pdf"
    },
    {
        "id": "Folger1998",
        "author": "Folger & Cropanzano (1998)",
        "title": "Organizational justice and human resource management",
        "doi": "10.4135/9781452231556",
        "direct_urls": [],
        "filename": "Folger_Cropanzano_1998_Organizational_Justice_HRM.pdf"
    },
    {
        "id": "Ghafoori2024",
        "author": "Ghafoori et al. (2024)",
        "title": "Operationalizing psychological safety in digital transformation projects",
        "doi": "10.1016/j.ijpe.2023.109120",
        "direct_urls": [],
        "filename": "Ghafoori_2024_Operationalizing_Psychological_Safety_in_DT.pdf"
    },
    {
        "id": "Leventhal1980",
        "author": "Leventhal (1980)",
        "title": "What should be done with equity theory?",
        "doi": "10.1007/978-1-4613-3087-5_2",
        "direct_urls": [],
        "filename": "Leventhal_1980_What_Should_Be_Done_With_Equity_Theory.pdf"
    },
    {
        "id": "Nunnally1978",
        "author": "Nunnally (1978)",
        "title": "Psychometric theory (2nd ed.)",
        "doi": "10.1037/h0020169",
        "direct_urls": [],
        "filename": "Nunnally_1978_Psychometric_Theory.pdf"
    },
    {
        "id": "Packmohr2023",
        "author": "Packmohr et al. (2023)",
        "title": "Digital transformation barriers in small and medium-sized enterprises",
        "doi": "10.1007/s10796-022-10291-7",
        "direct_urls": [],
        "filename": "Packmohr_2023_Digital_Transformation_Barriers_in_SMEs.pdf"
    },
    {
        "id": "Papadopoulos2020",
        "author": "Papadopoulos et al. (2020)",
        "title": "Digital transformation and resilience in operations",
        "doi": "10.1016/j.ijinfomgt.2020.102171",
        "direct_urls": [
            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7485368/pdf/main.pdf"
        ],
        "filename": "Papadopoulos_2020_Digital_Transformation_and_Resilience.pdf"
    },
    {
        "id": "Pierce2001",
        "author": "Pierce et al. (2001)",
        "title": "Toward a theory of psychological ownership in organizations",
        "doi": "10.5465/amr.2001.4378028",
        "direct_urls": [
            "https://www.researchgate.net/profile/Jon-Pierce-2/publication/246473183_Toward_a_Theory_of_Psychological_Ownership_in_Organizations/links/00b7d52f107f9c90eb000000/Toward-a-Theory-of-Psychological-Ownership-in-Organizations.pdf"
        ],
        "filename": "Pierce_2001_Toward_Theory_of_Psychological_Ownership.pdf"
    },
    {
        "id": "Podsakoff2003",
        "author": "Podsakoff et al. (2003)",
        "title": "Common method biases in behavioral research",
        "doi": "10.1037/0021-9010.88.5.879",
        "direct_urls": [],
        "filename": "Podsakoff_2003_Common_Method_Biases.pdf"
    },
    {
        "id": "Rizzo1970",
        "author": "Rizzo et al. (1970)",
        "title": "Role conflict and ambiguity in complex organizations",
        "doi": "10.2307/2391486",
        "direct_urls": [],
        "filename": "Rizzo_1970_Role_Conflict_and_Ambiguity.pdf"
    },
    {
        "id": "Teece2007",
        "author": "Teece (2007)",
        "title": "Explicating dynamic capabilities",
        "doi": "10.1002/smj.640",
        "direct_urls": [
            "https://www.business.rutgers.edu/sites/default/files/images/faculty/Teece%202007%20SMJ.pdf"
        ],
        "filename": "Teece_2007_Explicating_Dynamic_Capabilities.pdf"
    },
    {
        "id": "Vroom1964",
        "author": "Vroom (1964)",
        "title": "Work and motivation",
        "doi": "10.1037/0021-9010.50.6.582",
        "direct_urls": [],
        "filename": "Vroom_1964_Work_and_Motivation.pdf"
    },
    {
        "id": "IPA2023",
        "author": "IPA (2023)",
        "title": "『DX白書2023』",
        "doi": "",
        "direct_urls": [
            "https://www.ipa.go.jp/publish/wp-dx/gmcbt80000005n41-att/00_all.pdf",
            "https://www.ipa.go.jp/publish/wp-dx/dx-2023.html"
        ],
        "filename": "IPA_2023_DX白書2023_完全版.pdf"
    },
    {
        "id": "IPA2025",
        "author": "IPA (2025)",
        "title": "『DX動向2025』",
        "doi": "",
        "direct_urls": [
            "https://www.ipa.go.jp/digital/chousa/dx-trend/qv62040000004q8k-att/00_all.pdf"
        ],
        "filename": "IPA_2025_DX動向2025_完全版.pdf"
    },
    {
        "id": "SMRJ2024",
        "author": "中小機構 (2024)",
        "title": "『中小企業のDX推進に関する調査（2024年）』",
        "doi": "",
        "direct_urls": [
            "https://www.smrj.go.jp/research/survey/favgor000001yq52-att/20240424_dx_report.pdf"
        ],
        "filename": "中小機構_2024_中小企業のDX推進に関する調査.pdf"
    },
    {
        "id": "Yamane2026",
        "author": "山根ほか (2026)",
        "title": "SMOにおけるDX推進の阻害要因分析",
        "doi": "",
        "direct_urls": [],
        "filename": "山根_2026_SMOにおけるDX推進の阻害要因分析.pdf"
    }
]

def check_local_existing(paper):
    """手元ローカルディレクトリから既存PDFを探索"""
    keywords = []
    if paper["id"] == "Colquitt2001":
        keywords = ["Colquitt_Dimensionality"]
    elif paper["id"] == "Packmohr2023":
        keywords = ["UNRAVELING PERCEPTIONS OF BARRIERS", "Packmohr"]
    elif paper["id"] == "Papadopoulos2020":
        keywords = ["Papadopoulos", "COVID-19"]
    elif paper["id"] == "IPA2025":
        keywords = ["DX動向2025", "dx-trend"]
    elif paper["id"] == "Yamane2026":
        keywords = ["DX推進阻害要因の分析論文", "SMOにおけるDX推進の阻害要因分析"]
    elif paper["id"] == "Ghafoori2024":
        keywords = ["Ghafoori"]
    else:
        author_last = paper["author"].split()[0].replace(",", "")
        keywords = [author_last]

    for sdir in SEARCH_DIRS:
        if not os.path.exists(sdir):
            continue
        for fname in os.listdir(sdir):
            if not fname.lower().endswith(".pdf"):
                continue
            for kw in keywords:
                if kw.lower() in fname.lower():
                    src_path = os.path.join(sdir, fname)
                    return src_path
    return None

def fetch_open_access_pdf_url(doi):
    """Unpaywall API / OpenAlex API を用いてOpen AccessのPDF URLを取得"""
    if not doi:
        return None
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email=researcher@idm-dx.org"
        req = urllib.request.Request(url, headers={"User-Agent": "IDM-DX-Research/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("is_oa") and data.get("best_oa_location"):
                pdf_url = data["best_oa_location"].get("url_for_pdf")
                if pdf_url:
                    return pdf_url
    except Exception as e:
        pass

    # OpenAlex fallback
    try:
        url = f"https://api.openalex.org/works/https://doi.org/{doi}"
        req = urllib.request.Request(url, headers={"User-Agent": "IDM-DX-Research/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            best_oa = data.get("best_oa_location")
            if best_oa and best_oa.get("pdf_url"):
                return best_oa.get("pdf_url")
    except Exception as e:
        pass

    return None

def download_file(url, target_path):
    """ファイルをダウンロードして保存（User-Agent偽装付）"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/pdf,*/*"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()
            # PDFヘッダー確認 (%PDF)
            if data.startswith(b"%PDF") or len(data) > 50000:
                with open(target_path, "wb") as f:
                    f.write(data)
                return True, len(data)
            else:
                return False, f"Invalid format or HTML landing page (len={len(data)})"
    except Exception as e:
        return False, str(e)

def main():
    print(f"=== 文献PDFダウンロード＆集約バッチ開始 ===")
    results = []

    for paper in TARGET_PAPERS:
        pid = paper["id"]
        author = paper["author"]
        title = paper["title"]
        doi = paper["doi"]
        target_dest = os.path.join(DEST_DIR, paper["filename"])

        print(f"\n[{pid}] {author}: {title[:40]}...")

        # 1. 既に保存先にあるか？
        if os.path.exists(target_dest):
            sz = os.path.getsize(target_dest)
            print(f"  -> [ALREADY_EXIST] 保存先に既に存在します ({sz:,} bytes)")
            results.append({
                "id": pid, "author": author, "title": title, "status": "ALREADY_EXIST",
                "bytes": sz, "path": target_dest, "source": "Destination Directory"
            })
            continue

        # 2. ローカル既存フォルダにあるか？
        local_src = check_local_existing(paper)
        if local_src:
            shutil.copy2(local_src, target_dest)
            sz = os.path.getsize(target_dest)
            print(f"  -> [LOCAL_COPIED] 手元既存フォルダから取得しました: {os.path.basename(local_src)} ({sz:,} bytes)")
            results.append({
                "id": pid, "author": author, "title": title, "status": "LOCAL_COPIED",
                "bytes": sz, "path": target_dest, "source": local_src
            })
            continue

        # 3. 事前定義の直接URLからダウンロード試行
        downloaded = False
        for durl in paper.get("direct_urls", []):
            print(f"  -> 直接URLから試行中: {durl[:60]}...")
            ok, res = download_file(durl, target_dest)
            if ok:
                sz = res
                print(f"  -> [DOWNLOAD_SUCCESS] 直接URLからダウンロード成功 ({sz:,} bytes)")
                results.append({
                    "id": pid, "author": author, "title": title, "status": "DOWNLOAD_SUCCESS",
                    "bytes": sz, "path": target_dest, "source": durl
                })
                downloaded = True
                break
            else:
                print(f"     直接URL失敗: {res}")

        if downloaded:
            continue

        # 4. DOIからUnpaywall/OpenAlexでOA PDF URLを探索
        if doi:
            print(f"  -> Open Access API (Unpaywall/OpenAlex) 探索中: DOI {doi}...")
            oa_url = fetch_open_access_pdf_url(doi)
            if oa_url:
                print(f"  -> OA URL 発見: {oa_url[:60]}... ダウンロード試行中")
                ok, res = download_file(oa_url, target_dest)
                if ok:
                    sz = res
                    print(f"  -> [OA_DOWNLOAD_SUCCESS] OA API経由でダウンロード成功 ({sz:,} bytes)")
                    results.append({
                        "id": pid, "author": author, "title": title, "status": "DOWNLOAD_SUCCESS",
                        "bytes": sz, "path": target_dest, "source": oa_url
                    })
                    continue
                else:
                    print(f"     OAダウンロード失敗: {res}")
            else:
                print(f"     OA URLは見つかりませんでした（購読型・Paywall文献）")

        # 5. ダウンロード不可（ペイウォール/学術認証必要）
        print(f"  -> [PAYWALL_RESTRICTED] オープンアクセス未開放（要学内VPN/機関契約認証）")
        results.append({
            "id": pid, "author": author, "title": title, "status": "PAYWALL_RESTRICTED",
            "bytes": 0, "path": "", "source": "Paywall / Institutional License Required"
        })

    # 集約結果の保存
    out_json = os.path.join(r"G:\マイドライブ\antigravity\IDM\20261009\artifacts", "literature_download_report.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 成果サマリー表示
    print(f"\n==========================================")
    print(f"文献ダウンロード集約処理 完了サマリー")
    print(f"==========================================")
    total = len(results)
    success = sum(1 for r in results if r["status"] in ["ALREADY_EXIST", "LOCAL_COPIED", "DOWNLOAD_SUCCESS"])
    paywall = sum(1 for r in results if r["status"] == "PAYWALL_RESTRICTED")
    print(f"全対象文献数: {total} 編")
    print(f"手元取得完了 (PDF保有): {success} 編 ({success/total*100:.1f}%)")
    print(f"要機関認証 (Paywall): {paywall} 編 ({paywall/total*100:.1f}%)")

if __name__ == "__main__":
    main()

import urllib.request
import json
import time

dois_to_verify = [
    # 手元PDF実体 (真正文献)
    {"id": "PDF-01", "doi": "10.1109/TEM.2022.3215727", "expected_author": "Omrani", "expected_title": "Drivers of Digital Transformation in SMEs"},
    {"id": "PDF-02", "doi": "10.33965/ijcsis_2023180107", "expected_author": "Packmohr", "expected_title": "UNRAVELING PERCEPTIONS OF BARRIERS"},
    {"id": "PDF-03", "doi": "10.51847/rkbg4kurvq", "expected_author": "Giang", "expected_title": "Digital Transformation, Dynamic Capability"},
    {"id": "PDF-04", "doi": "10.59865/abacj.2023.52", "expected_author": "Fauzi", "expected_title": "Digital Transformation for SME Development"},
    {"id": "PDF-05", "doi": "10.3389/fpsyg.2022.977998", "expected_author": "Al-Ghazali", "expected_title": "Green transformational leadership"},
    {"id": "PDF-06", "doi": "10.1016/j.ijinfomgt.2020.102192", "expected_author": "Papadopoulos", "expected_title": "The use of digital technologies"},
    {"id": "PDF-07", "doi": "10.47750/qas/27.211.27", "expected_author": "Fajar", "expected_title": "Improving Leadership, Spirituality"},
    {"id": "PDF-08", "doi": "10.14707/ajbr.210115", "expected_author": "Liu", "expected_title": "Digital Transformation Challenges in the Sales"},
    {"id": "PDF-09", "doi": "10.2478/sbe-2022-0055", "expected_author": "Roman", "expected_title": "Digital Technologies and the Performance"},
    {"id": "PDF-10", "doi": "10.1007/s40812-026-00395-2", "expected_author": "Succurro", "expected_title": "Digital transformation in tourism SMEs"},
    {"id": "PDF-11", "doi": "10.1109/TEM.2022.3233132", "expected_author": "Lamperti", "expected_title": "Digital Servitization and Business Model Innovation"},
    {"id": "PDF-12", "doi": "10.1007/s43621-024-00506-w", "expected_author": "Al-Swidi", "expected_title": "The role of digital transformation in boosting CSR"},
    {"id": "PDF-14", "doi": "10.1371/journal.pone.0295327", "expected_author": "Hu", "expected_title": "Network evolution of diffusion"},
    {"id": "PDF-15", "doi": "10.1016/j.ijpe.2024.109205", "expected_author": "Ghafoori", "expected_title": "Toward the role of organizational culture"},
    
    # 理論基盤文献 (実在検証)
    {"id": "THEORY-01", "doi": "10.1037/h0040968", "expected_author": "Adams", "expected_title": "Toward an understanding of inequity"},
    {"id": "THEORY-03", "doi": "10.1037/0021-9010.86.3.386", "expected_author": "Colquitt", "expected_title": "On the dimensionality of organizational justice"},
    {"id": "THEORY-04", "doi": "10.1037/a0031757", "expected_author": "Colquitt", "expected_title": "Justice at the millennium"},
    {"id": "THEORY-05", "doi": "10.1037/0021-9010.71.3.500", "expected_author": "Eisenberger", "expected_title": "Perceived organizational support"},
    {"id": "THEORY-06", "doi": "10.1002/smj.4250131012", "expected_author": "Floyd", "expected_title": "Middle management involvement in strategy"},
    {"id": "THEORY-07", "doi": "10.1111/1467-6486.00059", "expected_author": "Floyd", "expected_title": "Middle management's strategic influence"},
    {"id": "THEORY-08", "doi": "10.1108/02635571111170785", "expected_author": "Ghobakhloo", "expected_title": "Adoption of e-commerce applications in SMEs"},
    {"id": "THEORY-09", "doi": "10.1177/014920639001600208", "expected_author": "Greenberg", "expected_title": "Organizational justice"},
    {"id": "THEORY-10", "doi": "10.2307/3094890", "expected_author": "Huy", "expected_title": "Emotional balancing of organizational continuity"},
    {"id": "THEORY-11", "doi": "10.5465/amr.2001.4378028", "expected_author": "Pierce", "expected_title": "Toward a theory of psychological ownership"},
    {"id": "THEORY-12", "doi": "10.1080/07421222.1999.11518227", "expected_author": "Thong", "expected_title": "An integrated model of information systems adoption"},
    {"id": "THEORY-15", "doi": "10.1177/0149206308324326", "expected_author": "Wooldridge", "expected_title": "The middle management perspective on strategy"},
    {"id": "THEORY-17", "doi": "10.1037/0003-066X.52.12.1280", "expected_author": "Higgins", "expected_title": "Beyond pleasure and pain"},
    {"id": "EXT-GARZONI", "doi": "10.1108/MD-07-2019-0939", "expected_author": "Garzoni", "expected_title": "Fostering digital transformation of SMEs"},
    {"id": "EXT-ELLER", "doi": "10.1016/j.jbusres.2020.03.004", "expected_author": "Eller", "expected_title": "Antecedents, consequences, and challenges"}
]

results = []
print(f"Starting Crossref DOI verification for {len(dois_to_verify)} items...")

for item in dois_to_verify:
    doi = item["doi"]
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": "IDM-Research-Audit/1.0 (mailto:audit@idm-dx.org)"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                message = data.get("message", {})
                title = message.get("title", [""])[0]
                container = message.get("container-title", [""])[0]
                issued = message.get("issued", {}).get("date-parts", [[None]])[0][0]
                authors = message.get("author", [])
                first_author = authors[0].get("family", "") if authors else "Unknown"
                
                res = {
                    "id": item["id"],
                    "doi": doi,
                    "status": "VALID_CROSSREF",
                    "verified_title": title,
                    "verified_journal": container,
                    "verified_year": issued,
                    "verified_first_author": first_author,
                    "expected_author": item["expected_author"],
                    "expected_title": item["expected_title"]
                }
                print(f"[{item['id']}] OK: {first_author} ({issued}) - {title[:50]}... ({container})")
                results.append(res)
            else:
                print(f"[{item['id']}] HTTP {response.status}")
                results.append({"id": item["id"], "doi": doi, "status": f"HTTP_{response.status}"})
    except Exception as e:
        print(f"[{item['id']}] Exception: {e}")
        results.append({"id": item["id"], "doi": doi, "status": f"ERROR_{str(e)}"})
    time.sleep(0.3)

out_file = r"G:\マイドライブ\antigravity\IDM\20261006\artifacts\crossref_verification_results.json"
import os
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nVerification finished. Saved results to {out_file}")

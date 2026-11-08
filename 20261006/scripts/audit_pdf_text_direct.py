import os
import json
import pypdf

pdf_dir = r"G:\マイドライブ\antigravity\IDM\20261004\papers_pdf"
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
pdf_files.sort()

results = []

for pf in pdf_files:
    path = os.path.join(pdf_dir, pf)
    try:
        reader = pypdf.PdfReader(path)
        first_page = reader.pages[0].extract_text() if len(reader.pages) > 0 else ""
        results.append({
            "file": pf,
            "pages": len(reader.pages),
            "sample_text": first_page[:600].replace("\n", " ")
        })
    except Exception as e:
        results.append({
            "file": pf,
            "error": str(e)
        })

out_json = r"G:\マイドライブ\antigravity\IDM\20261006\artifacts\pdf_firstpage_samples.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(results)} PDFs first page text. Saved to {out_json}")

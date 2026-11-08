import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('20261029/artifacts/pdf_extracted_texts.json', encoding='utf-8') as f:
    pdf_texts = json.load(f)

for idx, (k, v) in enumerate(list(pdf_texts.items())[:5], 1):
    print(f"=== {idx:02d}. {k} (Pages: {v['total_pages']}, Size: {v['filesize_kb']}KB) ===")
    print("Abstract Snippet:")
    print(v['abstract_snippet'][:300] if v['abstract_snippet'] else "No abstract found")
    print("-" * 50)

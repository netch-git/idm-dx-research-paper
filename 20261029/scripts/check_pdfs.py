import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('20261029/artifacts/pdf_extracted_texts.json', encoding='utf-8') as f:
    pdf_texts = json.load(f)

print(f"Total PDFs: {len(pdf_texts)}")
for idx, (k, pages) in enumerate(pdf_texts.items(), 1):
    total_chars = sum(len(p) for p in pages)
    print(f"{idx:02d}. {k} | pages: {len(pages)} | chars: {total_chars}")

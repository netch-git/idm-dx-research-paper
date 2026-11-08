# -*- coding: utf-8 -*-
import json

with open(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\refs_with_abstracts.json', 'r', encoding='utf-8') as f:
    refs = json.load(f)

missing = [r for r in refs if not r.get('abstract_en')]
print(f"Missing abstracts count: {len(missing)}")
for idx, m in enumerate(missing, 1):
    print(f"{idx:02d} | [{m.get('year')}] {m.get('author')[:30]} | {m.get('title')[:60]} | DOI: {m.get('doi')}")

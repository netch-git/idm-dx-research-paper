# -*- coding: utf-8 -*-
"""
全文献のアブストラクト原文をAPI（OpenAlex / Semantic Scholar / Crossref）から取得するスクリプト
"""
import json
import urllib.request
import urllib.parse
import re
import time

def clean_doi(doi_str):
    if not doi_str: return ""
    m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', doi_str)
    return m.group(0) if m else ""

def get_openalex_abstract(doi):
    cd = clean_doi(doi)
    if not cd: return None
    url = f"https://api.openalex.org/works/https://doi.org/{cd}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:researcher@idm-academic.org'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            inverted = data.get('abstract_inverted_index')
            if inverted:
                word_index = []
                for word, positions in inverted.items():
                    for pos in positions:
                        word_index.append((pos, word))
                word_index.sort(key=lambda x: x[0])
                abstract = ' '.join(w for _, w in word_index)
                return abstract
    except Exception as e:
        pass
    return None

def get_semanticscholar_abstract(doi):
    cd = clean_doi(doi)
    if not cd: return None
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{cd}?fields=abstract,title,authors,year"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            ab = data.get('abstract')
            if ab: return ab
    except Exception as e:
        pass
    return None

def get_crossref_abstract(doi):
    cd = clean_doi(doi)
    if not cd: return None
    url = f"https://api.crossref.org/works/{cd}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:researcher@idm-academic.org'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            item = data.get('message', {})
            ab = item.get('abstract')
            if ab:
                clean_ab = re.sub(r'<[^>]+>', '', ab).strip()
                return clean_ab
    except Exception as e:
        pass
    return None

def main():
    with open(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\all_unified_refs.json', 'r', encoding='utf-8') as f:
        refs = json.load(f)
        
    print(f"Total refs to fetch: {len(refs)}")
    
    results = []
    for idx, r in enumerate(refs, 1):
        title = r['title']
        doi = r.get('doi', '')
        print(f"[{idx}/{len(refs)}] Checking: {title[:40]}... (DOI: {doi})")
        
        abstract = None
        if doi:
            abstract = get_openalex_abstract(doi)
            if not abstract:
                time.sleep(0.5)
                abstract = get_semanticscholar_abstract(doi)
            if not abstract:
                time.sleep(0.5)
                abstract = get_crossref_abstract(doi)
                
        if abstract:
            print(f"  -> Found abstract ({len(abstract)} chars)")
        else:
            print("  -> Abstract not found automatically")
            
        r['abstract_en'] = abstract if abstract else ""
        results.append(r)
        time.sleep(0.3)
        
    with open(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\refs_with_abstracts.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    found_count = sum(1 for r in results if r['abstract_en'])
    print(f"\nCompleted! Found {found_count}/{len(results)} abstracts automatically.")

if __name__ == '__main__':
    main()

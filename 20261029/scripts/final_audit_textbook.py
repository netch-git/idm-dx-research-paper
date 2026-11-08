# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'G:\マイドライブ\antigravity\IDM\20261029\textbook_web\index.html', encoding='utf-8') as f:
    web_text = f.read()

bad_words = ["論破", "即死", "迎撃", "トラップ", "フルボッコ", "撃沈", "教官を黙らせる"]
print("=== Checking Web Textbook for AI-Cliches / Combativeness ===")
found_bad = False
for word in bad_words:
    if word in web_text:
        print(f"WARNING: Found aggressive word: {word}")
        found_bad = True
if not found_bad:
    print("Zero aggressive words found! Reverence & integrity 100% maintained.")

print("\n=== Checking for Control Characters in Web Textbook ===")
control_chars = [c for c in web_text if ord(c) < 32 and c not in '\r\n\t']
print(f"Total control characters: {len(control_chars)}")

print("\n=== Checking for Control Characters in EPUB Source Files ===")
import os
epub_root = r"G:\マイドライブ\antigravity\IDM\20261029\textbook_epub\OEBPS\text"
epub_bad = False
for f in os.listdir(epub_root):
    if f.endswith('.xhtml'):
        with open(os.path.join(epub_root, f), encoding='utf-8') as fp:
            t = fp.read()
            for word in bad_words:
                if word in t:
                    print(f"WARNING in EPUB {f}: {word}")
                    epub_bad = True
            c_chars = [c for c in t if ord(c) < 32 and c not in '\r\n\t']
            if c_chars:
                print(f"WARNING in EPUB {f}: found {len(c_chars)} control chars")
                epub_bad = True
if not epub_bad:
    print("EPUB text is 100% clean of aggressive words and control characters!")

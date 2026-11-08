# -*- coding: utf-8 -*-
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'G:\マイドライブ\antigravity\IDM\20261029\scripts\build_web_textbook.py', encoding='utf-8') as f:
    text = f.read()

# Extract sections
sections = re.findall(r'<section id="([^"]+)" class="chapter-section">(.*?)</section>', text, re.DOTALL)
print(f"Extracted {len(sections)} sections:")
for sid, shtml in sections:
    print(f"- {sid}: {len(shtml)} chars")

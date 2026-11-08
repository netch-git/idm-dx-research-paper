# -*- coding: utf-8 -*-
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'G:\マイドライブ\antigravity\IDM\20261029\scripts\build_web_textbook.py', encoding='utf-8') as f:
    text = f.read()

for ch_num in range(9, 16):
    m = re.search(rf'<section id="ch{ch_num}".*?</section>', text, re.DOTALL)
    if m:
        content = m.group(0)
        has_foundations = 'foundations-box' in content
        print(f"ch{ch_num}: has_foundations = {has_foundations}")
    else:
        print(f"ch{ch_num}: NOT FOUND")

import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'G:\マイドライブ\antigravity\IDM\20261029\textbook_web\index.html', encoding='utf-8') as f:
    text = f.read()

print('=== Checking formula cards in index.html ===')
for idx, m in enumerate(re.finditer(r'<div class="formula-card">(.*?)</div>', text, re.DOTALL), 1):
    raw_formula = m.group(1).strip()
    print(f'Formula {idx}: {raw_formula}')

print('\n=== Checking for control characters ===')
has_control = any(ord(c) < 32 and c not in '\r\n\t' for c in text)
print('Any control characters present:', has_control)

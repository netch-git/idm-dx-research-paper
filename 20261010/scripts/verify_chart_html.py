import re

with open(r'G:\マイドライブ\antigravity\IDM\20261008\reports\20261008_学術論文_実証図表集_ChartJS.html', 'r', encoding='utf-8') as f:
    text = f.read()

latex = re.findall(r'(\$[^\$]+\$)', text)
print('LaTeX dollar matches:', len(latex))
print('Has fig4-5:', 'id="fig4-5"' in text)
print('Has fig4-5b:', 'id="fig4-5b"' in text)
print('Has chartFig4_5:', 'chartFig4_5' in text)
print('Has chartFig4_5b:', 'chartFig4_5b' in text)

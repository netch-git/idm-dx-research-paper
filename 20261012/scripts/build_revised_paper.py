# -*- coding: utf-8 -*-
"""
build_revised_paper.py: 改訂版学術論文HTML完全ビルダースクリプト
企業規模2区分（大企業 vs SMO）および真のマスターデータ完全準拠版
"""
import os
import re
import sys

# Import section modules
from section_abstract import TITLE, ABSTRACT_HTML
from section_ch1 import CH1_HTML
from section_ch2 import CH2_HTML
from section_ch3 import CH3_HTML
from section_ch4 import CH4_HTML
from section_ch5 import CH5_HTML
from section_ch6 import CH6_HTML
from section_refs import REFS_HTML
from section_tabs import TAB_CHARTS_HTML, TAB_HYPO_HTML, TAB_REFS_HTML

SRC_PATH = r'G:\マイドライブ\antigravity\IDM\20261009\reports\20261009_学術論文ドラフト_スマホ対応フレキシブルUI.html'
DEST_2009 = SRC_PATH
DEST_2012 = r'G:\マイドライブ\antigravity\IDM\20261012\reports\20261012_学術論文ドラフト_スマホ対応フレキシブルUI_確定改訂版.html'

print("Reading source HTML...")
with open(SRC_PATH, 'r', encoding='utf-8') as f:
    html_text = f.read()

# 1. Extract head up to <div id="tab-paper" class="tab-content active">
tab_paper_start_idx = html_text.find('<div id="tab-paper" class="tab-content active">')
if tab_paper_start_idx == -1:
    print("Error: Could not find tab-paper start")
    sys.exit(1)

head_part = html_text[:tab_paper_start_idx]

# Replace <title> in head_part with refined title
head_part = re.sub(r'<title>.*?</title>', f'<title>【確定改訂版】{TITLE} (N=2,035)</title>', head_part, flags=re.DOTALL)

# 2. Assemble new tab-paper content
new_tab_paper = f"""<div id="tab-paper" class="tab-content active">
{ABSTRACT_HTML}
{CH1_HTML}
{CH2_HTML}
{CH3_HTML}
{CH4_HTML}
{CH5_HTML}
{CH6_HTML}
{REFS_HTML}
</div>
"""

# 3. Find end of tab-hypo or bottom-nav
bottom_nav_idx = html_text.find('<nav class="bottom-nav">')
if bottom_nav_idx == -1:
    print("Error: Could not find bottom-nav start")
    sys.exit(1)

tail_part = html_text[bottom_nav_idx:]

# 3b. Ensure createFig4_1 and LITERATURE_DATA in tail_part match 2-category (大企業 vs SMO) and Model 1 (tier_a) values
tail_part = tail_part.replace("data: [3.667, 3.402, 3.242]", "data: [3.852, 3.400, 3.227]")
tail_part = tail_part.replace("data: [3.570, 3.308, 3.230]", "data: [3.519, 3.306, 3.243]")
tail_part = tail_part.replace("y: { min: 3.10, max: 3.80,", "y: { min: 3.10, max: 4.00,")
tail_part = tail_part.replace("大企業と中小企業の構造的差異の定式化。", "大企業とSMOの構造的差異の定式化。")
tail_part = tail_part.replace("中小企業におけるデジタル変革阻害要因を大企業と比較検証。", "SMOにおけるデジタル変革阻害要因を大企業と比較検証。")
tail_part = tail_part.replace("SMO中間層が経営陣の期待と現場の板挟みで当事者意識をすり減らすメカニズムの基盤。", "SMO中間層が経営陣の期待と現場の要求の間で役割葛藤に直面し、当事者意識の低下を招くメカニズムの基盤。")

# 4. Assemble complete new HTML
complete_html = head_part + new_tab_paper + "\n" + TAB_CHARTS_HTML + "\n" + TAB_REFS_HTML + "\n" + TAB_HYPO_HTML + "\n" + tail_part

# Write to DEST_2009 (original requested file)
print(f"Writing to {DEST_2009}...")
with open(DEST_2009, 'w', encoding='utf-8') as f:
    f.write(complete_html)

# Write to DEST_2012 (today's archive)
os.makedirs(os.path.dirname(DEST_2012), exist_ok=True)
print(f"Writing to {DEST_2012}...")
with open(DEST_2012, 'w', encoding='utf-8') as f:
    f.write(complete_html)

print("Build complete successfully!")
print(f"File size: {len(complete_html.encode('utf-8')):,} bytes")

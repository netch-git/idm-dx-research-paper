import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('20261014/reports/20261014_学術論文ドラフト_スマホ対応フレキシブルUI_確定版.html', encoding='utf-8') as f:
    text = f.read()

# 1. 目次ドロワー全体のHTML
m_drawer = re.search(r'<div class="drawer-overlay".*?</ul>\s*</div>\s*</div>', text, re.DOTALL)
if m_drawer:
    print("=== TOC Drawer Links ===")
    for line in m_drawer.group(0).split('\n'):
        if 'href=' in line:
            print("  ", line.strip())

# 2. 本文側のセクションID、見出しID、図表ID
print("\n=== Body Headings / Section IDs ===")
for m in re.finditer(r'<(?:h[1-6]|section|div)[^>]*id="([^"]+)"[^>]*>(.*?)</', text):
    tag_id = m.group(1)
    content = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    if any(k in tag_id.lower() for k in ['ch', 'sec', 'fig', 'table', 'tab', 'ref', 'abs', 'title']):
        print(f"  id='{tag_id}' -> {content[:40]}")

# 3. 参考文献セクションの構造
print("\n=== References Container ===")
m_ref = re.search(r'<(?:div|section|ol|ul)[^>]*class="[^"]*references[^"]*"[^>]*>.*?</(?:div|section|ol|ul)>', text, re.DOTALL)
if not m_ref:
    m_ref = re.search(r'id="references".*?</(?:div|section|ol|ul)>', text, re.DOTALL)
if m_ref:
    print(m_ref.group(0)[:600])
else:
    # Look for Adams, J. S.
    idx = text.find('Adams, J. S.')
    if idx != -1:
        print("Found Adams around:\n", text[idx-100:idx+300])

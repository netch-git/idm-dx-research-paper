import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('20261014/reports/20261014_学術論文ドラフト_スマホ対応フレキシブルUI_確定版.html', encoding='utf-8') as f:
    text = f.read()

print("HTML Length:", len(text))

# 1. Drawer / TOC search
m_drawer = re.search(r'<div[^>]*class="[^"]*drawer[^"]*"[^>]*>.*?</div>\s*</div>', text, re.DOTALL)
if m_drawer:
    print("Found drawer snippet:\n", m_drawer.group(0)[:800])
else:
    # Look for TOC drawer
    for m in re.finditer(r'<nav[^>]*class="[^"]*drawer[^"]*"[^>]*>.*?</nav>', text, re.DOTALL):
        print("Found nav drawer:\n", m.group(0)[:800])

# 2. Look for literature search container and script
print("\n--- Lit Search HTML snippets ---")
for m in re.finditer(r'.{0,100}(?:litSearchInput|refSearchInput|litCardContainer|literatureCardsList).{0,100}', text):
    print(m.group(0).strip())

# 3. Look for script references to literature cards
print("\n--- JavaScript references to literature ---")
for m in re.finditer(r'function\s+(?:filterLiterature|renderLiteratureCards|searchReferences)[^{]*\{[^}]{0,300}\}', text):
    print(m.group(0))

# 4. Check references section
print("\n--- References section count ---")
m_ref = re.search(r'<section[^>]*id="references"[^>]*>.*?</section>', text, re.DOTALL)
if m_ref:
    li_count = len(re.findall(r'<li', m_ref.group(0)))
    print(f"References li count: {li_count}")
    print("Siemsen present in references?", "Siemsen" in m_ref.group(0))
else:
    # check other ref structures
    li_count = len(re.findall(r'class="ref-item"', text))
    print(f"ref-item count: {li_count}")
    print("Siemsen in text?", "Siemsen" in text)

import re

path = r'G:\マイドライブ\antigravity\IDM\20261009\reports\20261009_学術論文ドラフト_スマホ対応フレキシブルUI.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see the main section delimiters
# From <h1 to </main> or </body>
body_match = re.search(r'(<body[^>]*>)(.*?)(</body>)', text, re.DOTALL)
if body_match:
    body_content = body_match.group(2)
    print("Body length:", len(body_content))
    
    # Check headers in body
    headers = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', body_content)
    with open(r'G:\マイドライブ\antigravity\IDM\20261012\artifacts\current_headers.txt', 'w', encoding='utf-8') as out:
        for h in headers:
            clean_h = re.sub(r'<[^>]+>', '', h).strip()
            out.write(clean_h + '\n')
    print(f"Saved {len(headers)} headers to current_headers.txt")


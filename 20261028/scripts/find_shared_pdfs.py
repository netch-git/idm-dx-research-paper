import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Search across G:
cutoff = datetime.datetime(2026, 10, 26)
found_pdfs = []

search_paths = [
    'G:/マイドライブ',
    'G:/共有ドライブ',
    'G:/共有アイテム',
    'G:/'
]

print("Searching for PDFs...")
for base in search_paths:
    if not os.path.exists(base):
        print(f"Path does not exist: {base}")
        continue
    print(f"Scanning {base}...")
    try:
        # Check direct children first
        for item in os.listdir(base):
            item_path = os.path.join(base, item)
            if os.path.isfile(item_path) and item.lower().endswith('.pdf'):
                try:
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
                    found_pdfs.append((item_path, mtime, os.path.getsize(item_path)))
                except:
                    pass
    except Exception as e:
        print(f"Error listing {base}: {e}")

# Also check specific folders like IDM, Downloads, Desktop, etc.
check_dirs = [
    'G:/マイドライブ/IDM',
    'G:/マイドライブ/antigravity/IDM',
    'C:/Users/kynet/Downloads',
    'C:/Users/kynet/Desktop'
]

for d in check_dirs:
    if not os.path.exists(d):
        continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.lower().endswith('.pdf'):
                p = os.path.join(root, f)
                try:
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(p))
                    if mtime >= cutoff or any(k in f.lower() for k in ['scan', 'takata', 'kaidou', 'book', 'festinger', 'adams', 'aiken', 'folger', 'leventhal', 'vroom', 'nunnally']):
                        found_pdfs.append((p, mtime, os.path.getsize(p)))
                except:
                    pass

print(f"\nTotal PDFs found matching criteria: {len(found_pdfs)}")
for p, t, s in sorted(set(found_pdfs), key=lambda x: x[1], reverse=True)[:50]:
    print(f"{t} | {s:>10,} bytes | {p}")

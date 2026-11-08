import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

cutoff = datetime.datetime(2026, 10, 27) # Yesterday and today
found = []

print("Scanning all of G:/マイドライブ recursively for recent PDFs...")
root_dir = 'G:/マイドライブ'

for root, dirs, files in os.walk(root_dir):
    # skip git and large caches
    if '.git' in root or '.venv' in root:
        continue
    for f in files:
        if f.lower().endswith('.pdf'):
            p = os.path.join(root, f)
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(p))
                ctime = datetime.datetime.fromtimestamp(os.path.getctime(p))
                if mtime >= cutoff or ctime >= cutoff:
                    found.append((p, mtime, ctime, os.path.getsize(p)))
            except:
                pass

print(f"Found {len(found)} recent PDFs (since 2026-10-27):")
for p, m, c, s in sorted(found, key=lambda x: max(x[1], x[2]), reverse=True):
    print(f"Mod: {m} | Create: {c} | {s:>10,} bytes | {p}")

import os
import sys
import json
import urllib.request
import urllib.parse
import re

sys.stdout.reconfigure(encoding='utf-8')

DEST_DIR = r'G:\マイドライブ\antigravity\IDM\20261028\papers_pdf'
os.makedirs(DEST_DIR, exist_ok=True)

with open(r'G:\マイドライブ\antigravity\IDM\20261028\artifacts\shared_drive_files.json', 'r', encoding='utf-8') as f:
    files = json.load(f)

print(f"Attempting to download {len(files)} files to {DEST_DIR}...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def download_drive_file(file_id, dest_path):
    # Google drive direct download URL
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            # check if confirm token is needed (large files)
            if b"confirm=" in content or b"Google Drive - Virus scan warning" in content:
                # parse confirm token
                html = content.decode('utf-8', errors='ignore')
                m = re.search(r'confirm=([0-9a-zA-Z_]+)', html)
                if m:
                    confirm_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={m.group(1)}"
                    req2 = urllib.request.Request(confirm_url, headers=headers)
                    with urllib.request.urlopen(req2, timeout=30) as resp2:
                        content = resp2.read()
            
            if content.startswith(b'%PDF'):
                with open(dest_path, 'wb') as f_out:
                    f_out.write(content)
                print(f"  [SUCCESS] Downloaded {os.path.basename(dest_path)} ({len(content):,} bytes)")
                return True
            else:
                print(f"  [WARN] Not a PDF: {content[:100]}")
                return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

# Test the first one
test_item = files[0]
safe_fn = test_item['filename'].replace('/', '_').replace(':', '_')
dest_test = os.path.join(DEST_DIR, safe_fn)
print(f"Testing download for {safe_fn} (ID: {test_item['file_id']})...")
download_drive_file(test_item['file_id'], dest_test)

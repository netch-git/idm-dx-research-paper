import os
import sys
import json
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

sys.stdout.reconfigure(encoding='utf-8')

CRED_DIR = r'G:\マイドライブ\antigravity\credentials'
TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')
JSON_FILE = r'G:\マイドライブ\antigravity\IDM\20261028\artifacts\shared_drive_files.json'
DEST_DIR = r'G:\マイドライブ\antigravity\IDM\20261028\papers_pdf'
os.makedirs(DEST_DIR, exist_ok=True)

with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    token_info = json.load(f)

creds = Credentials.from_authorized_user_info(token_info)
drive_service = build('drive', 'v3', credentials=creds)

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    files = json.load(f)

print(f"=== Starting Download of {len(files)} Shared PDF Files ===")
download_results = []

for idx, item in enumerate(files, 1):
    file_id = item['file_id']
    orig_name = item['filename']
    safe_name = orig_name.replace('/', '_').replace(':', '_')
    dest_path = os.path.join(DEST_DIR, safe_name)
    
    print(f"\n[{idx}/{len(files)}] Fetching metadata for {orig_name} (ID: {file_id})...")
    try:
        meta = drive_service.files().get(fileId=file_id, fields='id, name, mimeType, size').execute()
        size_str = f"{int(meta.get('size', 0)):,} bytes" if 'size' in meta else "unknown size"
        print(f"  Drive Name: {meta.get('name')}, Size: {size_str}")
        
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  Download Progress: {int(status.progress() * 100)}%", end='\r')
        print(f"  Download Complete!")
        
        file_bytes = fh.getvalue()
        with open(dest_path, 'wb') as f_out:
            f_out.write(file_bytes)
            
        print(f"  Saved to: {dest_path} ({len(file_bytes):,} bytes)")
        download_results.append({
            'index': idx,
            'orig_name': orig_name,
            'safe_name': safe_name,
            'file_id': file_id,
            'dest_path': dest_path,
            'size': len(file_bytes),
            'status': 'SUCCESS'
        })
    except Exception as e:
        print(f"  [ERROR] Failed to download {orig_name}: {e}")
        download_results.append({
            'index': idx,
            'orig_name': orig_name,
            'safe_name': safe_name,
            'file_id': file_id,
            'dest_path': dest_path,
            'size': 0,
            'status': f'ERROR: {e}'
        })

summary_file = r'G:\マイドライブ\antigravity\IDM\20261028\artifacts\download_summary.json'
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(download_results, f, ensure_ascii=False, indent=2)

print(f"\n=== Download Finished: {len([r for r in download_results if r['status'] == 'SUCCESS'])}/{len(files)} files downloaded ===")

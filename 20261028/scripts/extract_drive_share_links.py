import os
import sys
import base64
import json
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

CRED_DIR = r'G:\マイドライブ\antigravity\credentials'
TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')

with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    token_info = json.load(f)

creds = Credentials.from_authorized_user_info(token_info)
service = build('gmail', 'v1', credentials=creds)

query = 'from:drive-shares-dm-noreply@google.com "スキャン"'
results = service.users().messages().list(userId='me', q=query).execute()
messages = results.get('messages', [])

print(f"Found {len(messages)} Google Drive share messages.")

shared_files = []

def extract_body_text(part):
    text = ""
    if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
        text += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
    if 'parts' in part:
        for p in part['parts']:
            text += extract_body_text(p)
    return text

for msg in messages:
    msg_id = msg['id']
    m = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = m.get('payload', {})
    headers = payload.get('headers', [])
    
    subject = ""
    date = ""
    for h in headers:
        name = h['name'].lower()
        if name == 'subject':
            subject = h['value']
        elif name == 'date':
            date = h['value']
            
    body_text = extract_body_text(payload)
    
    match = re.search(r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view', body_text)
    if match:
        file_id = match.group(1)
        fn_match = re.search(r'「([^」]+)」', subject)
        filename = fn_match.group(1) if fn_match else f"{file_id}.pdf"
        shared_files.append({
            'date': date,
            'subject': subject,
            'filename': filename,
            'file_id': file_id,
            'url': match.group(0)
        })

print(f"\nExtracted {len(shared_files)} shared files:")
for item in shared_files:
    print(f" - {item['filename']} | ID: {item['file_id']} | Date: {item['date']}")

out_file = r'G:\マイドライブ\antigravity\IDM\20261028\artifacts\shared_drive_files.json'
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(shared_files, f, ensure_ascii=False, indent=2)
print("Saved to", out_file)

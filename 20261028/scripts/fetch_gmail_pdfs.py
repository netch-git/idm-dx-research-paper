import os
import sys
import base64
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

CRED_DIR = r'G:\マイドライブ\antigravity\credentials'
TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')
CLIENT_FILE = os.path.join(CRED_DIR, 'gmail_oauth_client.json')

DEST_DIR = r'G:\マイドライブ\antigravity\IDM\20261028\papers_pdf'
os.makedirs(DEST_DIR, exist_ok=True)

print("Loading Gmail credentials...")
with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    token_info = json.load(f)

creds = Credentials.from_authorized_user_info(token_info)
service = build('gmail', 'v1', credentials=creds)

print("Searching messages from kaidou.takata@gmail.com...")
# Search query
query = "from:kaidou.takata@gmail.com"
results = service.users().messages().list(userId='me', q=query).execute()
messages = results.get('messages', [])

print(f"Found {len(messages)} messages.")

if not messages:
    # Also search by name or general query
    print("Searching with query 'kaidou'...")
    results = service.users().messages().list(userId='me', q="kaidou").execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages for 'kaidou'.")

for msg in messages:
    msg_id = msg['id']
    m = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = m.get('payload', {})
    headers = payload.get('headers', [])
    
    subject = ""
    sender = ""
    date = ""
    for h in headers:
        if h['name'].lower() == 'subject':
            subject = h['value']
        elif h['name'].lower() == 'from':
            sender = h['value']
        elif h['name'].lower() == 'date':
            date = h['value']
            
    print(f"\nMessage ID: {msg_id}")
    print(f"Date: {date}")
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    
    # Check parts for attachments
    parts = [payload]
    attachments = []
    
    def extract_parts(p):
        if 'parts' in p:
            for sub in p['parts']:
                extract_parts(sub)
        else:
            filename = p.get('filename', '')
            body = p.get('body', {})
            att_id = body.get('attachmentId')
            mime = p.get('mimeType', '')
            if filename or att_id:
                attachments.append({
                    'filename': filename,
                    'att_id': att_id,
                    'size': body.get('size', 0),
                    'mime': mime
                })
            # Also look at body text
            if mime == 'text/plain' and 'data' in body:
                text_data = base64.urlsafe_b64decode(body['data']).decode('utf-8', errors='ignore')
                print("Body snippet:\n", text_data[:300])
            elif mime == 'text/html' and 'data' in body:
                # snippet of html
                pass

    extract_parts(payload)
    
    print(f"Attachments ({len(attachments)}):")
    for att in attachments:
        fn = att['filename']
        print(f" - {fn} ({att['size']} bytes, mime: {att['mime']}, att_id: {bool(att['att_id'])})")
        if fn.lower().endswith('.pdf') and att['att_id']:
            dest_file = os.path.join(DEST_DIR, fn)
            print(f"   Downloading attachment {fn} to {dest_file}...")
            att_data = service.users().messages().attachments().get(
                userId='me', messageId=msg_id, id=att['att_id']
            ).execute()
            file_data = base64.urlsafe_b64decode(att_data['data'])
            with open(dest_file, 'wb') as f_out:
                f_out.write(file_data)
            print(f"   Successfully saved {len(file_data):,} bytes!")

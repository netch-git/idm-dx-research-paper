import os
import sys
import base64
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

CRED_DIR = r'G:\マイドライブ\antigravity\credentials'
TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')
CLIENT_FILE = os.path.join(CRED_DIR, 'gmail_oauth_client.json')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly'
]

DEST_DIR = r'G:\マイドライブ\antigravity\IDM\20261028\papers_pdf'
os.makedirs(DEST_DIR, exist_ok=True)

creds = None
# Try loading existing token
if os.path.exists(TOKEN_FILE):
    try:
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            token_info = json.load(f)
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    except Exception as e:
        print(f"Failed to load token: {e}")

# If credentials don't exist or are invalid, refresh or re-authenticate
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        try:
            print("Refreshing token...")
            creds.refresh(Request())
        except Exception as e:
            print(f"Refresh failed ({e}). Starting browser authentication flow...")
            creds = None
            
    if not creds:
        print("Launching browser for Gmail authorization...")
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
        creds = flow.run_local_server(port=0, prompt='consent')
        
    # Save the refreshed/new credentials
    print(f"Saving new token to {TOKEN_FILE}...")
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        f.write(creds.to_json())
    print("Token saved successfully!")

service = build('gmail', 'v1', credentials=creds)

print("\nSearching messages from kaidou.takata@gmail.com...")
# Let's search broadly for kaidou.takata@gmail.com
query = "from:kaidou.takata@gmail.com"
results = service.users().messages().list(userId='me', q=query).execute()
messages = results.get('messages', [])
print(f"Found {len(messages)} messages with query: {query}")

if not messages:
    query = "kaidou"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages with query: {query}")

downloaded_files = []

for msg in messages:
    msg_id = msg['id']
    m = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = m.get('payload', {})
    headers = payload.get('headers', [])
    
    subject = ""
    sender = ""
    date = ""
    for h in headers:
        name = h['name'].lower()
        if name == 'subject':
            subject = h['value']
        elif name == 'from':
            sender = h['value']
        elif name == 'date':
            date = h['value']
            
    print(f"\n==========================================")
    print(f"Message ID: {msg_id}")
    print(f"Date: {date}")
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    
    def walk_parts(part):
        mime = part.get('mimeType', '')
        filename = part.get('filename', '')
        body = part.get('body', {})
        att_id = body.get('attachmentId')
        
        # Check text body for links or content
        if mime == 'text/plain' and 'data' in body:
            try:
                t = base64.urlsafe_b64decode(body['data']).decode('utf-8', errors='ignore')
                print(f"Body snippet:\n{t.strip()[:400]}\n---")
            except:
                pass
        elif mime == 'text/html' and 'data' in body:
            try:
                t = base64.urlsafe_b64decode(body['data']).decode('utf-8', errors='ignore')
                # print any drive or download links
                import re
                links = re.findall(r'href=[\"\'](https?://[^\s\"\'>]+)[\"\']', t)
                for l in links:
                    if 'drive.google.com' in l or 'dropbox' in l or 'onedrive' in l or '.pdf' in l:
                        print(f"Found Cloud/File Link in email: {l}")
            except:
                pass
                
        if filename and filename.lower().endswith('.pdf'):
            dest_file = os.path.join(DEST_DIR, filename)
            print(f"Found PDF Attachment: {filename} (size: {body.get('size')} bytes)")
            if att_id:
                print(f"Downloading {filename}...")
                att = service.users().messages().attachments().get(
                    userId='me', messageId=msg_id, id=att_id
                ).execute()
                file_bytes = base64.urlsafe_b64decode(att['data'])
                with open(dest_file, 'wb') as f_out:
                    f_out.write(file_bytes)
                print(f"Saved: {dest_file} ({len(file_bytes):,} bytes)")
                downloaded_files.append((filename, dest_file, len(file_bytes)))
                
        if 'parts' in part:
            for subpart in part['parts']:
                walk_parts(subpart)

    walk_parts(payload)

print(f"\n==========================================")
print(f"Summary: Successfully downloaded {len(downloaded_files)} PDF files to {DEST_DIR}")
for fn, p, s in downloaded_files:
    print(f" - {fn} ({s:,} bytes)")

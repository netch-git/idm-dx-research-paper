import os
import sys
import json
from google_auth_oauthlib.flow import InstalledAppFlow

sys.stdout.reconfigure(encoding='utf-8')

CRED_DIR = r'G:\マイドライブ\antigravity\credentials'
CLIENT_FILE = os.path.join(CRED_DIR, 'gmail_oauth_client.json')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly'
]

PORT = 8080
REDIRECT_URI = f'http://localhost:{PORT}/'

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_FILE,
    SCOPES,
    redirect_uri=REDIRECT_URI
)

# Generate authorization URL with redirect_uri
auth_url, _ = flow.authorization_url(
    prompt='consent',
    access_type='offline'
)

print("=" * 80, flush=True)
print("AUTH_URL_START", flush=True)
print(auth_url, flush=True)
print("AUTH_URL_END", flush=True)
print("=" * 80, flush=True)

# Now wait for the local server to capture the code
print(f"Waiting for authentication on local server ({REDIRECT_URI})...", flush=True)
creds = flow.run_local_server(port=PORT, open_browser=False)

TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')
with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
    f.write(creds.to_json())

print("SUCCESS: Token saved to", TOKEN_FILE, flush=True)

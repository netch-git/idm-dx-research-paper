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
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)

msg = """
================================================================================
AUTH_URL_START
{url}
AUTH_URL_END
================================================================================
"""

print("Starting flow...", flush=True)
creds = flow.run_local_server(
    port=PORT,
    open_browser=False,
    authorization_prompt_message=msg
)

TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')
with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
    f.write(creds.to_json())

print("SUCCESS: Token saved to", TOKEN_FILE, flush=True)

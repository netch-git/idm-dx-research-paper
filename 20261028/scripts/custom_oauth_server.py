import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow

sys.stdout.reconfigure(encoding='utf-8')

CRED_DIR = r'G:\マイドライブ\antigravity\credentials'
CLIENT_FILE = os.path.join(CRED_DIR, 'gmail_oauth_client.json')
TOKEN_FILE = os.path.join(CRED_DIR, 'gmail_token.json')
URL_FILE = r'G:\マイドライブ\antigravity\IDM\20261028\scripts\auth_url.txt'

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

auth_url, state = flow.authorization_url(
    prompt='consent',
    access_type='offline'
)

with open(URL_FILE, 'w', encoding='utf-8') as f:
    f.write(auth_url)

print("=" * 80, flush=True)
print("AUTH_URL:", flush=True)
print(auth_url, flush=True)
print("=" * 80, flush=True)

auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>認証に成功しました！</h1><p>このウィンドウを閉じてエージェントにお戻りください。</p>".encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authentication failed.")

print(f"Waiting for authorization callback on port {PORT}...", flush=True)
server = HTTPServer(('localhost', PORT), OAuthHandler)
while auth_code is None:
    server.handle_request()

print("Callback received! Fetching token...", flush=True)
flow.fetch_token(code=auth_code)
creds = flow.credentials

with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
    f.write(creds.to_json())

print("SUCCESS: Token saved successfully to", TOKEN_FILE, flush=True)

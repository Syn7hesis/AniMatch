from flask import Flask, request, redirect, session  # Import session here
import requests
import base64
import hashlib
import os


app = Flask(__name__)

CLIENT_ID = '8f277978604007d8782b45e94e34a3cc'  # Replace with your Client ID
CLIENT_SECRET = '84fb3fb5f28a9cd0171d4e7367537c581b04ac8f1183435b04d403176afd3b59'  # Replace with your Client Secret
REDIRECT_URI = 'http://127.0.0.1:100/auth/callback'


# Function to create a code_verifier
def create_code_verifier():
    token = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    return token.replace('=', '')

# Function to create a code_challenge
def create_code_challenge(verifier):
    sha256 = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(sha256).decode('utf-8').replace('=', '')

@app.route('/')
def home():
    code_verifier = create_code_verifier()
    code_challenge = create_code_challenge(code_verifier)
    # Store code_verifier in session for later use
    session['code_verifier'] = code_verifier
    auth_url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}&code_challenge_method=S256&redirect_uri={REDIRECT_URI}'
    return f'<a href="{auth_url}">Authorize</a>'

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    code_verifier = session.get('code_verifier')
    print(f'Code: {code}')  # Log the code
    print(f'Code Verifier: {code_verifier}')  # Log the code verifier
    if code and code_verifier:
        token_url = 'https://myanimelist.net/v1/oauth2/token'
        token_data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
        }
        response = requests.post(token_url, data=token_data)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            return f'Authorization successful! Access Token: {access_token}'
        else:
            return f'Failed to retrieve access token. Status Code: {response.status_code}. Response: {response.text}'
    else:
        return 'Missing code or code_verifier'


if __name__ == '__main__':
    app.secret_key = os.urandom(24)  # Set a secret key for session management
    app.run(port=100)

from flask import Flask, request

app = Flask(__name__)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    # Handle the authorization code...
    return "Authorization successful!"

if __name__ == '__main__':
    app.run(port=100)

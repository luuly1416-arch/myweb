import os
from flask import Flask, redirect, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "dev_secret_key"

oauth = OAuth(app)

google = oauth.register(
    name="google",
client_id=os.environ.get("GOOGLE_CLIENT_ID"),
client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"}
)

@app.route("/")
def home():
    return '<a href="/login">Đăng nhập bằng Google</a>'

@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    user = google.get("userinfo").json()
    return f"Xin chào {user['email']}"

if __name__ == "__main__":
    app.run(debug=True)


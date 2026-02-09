import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# Bắt buộc phải có SECRET_KEY
app.secret_key = os.environ.get("SECRET_KEY")

# Cấu hình OAuth
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

@app.route("/")
def home():
    return '<h2>Trang chủ</h2><a href="/login">Đăng nhập bằng Google</a>'

@app.route("/login")
def login():
    return google.authorize_redirect(
        redirect_uri=url_for("authorize", _external=True)
    )

@app.route("/authorize")
def authorize():
    try:
        token = google.authorize_access_token()
        user = google.get("userinfo").json()
        return f"<h2>Xin chào {user['email']}</h2>"
    except Exception as e:
        return f"Lỗi: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)




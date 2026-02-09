import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

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
    return """
    <h2>Trang chủ</h2>
    <a href="/login">Đăng nhập bằng Google</a>
    """

@app.route("/login")
def login():
    return google.authorize_redirect(
        redirect_uri=url_for("authorize", _external=True)
    )

@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()

    # ✅ LẤY USER TỪ ID TOKEN (KHÔNG GỌI userinfo)
    user = token.get("userinfo")

    if not user:
        return "Không lấy được thông tin người dùng"

    return f"""
    <h2>Đăng nhập thành công 🎉</h2>
    <p>Email: {user.get('email')}</p>
    <p>Tên: {user.get('name')}</p>
    <img src="{user.get('picture')}" />
    """

if __name__ == "__main__":
    app.run(debug=True)



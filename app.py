from flask import Flask, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    api_base_url="https://openidconnect.googleapis.com/v1/",
    client_kwargs={
        "scope": "openid email profile"
    },
)

@app.route("/")
def home():
    user = session.get("user")
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Neon Login</title>
<style>
body{
    background:#0b0b16;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    color:white;
    font-family:Arial;
}
.box{
    padding:50px;
    border-radius:20px;
    background:#14142a;
    box-shadow:0 0 30px #00f2ff,0 0 60px #ff00ff;
    text-align:center;
}
button{
    padding:15px 40px;
    border-radius:30px;
    border:none;
    background:#00f2ff;
    cursor:pointer;
    font-size:16px;
}
</style>
</head>
<body>
<div class="box">
{% if user %}
<h2>Xin chào {{ user.email }}</h2>
<a href="/logout">Đăng xuất</a>
{% else %}
<h2>Đăng nhập Google</h2>
<a href="/login"><button>Login with Google</button></a>
{% endif %}
</div>
</body>
</html>
""", user=user)

@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    userinfo = google.get("userinfo").json()
    session["user"] = userinfo
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



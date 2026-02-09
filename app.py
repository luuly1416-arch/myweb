from flask import Flask, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# ===== GOOGLE OAUTH =====
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={
        "scope": "openid email profile"
    },
)

# ===== HOME =====
@app.route("/")
def home():
    user = session.get("user")
    return render_template_string("""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Neon Login</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Orbitron',sans-serif}
body{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:#0b0b16;
    color:white;
}
.card{
    padding:60px;
    border-radius:25px;
    background:rgba(20,20,40,0.85);
    box-shadow:0 0 20px #00f2ff,0 0 40px #ff00ff;
    text-align:center;
    animation:fade 1.2s ease;
}
@keyframes fade{
    from{opacity:0;transform:scale(0.8)}
    to{opacity:1;transform:scale(1)}
}
h1{
    color:#00f2ff;
    margin-bottom:20px;
    text-shadow:0 0 10px #00f2ff,0 0 30px #ff00ff;
}
p{margin-bottom:30px;color:#aaa}
.btn{
    padding:15px 40px;
    border-radius:40px;
    border:2px solid #00f2ff;
    background:transparent;
    color:#00f2ff;
    cursor:pointer;
    font-size:16px;
    transition:0.3s;
}
.btn:hover{
    background:#00f2ff;
    color:#000;
    box-shadow:0 0 20px #00f2ff,0 0 40px #ff00ff;
}
.user{
    color:#00ff88;
    margin-top:20px;
}
</style>
</head>
<body>
<div class="card">
    <h1>⚡ NEON LOGIN ⚡</h1>

    {% if user %}
        <p>Đăng nhập thành công 🎉</p>
        <div class="user">
            👤 {{ user.email }} <br>
            <a href="/logout" style="color:#ff0080">Đăng xuất</a>
        </div>
    {% else %}
        <p>Bấm nút dưới để đăng nhập Google</p>
        <a href="/login"><button class="btn">🚀 Login with Google</button></a>
    {% endif %}
</div>
</body>
</html>
""", user=user)

# ===== LOGIN =====
@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

# ===== AUTHORIZE =====
@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    userinfo = google.get("userinfo").json()
    session["user"] = userinfo
    return redirect("/")

# ===== LOGOUT =====
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



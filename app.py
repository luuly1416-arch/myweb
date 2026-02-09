import os
from flask import Flask, redirect, url_for, session, render_template_string
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# =========================
# DARK NEON TEMPLATE
# =========================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Neon Login</title>
<style>
body {
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:#0f0f0f;
    font-family:Arial, sans-serif;
    color:white;
    overflow:hidden;
}
.bg {
    position:absolute;
    width:200%;
    height:200%;
    background: radial-gradient(circle at center, #111 0%, #000 70%);
    animation: move 10s infinite linear;
}
@keyframes move {
    0% {transform: rotate(0deg);}
    100% {transform: rotate(360deg);}
}
.card {
    position:relative;
    padding:40px;
    border-radius:20px;
    background:rgba(20,20,20,0.8);
    box-shadow:0 0 30px #00f0ff, 0 0 60px #ff00f0;
    text-align:center;
    animation: fadeIn 1.2s ease;
}
@keyframes fadeIn {
    from {opacity:0; transform: translateY(30px);}
    to {opacity:1; transform: translateY(0);}
}
.btn {
    display:inline-block;
    margin-top:20px;
    padding:12px 25px;
    border-radius:50px;
    text-decoration:none;
    color:white;
    background:linear-gradient(90deg,#00f0ff,#ff00f0);
    box-shadow:0 0 20px #00f0ff;
    transition:0.3s;
}
.btn:hover {
    transform:scale(1.1);
    box-shadow:0 0 40px #ff00f0;
}
.email {
    margin-top:15px;
    font-size:18px;
    color:#00f0ff;
}
.logout {
    display:block;
    margin-top:15px;
    color:#ff4d4d;
    text-decoration:none;
}
</style>
</head>
<body>
<div class="bg"></div>
<div class="card">
{% if user %}
    <h2>✨ Welcome ✨</h2>
    <div class="email">{{ user }}</div>
    <a href="/logout" class="logout">Logout</a>
{% else %}
    <h2>🌌 Neon Google Login</h2>
    <a href="/login" class="btn">Login with Google</a>
{% endif %}
</div>
</body>
</html>
"""

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    user = session.get("user")
    return render_template_string(TEMPLATE, user=user)

@app.route("/login")
def login():
    try:
        nonce = generate_token()
        session["nonce"] = nonce
        redirect_uri = url_for("authorize", _external=True)
        return google.authorize_redirect(redirect_uri, nonce=nonce)
    except Exception as e:
        return f"Login error: {str(e)}"

@app.route("/authorize")
def authorize():
    try:
        token = google.authorize_access_token()
        nonce = session.get("nonce")
        user_info = google.parse_id_token(token, nonce=nonce)
        session["user"] = user_info["email"]
        return redirect("/")
    except Exception as e:
        return f"OAuth Error: {str(e)}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================

if __name__ == "__main__":
    app.run(debug=True)

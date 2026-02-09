from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Neon Pro Website</title>

<!-- Google Font -->
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family: 'Orbitron', sans-serif;
}

body{
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:#0f0f1a;
    overflow:hidden;
}

/* Animated gradient background */
body::before{
    content:"";
    position:absolute;
    width:200%;
    height:200%;
    background:linear-gradient(45deg,#00f2ff,#ff00ff,#00ff88,#ff0080);
    animation:moveBg 10s linear infinite;
    z-index:-2;
    opacity:0.1;
}

@keyframes moveBg{
    0%{transform:translate(0,0)}
    50%{transform:translate(-25%,-25%)}
    100%{transform:translate(0,0)}
}

/* Main Card */
.card{
    background:rgba(20,20,40,0.85);
    padding:60px;
    border-radius:25px;
    text-align:center;
    backdrop-filter:blur(15px);
    border:1px solid rgba(0,255,255,0.3);
    box-shadow:
        0 0 15px #00f2ff,
        0 0 30px #ff00ff,
        inset 0 0 15px #00ffcc;
    animation:fadeIn 1.5s ease;
}

@keyframes fadeIn{
    from{opacity:0; transform:scale(0.8);}
    to{opacity:1; transform:scale(1);}
}

h1{
    font-size:40px;
    color:#00f2ff;
    text-shadow:
        0 0 5px #00f2ff,
        0 0 10px #00f2ff,
        0 0 20px #ff00ff;
    margin-bottom:20px;
    animation:glowText 2s infinite alternate;
}

@keyframes glowText{
    from{text-shadow:0 0 5px #00f2ff,0 0 10px #ff00ff;}
    to{text-shadow:0 0 20px #00f2ff,0 0 40px #ff00ff;}
}

p{
    color:#aaa;
    margin-bottom:30px;
}

/* Neon Button */
.btn{
    padding:15px 40px;
    font-size:16px;
    border:none;
    border-radius:50px;
    cursor:pointer;
    background:transparent;
    color:#00f2ff;
    border:2px solid #00f2ff;
    position:relative;
    transition:0.3s;
}

.btn:hover{
    background:#00f2ff;
    color:#0f0f1a;
    box-shadow:
        0 0 10px #00f2ff,
        0 0 20px #00f2ff,
        0 0 40px #ff00ff;
    transform:scale(1.1);
}

/* Floating particles */
.particle{
    position:absolute;
    width:4px;
    height:4px;
    background:#00f2ff;
    border-radius:50%;
    animation:float 5s infinite linear;
}

@keyframes float{
    from{transform:translateY(100vh) scale(0);}
    to{transform:translateY(-10vh) scale(1);}
}

</style>
</head>

<body>

<div class="card">
    <h1>⚡ NEON DARK MODE ⚡</h1>
    <p>Website cực chất – hiệu ứng phát sáng + chuyển động mượt 🔥</p>
    <button class="btn" onclick="showAlert()">Click thử đi</button>
</div>

<script>
function showAlert(){
    alert("🚀 Bạn vừa kích hoạt chế độ Hacker Neon!");
}

/* Create floating particles */
for(let i=0;i<30;i++){
    let p = document.createElement("div");
    p.classList.add("particle");
    p.style.left = Math.random()*100 + "vw";
    p.style.animationDuration = (Math.random()*5+5)+"s";
    p.style.opacity = Math.random();
    document.body.appendChild(p);
}
</script>

</body>
</html>
""")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


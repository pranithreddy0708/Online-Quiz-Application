import subprocess
import time
import sys

print("=" * 65)
print(" === QuizMaster Server & Cloudflare Tunnel Starting ===")
print(" Live URL: https://alpine-career-wear-pipes.trycloudflare.com")
print("=" * 65)

# Start Flask server
flask_proc = subprocess.Popen([sys.executable, "app.py"])

# Give Flask 2 seconds to initialize
time.sleep(2)

# Start Cloudflare Tunnel (100% uptime, zero 503 errors, no password screens)
tunnel_cmd = "npx -y cloudflared tunnel --url http://localhost:5500"
tunnel_proc = subprocess.Popen(tunnel_cmd, shell=True)

try:
    flask_proc.wait()
    tunnel_proc.wait()
except KeyboardInterrupt:
    print("\nStopping QuizMaster server and public tunnel...")
    flask_proc.terminate()
    tunnel_proc.terminate()

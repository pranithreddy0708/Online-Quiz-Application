import subprocess
import time
import sys

print("=" * 65)
print(" === QuizMaster Server & Public Tunnel Starting ===")
print(" Universal Live URL: https://online-quiz-application.loca.lt")
print("=" * 65)

# Start Flask server
flask_proc = subprocess.Popen([sys.executable, "app.py"])

# Give Flask 2 seconds to initialize
time.sleep(2)

# Start localtunnel daemon with professional subdomain
tunnel_cmd = "npx -y localtunnel --port 5500 --subdomain online-quiz-application"
tunnel_proc = subprocess.Popen(tunnel_cmd, shell=True)

try:
    flask_proc.wait()
    tunnel_proc.wait()
except KeyboardInterrupt:
    print("\nStopping QuizMaster server and public tunnel...")
    flask_proc.terminate()
    tunnel_proc.terminate()

import os, sys, requests
HOST = os.environ.get("TARGET_HOST", "192.168.1.120")  # pon la IP REAL de tu Pi
PORT = int(os.environ.get("TARGET_PORT", "5000"))
TEXT = " ".join(sys.argv[1:]) or os.environ.get("MESSAGE", "Hola desde Steam Deck!")
url = f"http://{HOST}:{PORT}/message"
r = requests.post(url, json={"text": TEXT}, timeout=5)
print("status:", r.status_code)
print("response:", r.text)

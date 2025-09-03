from flask import Flask, request
app = Flask(__name__)

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    print(f"[RECEIVED] {text}", flush=True)   # se verá en `docker logs`
    return {"ok": True, "echo": text}

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

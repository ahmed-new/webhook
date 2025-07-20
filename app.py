from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "netgenius"  # نفس التوكن اللي كتبته في إعدادات فيسبوك
N8N_URL = "https://ahmeddev.app.n8n.cloud/webhook/23044787-0b7d-4756-b643-19f90aa65b42"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == "POST":
        # إرسال البيانات إلى n8n
        try:
            response = requests.post(N8N_URL, json=request.json)
            return "Forwarded to n8n", response.status_code
        except Exception as e:
            return f"Error: {str(e)}", 500

    return "Method not allowed", 405

if __name__ == "__main__":
    app.run()

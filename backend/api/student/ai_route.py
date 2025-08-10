import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from your Vue frontend

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

@app.route("/api/child/chat", methods=["POST"])
def chat_with_ai():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Prepare request to Gemini API
    payload = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }

    # Send request to Gemini API
    response = requests.post(
        GEMINI_URL,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": "Gemini API request failed", "details": response.text}), 500

    result = response.json()
    ai_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return jsonify({"reply": ai_text})


import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# Enable CORS for all routes to allow your frontend to communicate with this backend
CORS(app)

# Initialize OpenAI client with Groq API key from environment variables
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 1. Added a root route to prevent 405 errors when visiting the base URL
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "Aegis Backend is live and running!"}), 200

# 2. Main processing route
@app.route("/submit", methods=["POST"])
def process_assessment():
    try:
        data = request.get_json()
        if not data or 'problem' not in data:
            return jsonify({"error": "No 'problem' field found in request"}), 400
            
        user_issue = data['problem']
        
        # Chat completion logic
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a legal compliance engineer."},
                {"role": "user", "content": user_issue}
            ],
            model="llama3-8b-8192",
        )
        
        return jsonify({"analysis": chat_completion.choices[0].message.content}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()







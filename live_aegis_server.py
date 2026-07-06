import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client using the environment variable
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# This route handles the root URL for browser GET requests
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "Aegis Backend is ready."}), 200

# This route handles the POST requests for your logic
@app.route("/submit", methods=["POST"])
def process_assessment():
    try:
        data = request.get_json()
        if not data or 'problem' not in data:
            return jsonify({"error": "Missing 'problem' field in JSON body"}), 400
            
        user_issue = data['problem']
        
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








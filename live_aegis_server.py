import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# Configure CORS to allow cross-origin requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize the client
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

# Root route for health checks
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "active", "message": "Aegis Backend is live."}), 200

# Submit route with explicit OPTIONS handling for CORS
@app.route("/submit", methods=["POST", "OPTIONS"])
def process_assessment():
    if request.method == "OPTIONS":
        return '', 200
    
    try:
        data = request.get_json()
        if not data or 'problem' not in data:
            return jsonify({"error": "Missing 'problem' field"}), 400
            
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






from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# Replace '*' with your actual GitHub Pages URL once you have it, for better security
CORS(app, resources={r"/submit": {"origins": "*"}})

client = OpenAI(
    api_key="os.environ.get("GROQ_API_KEY")

",
    base_url="https://api.groq.com/openai/v1"
)

@app.route('/submit', methods=['POST'])
def process_assessment():
    try:
        data = request.get_json()
        user_issue = data.get('problem', '')
        # Adding system context for better AI performance
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a legal compliance engine."},
                {"role": "user", "content": user_issue}
            ],
            model="llama3-8b-8192",
        )
        return jsonify({"analysis": chat_completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500






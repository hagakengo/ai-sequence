from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__, static_folder='../')

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route('/')
def index():
    return send_from_directory('../', 'index.html')

@app.route('/api', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get('input')
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "あなたは優秀なPMです。設計図を作成してください。"},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"content": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"content": f"エラーが発生しました: {str(e)}"}), 500
from flask import Flask, request, jsonify, send_from_directory
import openai
import os

# Vercelが認識するための窓口
app = Flask(__name__, static_folder='.')

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route('/')
def index():
    # トップページとして index.html を返す
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get('input')
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "あなたは優秀なPMです。"},
            {"role": "user", "content": user_input}
        ]
    )
    return jsonify({"content": response.choices[0].message.content})
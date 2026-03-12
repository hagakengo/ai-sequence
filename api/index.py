import os
import requests
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    if not db_url: return
    try:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        with psycopg2.connect(db_url, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS designs (id SERIAL PRIMARY KEY, user_input TEXT, ai_content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
                cur.execute("INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)", (user_input, ai_content))
                conn.commit()
    except Exception as e:
        print(f"DB ERROR: {e}")

@app.route('/api', methods=['POST'])
def generate():
    try:
        data = request.json
        user_input = data.get('input', '')
        api_key = os.environ.get('GROQ_API_KEY')
        
        # 修正ポイント: URLに余計な [] や () を含めない
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"{user_input}。必ずmermaid形式のsequenceDiagramコードを```mermaid ... ```で囲って出力してください。"}]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        ai_content = response.json()['choices'][0]['message']['content']
        
        save_to_db(user_input, ai_content)
        return jsonify({"content": ai_content})
    except Exception as e:
        return jsonify({"content": f"Error: {str(e)}"}), 500
import os
import requests
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    if not db_url: return
    try:
        # postgres:// を postgresql:// に修正（psycopg2の仕様対応）
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        with psycopg2.connect(db_url, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS designs (id SERIAL PRIMARY KEY, user_input TEXT, ai_content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
                cur.execute("INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)", (user_input, ai_content))
                conn.commit()
        print("DEBUG: DB SAVE SUCCESS")
    except Exception as e:
        print(f"DEBUG: DB ERROR -> {e}")

@app.route('/api', methods=['POST'])
def generate():
    try:
        data = request.json
        user_input = data.get('input', '')
        
        api_key = os.environ.get('GROQ_API_KEY')
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"{user_input}。必ずmermaid形式のsequenceDiagramコードを```mermaid ... ```で囲って出力してください。"}]
        }
        
        response = requests.post("[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)", json=payload, headers=headers)
        ai_content = response.json()['choices'][0]['message']['content']
        
        save_to_db(user_input, ai_content)
        
        return jsonify({"content": ai_content})
    except Exception as e:
        return jsonify({"content": f"Error: {str(e)}"}), 500
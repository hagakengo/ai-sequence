import os
import requests
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_conn():
    db_url = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url, sslmode='require')

@app.route('/api', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get('input', '')
    api_key = os.environ.get('GROQ_API_KEY')
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Mermaidのシーケンス図のみ生成すること。Note overでの複数人指定は禁止。必ず正確なMermaid構文で出力せよ。"},
            {"role": "user", "content": f"{user_input} をMermaidシーケンス図で出力。```mermaid で囲むこと。"}
        ]
    }
    
    res = requests.post(url, json=payload, headers=headers).json()
    ai_content = res['choices'][0]['message']['content']
    
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS designs (id SERIAL PRIMARY KEY, user_input TEXT, ai_content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
            cur.execute("INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)", (user_input, ai_content))
            conn.commit()
            
    return jsonify({"content": ai_content})

@app.route('/api/history', methods=['GET'])
def history():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_input, ai_content FROM designs ORDER BY created_at DESC LIMIT 5;")
            return jsonify([{"input": r[0], "content": r[1]} for r in cur.fetchall()])
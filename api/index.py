import os
import psycopg2
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Neonへの保存処理
def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS designs (id SERIAL PRIMARY KEY, user_input TEXT, ai_content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        cur.execute("INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)", (user_input, ai_content))
        conn.commit()
        cur.close()
        conn.close()
        print("DEBUG: SUCCESS SAVED")
    except Exception as e:
        print(f"DEBUG: ERROR -> {str(e)}")

@app.route('/api', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get('input', '')
    
    # Groq APIへのリクエスト（mermaidを強制するプロンプト）
    headers = {"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"{user_input}。必ず以下のようにMermaidのコードをMarkdown形式で囲んで出力してください。```mermaid\n(ここにコード)\n```"}]
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    ai_content = response.json()['choices'][0]['message']['content']
    
    # DBに保存
    save_to_db(user_input, ai_content)
    
    return jsonify({"content": ai_content})

if __name__ == '__main__':
    app.run()
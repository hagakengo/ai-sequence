import os
import requests
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DEBUG: DATABASE_URL is missing")
        return
    try:
        # Vercel/psycopg2互換性のための修正
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
            
        with psycopg2.connect(db_url, sslmode='require') as conn:
            with conn.cursor() as cur:
                # テーブル作成（存在しない場合）
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS designs (
                        id SERIAL PRIMARY KEY,
                        user_input TEXT,
                        ai_content TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                # データ挿入
                cur.execute(
                    "INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)",
                    (user_input, ai_content)
                )
                conn.commit()
        print("DEBUG: DB saved successfully")
    except Exception as e:
        print(f"DEBUG: DB error -> {e}")

@app.route('/api', methods=['POST'])
def generate():
    try:
        data = request.json
        user_input = data.get('input', '')
        
        # Groq API設定
        api_key = os.environ.get('GROQ_API_KEY')
        url = "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system", 
                    "content": "あなたはプロのシステムエンジニアです。ユーザーの要望をシーケンス図に変換します。"
                },
                {
                    "role": "user", 
                    "content": f"{user_input}。必ずmermaid形式のsequenceDiagramコードを```mermaid ... ```で囲って出力してください。"
                }
            ],
            "temperature": 0.7
        }
        
        # AIリクエスト
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        ai_content = response.json()['choices'][0]['message']['content']
        
        # データベース保存（バックグラウンドではなく確実に行う）
        save_to_db(user_input, ai_content)
        
        return jsonify({"content": ai_content})
        
    except Exception as e:
        print(f"DEBUG: Global error -> {e}")
        return jsonify({"content": f"サーバーエラー: {str(e)}"}), 500
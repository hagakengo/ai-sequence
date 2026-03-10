import os
import psycopg2  # 追加
from flask import Flask, request, jsonify, send_from_directory
import openai

app = Flask(__name__, static_folder='../')

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# データベース接続関数
def save_to_db(user_input, ai_content):
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()
        # テーブル作成（存在しなければ作成）
        cur.execute('''
            CREATE TABLE IF NOT EXISTS designs (
                id SERIAL PRIMARY KEY,
                user_input TEXT,
                ai_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        # データ保存
        cur.execute(
            "INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)",
            (user_input, ai_content)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB保存エラー: {e}")

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
                {"role": "system", "content": "あなたはITコンサルタント兼PMです。概要、Mermaid形式のシーケンス図、補足説明の形式で回答してください。"},
                {"role": "user", "content": user_input}
            ]
        )
        ai_content = response.choices[0].message.content
        
        # ★ここでDB保存処理を呼び出す
        save_to_db(user_input, ai_content)
        
        return jsonify({"content": ai_content})
    except Exception as e:
        return jsonify({"content": f"エラーが発生しました: {str(e)}"}), 500
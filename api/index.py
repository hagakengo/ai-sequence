import os
import psycopg2
from flask import Flask, request, jsonify, send_from_directory
import openai

app = Flask(__name__, static_folder='../')

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# 保存関数をここに配置
def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS designs (
                id SERIAL PRIMARY KEY,
                user_input TEXT,
                ai_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        cur.execute("INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)", (user_input, ai_content))
        conn.commit()
        cur.close()
        conn.close()
        print("DEBUG: DB Save Success!")
    except Exception as e:
        print(f"DEBUG: DB ERROR IS -> {str(e)}")

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
                {"role": "system", "content": "あなたはPMです。Mermaid形式のシーケンス図コードを必ず含めてください。"},
                {"role": "user", "content": user_input}
            ]
        )
        ai_content = response.choices[0].message.content
        
        # ★ここ！ここで関数を呼び出します
        save_to_db(user_input, ai_content)
        
        return jsonify({"content": ai_content})
    except Exception as e:
        return jsonify({"content": f"エラーが発生しました: {str(e)}"}), 500
print("DEBUG: NEW DEPLOYMENT ACTIVE")
import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# 保存関数
def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    print(f"DEBUG: Start saving... URL exists: {db_url is not None}") # 確実にログを出す
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
    print(f"DEBUG: API Called with input: {user_input[:20]}") # リクエストが届いたことを確認
    
    # AI処理は省略しますが、ここを維持してください
    ai_content = "ここにAIの生成結果" 
    
    # 呼び出し
    save_to_db(user_input, ai_content)
    
    return jsonify({"content": ai_content})
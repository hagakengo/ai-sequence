import os
import psycopg2

def save_to_db(user_input, ai_content):
    db_url = os.environ.get("DATABASE_URL")
    
    # 接続確認用のログ出力
    print(f"DEBUG: Connecting to {db_url}")
    
    try:
        # sslmode=require を強制付与して接続
        conn = psycopg2.connect(db_url, sslmode='require')
        cur = conn.cursor()
        
        # テーブル作成
        cur.execute('''
            CREATE TABLE IF NOT EXISTS designs (
                id SERIAL PRIMARY KEY,
                user_input TEXT,
                ai_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute(
            "INSERT INTO designs (user_input, ai_content) VALUES (%s, %s)",
            (user_input, ai_content)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("DEBUG: DB Save Success!")
    except Exception as e:
        # ここが超重要：エラーが出たらVercelのLogsに全情報が出る
        print(f"DEBUG: DB ERROR IS -> {str(e)}")
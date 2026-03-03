import openai
import os
from dotenv import load_dotenv # python-dotenvライブラリが必要

load_dotenv() # .envファイルの内容を読み込む

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY") # 隠したキーを呼び出す
)

print("--- 🛠️ シーケンス図自動作成 ---")
user_input = input("開発フローを詳細化したい機能を教えてください\n（例：Amazonの注文確定処理、パスワードリセットなど）\n入力 > ")

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": """あなたはテックリード経験のあるシニアPMです。
                ユーザーの入力を元に、実装レベルの設計図を出力してください。

                1. 【開発用シーケンス図 (sequenceDiagram)】
                   - 登場人物: User, Frontend, API Gateway, Microservice, Database, External API (Stripe等)
                   - メソッド名 (POST / GET / PUT) や、成功/失敗のループ (alt / opt) を含めてください。
                   - Notionでエラーが出ないようシンプルな構文を使用してください。

                2. 【技術仕様メモ】
                   - 必要なAPIエンドポイント例 (例: POST /orders)
                   - DBに保存すべき主要なカラム名
                   - 異常系（通信エラーや在庫不足）の挙動
                """
            },
            {"role": "user", "content": user_input}
        ]
    )
    
    print("\n" + "⚙️ 開発用設計データが生成されました" + "\n" + "="*50)
    print(response.choices[0].message.content)
    print("="*50)

except Exception as e:
    print(f"エラー: {e}")
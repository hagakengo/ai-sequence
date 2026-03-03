import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv()


client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


st.set_page_config(page_title="PMアシスタント", page_icon="⚙️")
st.title("🛠️ シーケンス図自動作成")
st.caption("テックリード経験のあるシニアPMが、あなたのアイデアを設計図にします。")


user_input = st.text_input("開発フローを詳細化したい機能を教えてください", 
                          placeholder="例：Amazonの注文確定処理")

if st.button("設計図を生成する"):
    if not user_input:
        st.warning("機能を記入してください")
    else:
        with st.spinner("孤独なおっさんが思考中..."):
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
                
                
                st.success("⚙️ 開発用設計データが生成されました")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                st.markdown("---")

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
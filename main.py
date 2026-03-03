import streamlit as st
import openai
import os
import sys
from dotenv import load_dotenv

# Vercel環境下でStreamlitを起動するための設定
if '__file__' in locals():
    load_dotenv()

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def main():
    st.set_page_config(page_title="PMアシスタント", page_icon="⚙️")
    st.title("🛠️ シーケンス図自動作成")
    
    user_input = st.text_input("機能を教えてください", placeholder="例：ログイン処理")
    
    if st.button("設計図を生成"):
        if user_input:
            with st.spinner("生成中..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "あなたはシニアPMです。"},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    st.success("生成完了")
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
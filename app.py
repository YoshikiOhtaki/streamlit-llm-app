from dotenv import load_dotenv

load_dotenv()

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


def get_system_message(selected_role: str) -> str:
    role_prompts = {
        "AIエンジニア": (
            "あなたはAIエンジニアの専門家です。"
            "Python、LangChain、RAG、AIエージェントの観点から、"
            "実務で使えるように具体的かつわかりやすく日本語で回答してください。"
        ),
        "マーケティングコンサルタント": (
            "あなたはマーケティングコンサルタントの専門家です。"
            "集客、販売導線、SNS、広告、顧客理解の観点から、"
            "実践的でわかりやすい日本語で回答してください。"
        ),
    }
    return role_prompts[selected_role]


def generate_response(user_input: str, expert_type: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY が設定されていません。.env を確認してください。")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5,
        api_key=api_key
    )

    system_message = get_system_message(expert_type)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input),
    ]

    result = llm.invoke(messages)
    return result.content


st.title("LLM専門家アドバイザー")

st.write("### アプリ概要")
st.write("このアプリは、選択した専門家タイプに応じてLLMが回答を生成するWebアプリです。")

st.write("### 操作方法")
st.write("1. 専門家タイプを選択してください。")
st.write("2. 質問を入力してください。")
st.write("3. 送信ボタンを押すと回答が表示されます。")

expert_type = st.radio(
    "専門家タイプを選択してください。",
    ["AIエンジニア", "マーケティングコンサルタント"]
)

user_input = st.text_input("質問を入力してください。")

if st.button("送信"):
    if not user_input.strip():
        st.error("質問を入力してください。")
    else:
        try:
            answer = generate_response(user_input=user_input, expert_type=expert_type)
            st.divider()
            st.write("### 回答")
            st.write(answer)
        except Exception as error:
            st.error(f"エラーが発生しました: {error}")
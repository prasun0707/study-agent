
import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = "gemini-2.5-flash"

st.title("Study Helper Agent")

if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {
            "role": "system",
            "content": "You are a friendly study helper. Explain simply with examples."
        }
    ]

for m in st.session_state.msgs[1:]:
    st.chat_message(m["role"]).write(m["content"])

if q := st.chat_input("Ask anything"):
    st.session_state.msgs.append({"role": "user", "content": q})
    st.chat_message("user").write(q)

    r = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.msgs
    )

    a = r.choices[0].message.content
    st.session_state.msgs.append({"role": "assistant", "content": a})
    st.chat_message("assistant").write(a)
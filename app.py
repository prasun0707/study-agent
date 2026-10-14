
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Study Helper AI",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Keep your existing Gemini integration and secret
client = OpenAI(
    api_key=st.secrets["API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = (
    "You are a friendly study helper for students. "
    "Explain concepts simply, use examples, organize answers with headings "
    "and bullet points when useful, and encourage learning."
)

# Clean white-and-blue styling
st.markdown(
    """
    <style>
    .stApp {
        background: #f7faff;
    }

    [data-testid="stHeader"] {
        background: rgba(247, 250, 255, 0.95);
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(135deg, #ffffff, #eaf3ff);
        border: 1px solid #d9e8ff;
        border-radius: 22px;
        padding: 28px 26px;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: #153b70;
        font-size: 2.25rem;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #55708f;
        font-size: 1rem;
        margin: 0;
    }

    .section-label {
        color: #244b7c;
        font-weight: 650;
        font-size: 1rem;
        margin: 12px 0;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #cbdcf5;
        background: white;
        color: #204c83;
        min-height: 46px;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        border-color: #4785dc;
        background: #edf5ff;
        color: #153b70;
    }

    div.stButton > button[kind="primary"] {
        background: #2563eb;
        color: white;
        border: 1px solid #2563eb;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #1d4ed8;
        color: white;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #e1eaf7;
        border-radius: 16px;
        padding: 12px 16px;
        background: white;
    }

    [data-testid="stChatInput"] {
        border-color: #cbdcf5;
    }

    .footer {
        text-align: center;
        color: #7185a0;
        font-size: 0.82rem;
        padding-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Start or restore the conversation
if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Header
header_col, action_col = st.columns([5, 1.5])

with header_col:
    st.markdown(
        """
        <div class="hero">
            <h1>📘 Study Helper AI</h1>
            <p>Your personal AI study partner. Learn smarter, one question at a time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with action_col:
    st.write("")
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.msgs = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.session_state.pop("pending_prompt", None)
        st.rerun()

# Quick prompts
st.markdown(
    '<div class="section-label">✨ What would you like to study?</div>',
    unsafe_allow_html=True,
)

prompts = [
    ("💡 Explain a topic", "Explain a difficult topic in simple words with an example."),
    ("📝 Make study notes", "Help me make clear, exam-ready study notes on a topic."),
    ("🧠 Test my knowledge", "Quiz me on a topic with 5 questions, one at a time."),
    ("📚 Give an example", "Teach me a concept using a practical, real-world example."),
]

prompt_cols = st.columns(2)

for i, (label, prompt_text) in enumerate(prompts):
    with prompt_cols[i % 2]:
        if st.button(label, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_prompt = prompt_text
            st.rerun()

st.divider()

# Conversation history
for message in st.session_state.msgs[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and quick-prompt handling
typed_prompt = st.chat_input("Ask a question or tell me what you're studying...")

if "pending_prompt" in st.session_state:
    question = st.session_state.pop("pending_prompt")
else:
    question = typed_prompt

if question:
    st.session_state.msgs.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking through your question..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.msgs,
                )

            answer = response.choices[0].message.content
            if not answer:
                answer = "I couldn't generate a response. Please try again."

            st.markdown(answer)
            st.session_state.msgs.append(
                {"role": "assistant", "content": answer}
            )

        except Exception:
            st.warning(
                "I couldn't get a response right now. "
                "Please try again in a moment. Your conversation is still here."
            )

st.markdown(
    '<div class="footer">Made for curious minds · Keep learning, keep growing ✨</div>',
    unsafe_allow_html=True,
)

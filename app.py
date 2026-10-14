
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Study Helper AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

client = OpenAI(
    api_key=st.secrets["API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = "gemini-3.8-flash"

MODES = {
    "Flashcards": (
        "Create 10 useful revision flashcards. Give each a clear question "
        "and answer, focusing on key definitions and concepts."
    ),
    "Explain It Back": (
        "Explain the topic simply, then give me a short exercise to check "
        "my understanding. Invite me to explain it back in my own words."
    ),
    "My Notes": (
        "Create organized, exam-ready notes with headings, definitions, "
        "key points, examples, and a short revision summary."
    ),
    "Practice Quiz": (
        "Create 5 MCQs with four options each. Put the answer key and "
        "brief explanations at the end so I can try first."
    ),
    "Explain a Topic": (
        "Explain this topic in simple language, step by step, with examples."
    ),
}

SYSTEM = (
    "You are a friendly and accurate AI study coach. "
    "Help students understand concepts, use clear formatting, and "
    "encourage active learning. Be honest if you are uncertain."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Flashcards"
if "pending_topic" not in st.session_state:
    st.session_state.pending_topic = ""

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background: #f6f9fc;
    color: #172b3a;
}
[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(120deg, #10b981 0%, #078b9c 100%);
    border-radius: 24px;
    padding: 30px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px rgba(8, 145, 140, 0.13);
}
.hero h1, .hero h2, .hero p, .hero span {
    color: white !important;
}
.hero .eyebrow {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1.3px;
    opacity: 0.85;
}
.hero h1 {
    font-size: clamp(1.65rem, 4vw, 2.35rem);
    line-height: 1.2;
    margin: 10px 0;
}
.hero p {
    font-size: 1rem;
    max-width: 650px;
    opacity: 0.94;
}
.section-title {
    font-size: 1.18rem;
    font-weight: 750;
    color: #18334a;
    margin: 20px 0 10px 0;
}
.tool-card {
    background: #ffffff;
    border: 1px solid #e2e9f0;
    border-radius: 18px;
    padding: 20px;
    min-height: 160px;
    box-shadow: 0 3px 12px rgba(22, 44, 66, 0.035);
}
.tool-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: #f0e7ff;
    color: #8b3dce;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    margin-bottom: 14px;
}
.tool-card h3 {
    color: #172b3a !important;
    font-size: 1.05rem;
    margin: 0 0 6px 0;
}
.tool-card p {
    color: #6b7c8f !important;
    font-size: 0.9rem;
    margin: 0;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    border: 1px solid #dfe7ef;
    background: #ffffff;
    color: #243e55 !important;
    font-weight: 600;
}
div.stButton > button:hover {
    border-color: #0d9488;
    background: #f0fdfa;
    color: #0f766e !important;
}
div.stButton > button[kind="primary"] {
    background: #ffffff;
    border-color: #ffffff;
    color: #087f70 !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #e8fffa;
}
.assessment {
    background: #e4fbfa;
    border: 1px solid #b8eeea;
    border-radius: 16px;
    padding: 16px 18px;
    color: #176b70;
    margin: 20px 0 12px 0;
}
.assessment strong {
    color: #176b70;
}
[data-testid="stChatMessage"] {
    background: white !important;
    border: 1px solid #e2e9f0;
    border-radius: 16px;
    color: #172b3a !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #172b3a !important;
}
.footer {
    text-align: center;
    color: #8291a2;
    font-size: 0.82rem;
    padding: 22px 0 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
top_left, top_right = st.columns([5, 1])

with top_left:
    st.markdown("### 📚 Study Helper AI")
with top_right:
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_topic = ""
        st.session_state.mode = "Flashcards"
        st.rerun()

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR AI STUDY COACH</div>
    <h1>A quick 5-minute study session</h1>
    <p>Small, focused sessions make learning easier.
    Choose a tool below and start learning at your own pace.</p>
</div>
""", unsafe_allow_html=True)

hero_left, hero_right = st.columns([1, 1])

with hero_left:
    if st.button("📚  Review flashcards  →", type="primary",
                 use_container_width=True):
        st.session_state.mode = "Flashcards"
        st.session_state.pending_topic = "Help me revise an important topic"
        st.rerun()

with hero_right:
    if st.button("💡  Explain a topic", use_container_width=True):
        st.session_state.mode = "Explain a Topic"
        st.session_state.pending_topic = ""
        st.rerun()

# ---------- Quick tools ----------
st.markdown(
    '<div class="section-title">⚡ Quick tools</div>',
    unsafe_allow_html=True,
)

quick_cols = st.columns(3)
quick_tools = [
    ("🎙️ Explain It Back", "Explain It Back"),
    ("🗂️ Flashcards", "Flashcards"),
    ("📝 My Notes", "My Notes"),
]

for col, (label, mode) in zip(quick_cols, quick_tools):
    with col:
        if st.button(label, key=f"quick_{mode}", use_container_width=True):
            st.session_state.mode = mode
            st.session_state.pending_topic = ""
            st.rerun()

# ---------- Feature cards ----------
st.markdown(
    '<div class="section-title">Choose your study tool</div>',
    unsafe_allow_html=True,
)

card_cols = st.columns(3)
cards = [
    ("🗂️", "Flashcards", "Quick spaced-repetition style revision."),
    ("🎙️", "Explain It Back", "Understand a concept and check your understanding."),
    ("📝", "My Notes", "Turn a topic into clear, structured study notes."),
]

for col, (icon, title, description) in zip(card_cols, cards):
    with col:
        st.markdown(f"""
        <div class="tool-card">
            <div class="tool-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Start →", key=f"start_{title}",
                     use_container_width=True):
            st.session_state.mode = title
            st.session_state.pending_topic = ""
            st.rerun()

# ---------- Assessment banner ----------
st.markdown("""
<div class="assessment">
    <strong>📄 Got an assessment or assignment?</strong><br>
    Upload support can be added next so you can generate practice questions
    from your own study material.
</div>
""", unsafe_allow_html=True)

# ---------- Study workspace ----------
st.markdown(
    f'<div class="section-title">✍️ Study workspace · {st.session_state.mode}</div>',
    unsafe_allow_html=True,
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

typed_topic = st.chat_input("Ask a question or enter a topic to study...")

topic = typed_topic
if st.session_state.pending_topic:
    topic = st.session_state.pending_topic
    st.session_state.pending_topic = ""

if topic:
    mode = st.session_state.mode
    st.session_state.messages.append(
        {"role": "user", "content": f"**{mode}:** {topic}"}
    )

    with st.chat_message("user"):
        st.markdown(f"**{mode}:** {topic}")

    api_messages = [{"role": "system", "content": SYSTEM}]
    for msg in st.session_state.messages[:-1]:
        api_messages.append(msg)

    api_messages.append({
        "role": "user",
        "content": (
            f"Study mode: {mode}\n"
            f"Topic or request: {topic}\n"
            f"Instructions: {MODES[mode]}"
        ),
    })

    with st.chat_message("assistant"):
        try:
            with st.spinner("Preparing your study session..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                )

            answer = response.choices[0].message.content
            if not answer:
                answer = "I couldn't generate a response. Please try again."

            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception:
            st.warning(
                "The AI service is temporarily unavailable. "
                "Please try again in a moment."
            )

st.markdown(
    '<div class="footer">Made for curious minds · Keep learning, keep growing ✨</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="footer">Made for curious minds · Keep learning, keep growing ✨</div>',
    unsafe_allow_html=True,
)

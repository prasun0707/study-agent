
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Study Helper AI",
    page_icon="📘",
    layout="centered",
)

client = OpenAI(
    api_key=st.secrets["API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = "gemini-3.8-flash"

MODES = {
    "Explain": {
        "icon": "💡",
        "description": "Understand difficult concepts simply.",
        "instruction": (
            "Explain the topic in simple language. Use clear headings, "
            "step-by-step explanations, and practical examples."
        ),
    },
    "Study Notes": {
        "icon": "📝",
        "description": "Create structured, exam-ready notes.",
        "instruction": (
            "Create well-organized study notes with headings, definitions, "
            "key points, examples, and a short revision summary."
        ),
    },
    "Flashcards": {
        "icon": "🗂️",
        "description": "Revise with questions and answers.",
        "instruction": (
            "Create 10 useful flashcards. Format each as a question followed "
            "by its answer. Focus on important definitions, concepts, and facts."
        ),
    },
    "Practice Quiz": {
        "icon": "🧠",
        "description": "Test yourself with multiple-choice questions.",
        "instruction": (
            "Create 5 multiple-choice questions with four options each. "
            "Put the answer key and a short explanation after all questions "
            "so the student can attempt them first."
        ),
    },
}

SYSTEM_PROMPT = (
    "You are Study Helper AI, a friendly and accurate study tutor. "
    "Help students learn rather than merely memorize. Use clear formatting, "
    "correct mistakes gently, and never invent facts when uncertain."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "study_mode" not in st.session_state:
    st.session_state.study_mode = "Explain"

# White-and-blue theme with explicit text contrast
st.markdown(
    """
    <style>
    .stApp {
        background: #F5F8FF;
        color: #172B4D;
    }

    [data-testid="stHeader"] {
        background: #F5F8FF;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        color: #172B4D;
    }

    .hero {
        background: linear-gradient(135deg, #FFFFFF, #EAF2FF);
        border: 1px solid #D7E5F7;
        border-radius: 22px;
        padding: 26px;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: #16345C !important;
        font-size: 2.25rem;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #526987 !important;
        margin: 0;
        font-size: 1rem;
    }

    .section-label {
        color: #16345C;
        font-weight: 700;
        font-size: 1.08rem;
        margin: 18px 0 10px 0;
    }

    div.stButton > button {
        width: 100%;
        min-height: 48px;
        background: #FFFFFF;
        color: #16345C !important;
        border: 1px solid #D0DFF3;
        border-radius: 12px;
        white-space: normal;
    }

    div.stButton > button:hover {
        background: #EAF2FF;
        border-color: #2563EB;
        color: #16345C !important;
    }

    div.stButton > button[kind="primary"] {
        background: #2563EB;
        border-color: #2563EB;
        color: #FFFFFF !important;
    }

    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1px solid #D7E5F7;
        border-radius: 16px;
        padding: 14px;
        color: #172B4D !important;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #172B4D !important;
    }

    [data-testid="stChatInput"] {
        border-color: #BFD3F2;
    }

    .footer {
        text-align: center;
        color: #647B99;
        font-size: 0.82rem;
        padding-top: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header and new-chat button
header_col, action_col = st.columns([4, 1.4])

with header_col:
    st.markdown(
        """
        <div class="hero">
            <h1>📘 Study Helper AI</h1>
            <p>Your personal AI learning workspace. Learn smarter, one topic at a time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with action_col:
    st.write("")
    if st.button("＋ New chat", key="new_chat"):
        st.session_state.messages = []
        st.session_state.study_mode = "Explain"
        st.rerun()

# Study mode selector
st.markdown(
    '<div class="section-label">What would you like to study?</div>',
    unsafe_allow_html=True,
)

mode_names = list(MODES.keys())
mode_cols = st.columns(2)

for index, mode in enumerate(mode_names):
    with mode_cols[index % 2]:
        selected = st.session_state.study_mode == mode
        button_label = (
            f"{MODES[mode]['icon']}  {mode}"
            + ("  ✓" if selected else "")
        )

        if st.button(
            button_label,
            key=f"mode_{mode}",
            type="primary" if selected else "secondary",
            help=MODES[mode]["description"],
        ):
            st.session_state.study_mode = mode
            st.rerun()

active_mode = st.session_state.study_mode
st.caption(
    f"{MODES[active_mode]['icon']} {MODES[active_mode]['description']}"
)

st.divider()

# Conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Topic input
topic = st.chat_input(
    f"Enter a topic for {active_mode.lower()}..."
)

if topic:
    user_message = (
        f"Study mode: {active_mode}\n"
        f"Topic or request: {topic}\n\n"
        f"Instructions: {MODES[active_mode]['instruction']}"
    )

    st.session_state.messages.append(
        {"role": "user", "content": topic}
    )

    with st.chat_message("user"):
        st.markdown(f"**{active_mode}:** {topic}")

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for message in st.session_state.messages:
        if message["role"] == "user" and message["content"] == topic:
            api_messages.append(
                {"role": "user", "content": user_message}
            )
        else:
            api_messages.append(message)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Preparing your study material..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                )

            answer = response.choices[0].message.content
            if not answer:
                answer = "I couldn't generate an answer. Please try again."

            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception:
            st.warning(
                "I couldn't get a response right now. "
                "Please try again in a moment."
            )

st.markdown(
    '<div class="footer">Made for curious minds · Keep learning, keep growing ✨</div>',
    unsafe_allow_html=True,
)

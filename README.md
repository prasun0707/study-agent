
# 📘 Study Helper AI

A simple AI-powered study assistant built with Streamlit and Google's Gemini model. It helps students understand difficult concepts, prepare study notes, and learn through interactive conversations.

🔗 **Live Demo:** https://study-agent-9tvz3fbbdbnasyxisrm6jg.streamlit.app/

## ✨ Features

- 💬 **AI Chat:** Ask questions and get clear, student-friendly explanations.
- ⚡ **Quick Prompts:** Start studying with ready-made prompts.
- 📝 **Study Notes:** Get help creating exam-ready notes.
- 🧠 **Learning Support:** Explore concepts with practical examples.
- 🔄 **New Chat:** Start a fresh conversation whenever needed.
- 🎨 **Clean UI:** A responsive, white-and-blue interface.

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- OpenAI Python SDK (for Gemini's compatible API)

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/prasun0707/study-agent.git
cd study-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

Create a `.streamlit/secrets.toml` file with:

```toml
API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key. Never commit this file or publish your key.

### 4. Run the app

```bash
streamlit run app.py
```

## 🔐 Security

- API credentials are stored separately from application code.
- Never share or commit API keys.
- Keep local secrets files out of version control.

## 👨‍💻 Author

**Prasun Kumar**

- GitHub: [@prasun0707](https://github.com/prasun0707)

---

Built as a learning project to explore Python, AI APIs, and Streamlit deployment.

# 🕵️ Agent Vinod
### *Your astrologer you don't need*
`Certified by no one · Trusted by fewer`

A deadpan, dry-wit astrology agent built with Streamlit + Claude.

---

## 🚀 Deploy in 5 steps

### Step 1 — Get your Anthropic API key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Go to **API Keys** → **Create Key**
4. Copy it somewhere safe

---

### Step 2 — Put these files on GitHub
1. Go to [github.com](https://github.com) → **New repository**
2. Name it `agent-vinod`
3. Make it **Public**
4. Upload these two files:
   - `app.py`
   - `requirements.txt`

---

### Step 3 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New app**
4. Choose your `agent-vinod` repo
5. Main file path: `app.py`
6. Click **Deploy**

---

### Step 4 — Add your API key as a Secret
1. In Streamlit Cloud, go to your app → **Settings** → **Secrets**
2. Add this:
```
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```
3. Save → the app will restart automatically

---

### Step 5 — Share your link 🎉
Your app will be live at:
`https://your-username-agent-vinod-app-xxxx.streamlit.app`

---

## 📁 File structure
```
agent-vinod/
├── app.py            ← main app
└── requirements.txt  ← dependencies
```

---

## 🛠 Local development (optional)
```bash
pip install streamlit anthropic
streamlit run app.py
```
Add your key to `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

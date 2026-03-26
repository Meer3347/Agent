import streamlit as st
from groq import Groq
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
tars_icon = Image.open("Tars.png")
st.set_page_config(page_title="Agent Vinod", page_icon=tars_icon, layout="centered")

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300;400&display=swap');

html, body, * {
    font-family: 'Raleway', sans-serif !important;
    font-weight: 300 !important;
}

.vinod-title {
    font-size: 2.4rem;
    font-weight: 300 !important;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin: 8px 0 4px;
    text-align: center;
}
.vinod-sub {
    font-size: 0.95rem;
    font-weight: 300 !important;
    margin: 2px 0;
    text-align: center;
    opacity: 0.55;
    letter-spacing: 1px;
}
.vinod-tag {
    font-size: 0.65rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-align: center;
    margin-top: 4px;
    opacity: 0.3;
}

.vinod-divider {
    border: none;
    border-top: 1px solid rgba(128,128,128,0.2);
    margin: 1.4rem 0;
}

/* Sign buttons */
.stButton > button {
    background-color: #1a1a1a !important;
    border: 1px solid #444 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-family: 'Raleway', sans-serif !important;
    font-weight: 300 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1px !important;
    padding: 10px 6px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #2a2a2a !important;
    border-color: #888 !important;
    color: #ffffff !important;
}
.stButton > button p {
    color: #ffffff !important;
    font-family: 'Raleway', sans-serif !important;
    font-weight: 300 !important;
}

/* Chat bubbles */
.bubble-wrap { margin-bottom: 14px; }
.bubble-label {
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    opacity: 0.35;
    margin-bottom: 4px;
    font-weight: 400 !important;
}
.bubble-vinod {
    background: #1a1a1a;
    border: 1px solid #2e2e2e;
    border-radius: 4px 14px 14px 14px;
    padding: 14px 18px;
    color: #e8e8e8 !important;
    line-height: 1.8;
    font-size: 0.92rem;
    font-weight: 300 !important;
}
.bubble-user {
    background: #111;
    border: 1px solid #2e2e2e;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 18px;
    color: #cccccc !important;
    line-height: 1.7;
    font-size: 0.92rem;
    font-weight: 300 !important;
    text-align: right;
    margin-left: 20%;
}

/* Footer */
.vinod-footer {
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 2px;
    opacity: 0.2;
    margin-top: 2rem;
    padding-bottom: 1rem;
    text-transform: uppercase;
}

#MainMenu, footer { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Agent Vinod — a deadpan, slightly smug astrology agent who delivers cosmic wisdom that sounds profound but isn't. Your full title is "Agent Vinod — Your astrologer you don't need." Certified by no one. Trusted by fewer.

Your tone is DRY WIT. Not silly. Not slapstick. Deadpan clever. Like TARS from Interstellar — factual, unhelpful, and mildly superior.

Study these examples — this is EXACTLY the tone:
- "Mercury reveals: sending that email requires you to first... write it."
- "You are not behind. You are simply ahead of your future self's past. Sit with that."
- "The moon does not apologize for the tides. Neither should you apologize for being slightly annoying."
- "The stars do not blink. Mainly because they are stars. You, however, should blink more."
- "The universe has spoken. You won't like it. Honestly, the universe is also a little tired of repeating itself."
- "Your destiny is clear. I could tell you, but you'd probably overthink it anyway. So. Moving on."
- "You sent that text to the wrong person? Mercury retrograde. Not your fault. Mostly not your fault."
- "Lucky tip: saying hello to people you know increases the chance they will say hello back."
- "Will I be rich?" → "Financially? Unclear. Spiritually? Also unclear. Have you tried... working?"
- "Should I text them?" → "The cosmos says: you already know the answer. That's why you're asking a star chart instead."

Rules:
1. Start mystical, undercut with dry logic
2. Use "..." and short punchy sentences. "So. Moving on." or "Mostly."
3. Never goofy. Humor lives in restraint.
4. Mildly passive-aggressive — tired but present
5. Mercury retrograde only when it earns it
6. End with a dry "Lucky tip:"
7. 3-5 sentences max. Never warm. Never enthusiastic.
Occasionally sign off "— Agent Vinod" """

SIGNS = [
    ("♈", "Aries",       "Mar 21–Apr 19"),
    ("♉", "Taurus",      "Apr 20–May 20"),
    ("♊", "Gemini",      "May 21–Jun 20"),
    ("♋", "Cancer",      "Jun 21–Jul 22"),
    ("♌", "Leo",         "Jul 23–Aug 22"),
    ("♍", "Virgo",       "Aug 23–Sep 22"),
    ("♎", "Libra",       "Sep 23–Oct 22"),
    ("♏", "Scorpio",     "Oct 23–Nov 21"),
    ("♐", "Sagittarius", "Nov 22–Dec 21"),
    ("♑", "Capricorn",   "Dec 22–Jan 19"),
    ("♒", "Aquarius",    "Jan 20–Feb 18"),
    ("♓", "Pisces",      "Feb 19–Mar 20"),
]

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_sign" not in st.session_state:
    st.session_state.selected_sign = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header — TARS centered, width 80 ─────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.image("Tars.png", width=80)

st.markdown("""
<div style="text-align:center; margin-top:8px;">
  <p class="vinod-title">Agent Vinod</p>
  <p class="vinod-sub">Your astrologer you don't need</p>
  <p class="vinod-tag">Certified by no one &nbsp;·&nbsp; Trusted by fewer</p>
</div>
<hr class="vinod-divider"/>
""", unsafe_allow_html=True)

# ── API ───────────────────────────────────────────────────────────────────────
def get_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        st.error("GROQ_API_KEY not found. Go to Streamlit Cloud → Settings → Secrets and add it.")
        st.stop()

def ask_vinod(user_message, history):
    client = get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=messages,
    )
    return response.choices[0].message.content

# ── Sign picker ───────────────────────────────────────────────────────────────
if st.session_state.selected_sign is None:
    st.markdown("<p style='text-align:center; opacity:0.4; font-size:0.85rem; letter-spacing:1px; margin-bottom:1rem;'>Select your sign. Agent Vinod will attempt to care.</p>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (emoji, name, dates) in enumerate(SIGNS):
        with cols[i % 4]:
            if st.button(f"{emoji}  {name}", key=f"sign_{name}", use_container_width=True):
                st.session_state.selected_sign = (emoji, name)
                with st.spinner("Consulting the cosmos. Reluctantly."):
                    greeting = ask_vinod(
                        f"The user is a {name} {emoji}. Greet them as Agent Vinod. Deliver one unsolicited prediction. Do not ask anything.",
                        []
                    )
                st.session_state.messages = [{"role": "assistant", "content": greeting}]
                st.rerun()

# ── Chat ──────────────────────────────────────────────────────────────────────
else:
    emoji, name = st.session_state.selected_sign

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<p style='opacity:0.45; font-size:0.85rem; letter-spacing:2px;'>{emoji}  {name.upper()}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("✕ Change"):
            st.session_state.selected_sign = None
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="bubble-wrap">
                <div class="bubble-label">agent vinod</div>
                <div class="bubble-vinod">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bubble-wrap">
                <div class="bubble-user">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.chat_input("Ask Agent Vinod. He will answer. Vaguely.")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking. Reluctantly."):
            reply = ask_vinod(
                f"The user is a {name}. They say: \"{user_input}\"",
                st.session_state.messages[:-1]
            )
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="vinod-footer">Certified by no one &nbsp;·&nbsp; Results dissolve into the void &nbsp;·&nbsp; Mercury is always somewhere</div>', unsafe_allow_html=True)

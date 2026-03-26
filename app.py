import streamlit as st
from groq import Groq
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
tars_icon = Image.open("Tars.png")
st.set_page_config(page_title="Agent Vinod", page_icon=tars_icon, layout="centered")

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&display=swap');

html, body, [class*="css"] {
    background-color: #000 !important;
    color: #fff !important;
    font-family: 'IM Fell English', Georgia, serif !important;
}

.vinod-header { text-align: center; padding: 2rem 0 1rem; }
.vinod-title {
    font-size: 2.6rem;
    font-style: italic;
    color: #ffffff;
    letter-spacing: 3px;
    margin: 0;
}
.vinod-sub  { color: #aaa; font-style: italic; font-size: 1rem; margin: 4px 0; }
.vinod-tag  { color: #444; font-size: 0.72rem; letter-spacing: 3px; text-transform: uppercase; }

.tars-img {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid #333;
    margin-bottom: 10px;
}

.bubble-vinod {
    background: #111;
    border: 0.5px solid #333;
    border-radius: 4px 12px 12px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    font-style: italic;
    color: #e0e0e0;
    line-height: 1.7;
    font-size: 0.95rem;
}
.bubble-user {
    background: #222;
    border: 0.5px solid #444;
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin: 8px 0 8px 20%;
    color: #fff;
    line-height: 1.7;
    font-size: 0.95rem;
    text-align: right;
}
.bubble-label {
    font-size: 0.7rem;
    color: #555;
    margin-bottom: 2px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stTextInput input {
    background: #111 !important;
    border: 0.5px solid #333 !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'IM Fell English', Georgia, serif !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus { border-color: #666 !important; box-shadow: none !important; }

.stButton > button {
    background: transparent !important;
    border: 0.5px solid #333 !important;
    color: #fff !important;
    border-radius: 10px !important;
    font-family: 'IM Fell English', Georgia, serif !important;
    font-style: italic !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { background: #222 !important; border-color: #666 !important; }

.vinod-footer {
    text-align: center;
    font-size: 0.7rem;
    color: #2a2a2a;
    font-style: italic;
    margin-top: 2rem;
    padding-bottom: 1rem;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
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

# ── Header with TARS image ────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    st.image("Tars.png", width=80)
    st.markdown("""
    <div class="vinod-header" style="padding-top:0;">
      <p class="vinod-title">Agent Vinod</p>
      <p class="vinod-sub">Your astrologer you don't need</p>
      <p class="vinod-tag">Certified by no one &nbsp;·&nbsp; Trusted by fewer</p>
    </div>
    """, unsafe_allow_html=True)

# ── API ───────────────────────────────────────────────────────────────────────
def get_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        st.error("GROQ_API_KEY not found. Add it in Streamlit Cloud → Settings → Secrets.")
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
    st.markdown("<p style='text-align:center; color:#555; font-style:italic; margin-bottom:1rem;'>Select your sign. Agent Vinod will attempt to care.</p>", unsafe_allow_html=True)
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
        st.markdown(f"<p style='color:#aaa; font-style:italic; font-size:0.9rem;'>{emoji} {name}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("✕ Change sign"):
            st.session_state.selected_sign = None
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(f'<div class="bubble-label">agent vinod</div><div class="bubble-vinod">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)

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

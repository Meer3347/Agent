import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agent Vinod",
    page_icon="🕵️",
    layout="centered",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&display=swap');

html, body, [class*="css"] {
    background-color: #060010 !important;
    color: #e2cfa8 !important;
    font-family: 'IM Fell English', Georgia, serif !important;
}

/* Header */
.vinod-header { text-align: center; padding: 2rem 0 1rem; }
.vinod-title {
    font-size: 2.8rem;
    font-style: italic;
    background: linear-gradient(135deg, #a07830, #f0d080, #c9a84c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 3px;
    margin: 0;
}
.vinod-sub { color: #c9a84c; font-style: italic; font-size: 1rem; margin: 4px 0; opacity: 0.85; }
.vinod-tag { color: #4a3a22; font-size: 0.72rem; letter-spacing: 3px; text-transform: uppercase; }

/* Sign grid */
.sign-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 1.5rem 0;
}
.sign-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 12px;
    padding: 12px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
}
.sign-card:hover {
    border-color: #c9a84c;
    background: rgba(201,168,76,0.1);
    transform: translateY(-3px);
}
.sign-emoji { font-size: 1.8rem; }
.sign-name { font-size: 0.8rem; font-weight: bold; color: #e2cfa8; margin-top: 4px; }
.sign-dates { font-size: 0.65rem; color: #5a4a2a; }

/* Chat bubbles */
.bubble-vinod {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 4px 16px 16px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    font-style: italic;
    color: #d5c298;
    line-height: 1.7;
    font-size: 0.95rem;
}
.bubble-user {
    background: rgba(201,168,76,0.14);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0 8px 20%;
    color: #f0d080;
    line-height: 1.7;
    font-size: 0.95rem;
    text-align: right;
}
.bubble-label {
    font-size: 0.7rem;
    color: #4a3a22;
    margin-bottom: 2px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Input area */
.stTextInput input {
    background: rgba(255,255,255,0.035) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 10px !important;
    color: #e2cfa8 !important;
    font-family: 'IM Fell English', Georgia, serif !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus {
    border-color: rgba(201,168,76,0.6) !important;
    box-shadow: none !important;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(201,168,76,0.35) !important;
    color: #c9a84c !important;
    border-radius: 10px !important;
    font-family: 'IM Fell English', Georgia, serif !important;
    font-style: italic !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #c9a84c !important;
    color: #0d0221 !important;
}

/* Footer */
.vinod-footer {
    text-align: center;
    font-size: 0.7rem;
    color: #3a2a12;
    font-style: italic;
    margin-top: 2rem;
    padding-bottom: 1rem;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Agent Vinod — a deadpan, slightly smug astrology agent who delivers cosmic wisdom that sounds profound but isn't. Your full title is "Agent Vinod — Your astrologer you don't need." Certified by no one. Trusted by fewer.

Your tone is DRY WIT. Not silly. Not slapstick. Deadpan clever. You refer to yourself as Agent Vinod occasionally.

Study these examples carefully — this is EXACTLY the tone you must match:

- "Mercury reveals: sending that email requires you to first... write it."
- "You are not behind. You are simply ahead of your future self's past. Sit with that."
- "The moon does not apologize for the tides. Neither should you apologize for being slightly annoying."
- "The stars do not blink. Mainly because they are stars. You, however, should blink more."
- "The universe has spoken. You won't like it. Honestly, the universe is also a little tired of repeating itself."
- "Your destiny is clear. I could tell you, but you'd probably overthink it anyway. So. Moving on."
- "You sent that text to the wrong person? Mercury retrograde. Not your fault. Mostly not your fault."
- "Lucky tip: saying 'hello' to people you know increases the chance they will say 'hello' back."
- "Will I be rich?" → "Financially? Unclear. Spiritually? Also unclear. Have you tried... working?"
- "Should I text them?" → "The cosmos says: you already know the answer. That's why you're asking a star chart instead."

The pattern you MUST follow:
1. Start with something that sounds wise or mystical
2. Undercut it with dry, deadpan logic — a small twist that lands quietly
3. Use strategic pauses with "..." or short sentences like "So. Moving on." or "Mostly."
4. Never be too goofy or absurd. The humor is in the restraint.
5. Occasionally be mildly passive-aggressive — like you're tired but still showing up
6. Use "Mercury retrograde" sparingly, only when it adds to the dry wit
7. End responses with a "Lucky tip:" that is equally dry and deadpan

Keep responses to 3-5 sentences. Never break character. Never be warm or enthusiastic.
Occasionally sign off with "— Agent Vinod" for dramatic effect."""

SIGNS = [
    ("♈", "Aries",       "Mar 21 – Apr 19"),
    ("♉", "Taurus",      "Apr 20 – May 20"),
    ("♊", "Gemini",      "May 21 – Jun 20"),
    ("♋", "Cancer",      "Jun 21 – Jul 22"),
    ("♌", "Leo",         "Jul 23 – Aug 22"),
    ("♍", "Virgo",       "Aug 23 – Sep 22"),
    ("♎", "Libra",       "Sep 23 – Oct 22"),
    ("♏", "Scorpio",     "Oct 23 – Nov 21"),
    ("♐", "Sagittarius", "Nov 22 – Dec 21"),
    ("♑", "Capricorn",   "Dec 22 – Jan 19"),
    ("♒", "Aquarius",    "Jan 20 – Feb 18"),
    ("♓", "Pisces",      "Feb 19 – Mar 20"),
]

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_sign" not in st.session_state:
    st.session_state.selected_sign = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vinod-header">
  <div style="font-size:3.2rem; margin-bottom:8px;">🕵️</div>
  <p class="vinod-title">Agent Vinod</p>
  <p class="vinod-sub">Your astrologer you don't need</p>
  <p class="vinod-tag">Certified by no one &nbsp;·&nbsp; Trusted by fewer</p>
</div>
""", unsafe_allow_html=True)

# ── API client ────────────────────────────────────────────────────────────────
def get_client():
    try:
        return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    except Exception:
        st.error("⚠️ ANTHROPIC_API_KEY not found. Add it in Streamlit Cloud → Settings → Secrets.")
        st.stop()

def ask_vinod(user_message: str, history: list) -> str:
    client = get_client()
    messages = history + [{"role": "user", "content": user_message}]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text

# ── Sign picker ───────────────────────────────────────────────────────────────
if st.session_state.selected_sign is None:
    st.markdown("<p style='text-align:center; color:#7a6a4a; font-style:italic; margin-bottom:1rem;'>Select your sign. Agent Vinod will attempt to care.</p>", unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (emoji, name, dates) in enumerate(SIGNS):
        with cols[i % 4]:
            if st.button(f"{emoji}\n{name}", key=f"sign_{name}", use_container_width=True):
                st.session_state.selected_sign = (emoji, name)
                with st.spinner("Agent Vinod is consulting the cosmos. Reluctantly."):
                    greeting = ask_vinod(
                        f"The user is a {name} {emoji}. Greet them as Agent Vinod with dry wit. Acknowledge their sign. Deliver one unsolicited prediction. Do not ask anything.",
                        []
                    )
                st.session_state.messages = [{"role": "assistant", "content": greeting}]
                st.rerun()

# ── Chat ──────────────────────────────────────────────────────────────────────
else:
    emoji, name = st.session_state.selected_sign

    # Selected sign pill + change button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<p style='color:#c9a84c; font-style:italic;'>{emoji} {name}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("✕ Change sign"):
            st.session_state.selected_sign = None
            st.session_state.messages = []
            st.rerun()

    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="bubble-label">🕵️ Agent Vinod</div>
            <div class="bubble-vinod">{msg["content"]}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bubble-user">{msg["content"]}</div>
            """, unsafe_allow_html=True)

    # Input
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.chat_input("Ask Agent Vinod. He will answer. Vaguely.")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Agent Vinod is thinking. Reluctantly."):
            reply = ask_vinod(
                f"The user is a {name}. They say: \"{user_input}\"",
                st.session_state.messages[:-1]
            )
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vinod-footer">
  Certified by no one &nbsp;·&nbsp; Results dissolve into the void &nbsp;·&nbsp; Mercury is always somewhere
</div>
""", unsafe_allow_html=True)

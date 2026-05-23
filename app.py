import streamlit as st
import os
import random
import re
import math
from datetime import datetime
from dotenv import load_dotenv

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), "Bot", ".env"))

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChatBot AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #161b33 50%, #1a1a2e 100%);
}

/* Hide default header/footer */
header[data-testid="stHeader"] { background: transparent; }
footer { display: none; }
#MainMenu { display: none; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #16213e 0%, #0f0c29 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e0e0ff;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #a0a0c0;
    font-size: 0.88rem;
}

/* Hero header */
.hero-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.hero-header h1 {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero-header p {
    color: #8888aa;
    font-size: 0.95rem;
    margin-top: 0;
}

/* Mode badge */
.mode-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}
.mode-offline {
    background: rgba(102, 126, 234, 0.15);
    color: #667eea;
    border: 1px solid rgba(102, 126, 234, 0.3);
}
.mode-ai {
    background: rgba(240, 147, 251, 0.15);
    color: #f093fb;
    border: 1px solid rgba(240, 147, 251, 0.3);
}

/* Chat container */
.chat-container {
    max-height: 55vh;
    overflow-y: auto;
    padding: 1rem 0;
    scrollbar-width: thin;
    scrollbar-color: #333355 transparent;
}

/* Chat bubbles */
.chat-bubble {
    padding: 0.85rem 1.1rem;
    border-radius: 18px;
    margin-bottom: 0.7rem;
    max-width: 85%;
    line-height: 1.55;
    font-size: 0.92rem;
    animation: fadeSlideIn 0.35s ease-out;
    word-wrap: break-word;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.user-bubble {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    margin-left: auto;
    border-bottom-right-radius: 4px;
}
.bot-bubble {
    background: rgba(255, 255, 255, 0.06);
    color: #d0d0e8;
    border: 1px solid rgba(255,255,255,0.08);
    margin-right: auto;
    border-bottom-left-radius: 4px;
    backdrop-filter: blur(10px);
}

/* Sender labels */
.sender-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
    text-transform: uppercase;
}
.sender-user { color: #667eea; text-align: right; }
.sender-bot  { color: #f093fb; text-align: left; }

/* Quick action buttons */
.quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    padding: 0.5rem 0 1rem;
}

/* Stats card */
.stats-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.stats-card h4 {
    color: #a0a0c0;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}
.stats-card .stat-value {
    color: #e0e0ff;
    font-size: 1.4rem;
    font-weight: 700;
}

/* Input styling */
.stChatInput > div {
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RULE-BASED BOT ENGINE  (imported from chatbot.py logic)
# ══════════════════════════════════════════════════════════════════════════════

mood_keywords = {
    "happy": ["happy","glad","great","awesome","fantastic","wonderful","excited","joy","amazing","good"],
    "sad": ["sad","unhappy","depressed","down","miserable","crying","lonely","heartbroken","upset"],
    "angry": ["angry","mad","furious","annoyed","irritated","frustrated","hate"],
    "anxious": ["anxious","nervous","worried","stressed","overwhelmed","panic","scared"],
    "bored": ["bored","boring","nothing to do","dull","uninteresting"],
}
mood_responses = {
    "happy": ["That's wonderful to hear! 😄","Your positivity is contagious! 🌟","Keep that great energy going! ✨"],
    "sad": ["I'm sorry you're feeling that way. 💙 Want to talk about it?","Sending you virtual hugs! 🤗","It's okay to feel sad sometimes. I'm here for you."],
    "angry": ["Take a deep breath. 🌬️ Want to vent about it?","I hear you. Sometimes things can be really frustrating.","Let it out — I'm here to listen. 💪"],
    "anxious": ["Try taking slow, deep breaths. 🧘 You've got this!","One thing at a time — you don't have to figure it all out now.","Remember: most of what we worry about never happens. 🌈"],
    "bored": ["Let's fix that! Want a joke, a fun fact, or a riddle? 🎲","Boredom is the birthplace of creativity! Try something new!","How about a quick trivia challenge? Just say 'riddle'!"],
}

responses = {
    ("hello","hi","hey","hola","sup","yo","howdy","greetings","good morning","good afternoon","good evening"):
        ["Hey there! How can I help you?","Hello! Nice to see you!","Hi! What's on your mind?","Hey! Ready to chat?"],
    ("how are you","how's it going","what's up","how u doing"):
        ["I'm doing great, thanks for asking! How about you?","All systems running smoothly! What about you?","Living my best digital life! How are you?"],
    ("your name","who are you","what are you","introduce yourself"):
        ["I'm ChatBot — your friendly assistant!","Call me ChatBot! I'm here to chat with you."],
    ("time","what time","current time","clock"):
        [lambda: f"The current time is {datetime.now().strftime('%I:%M %p')}."],
    ("date","today","what day","calendar"):
        [lambda: f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."],
    ("thank","thanks","thx","appreciate","ty"):
        ["You're welcome!","Happy to help!","No problem at all!","Anytime!"],
    ("joke","funny","laugh","humor","make me laugh"):
        ["Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
         "Why was the JavaScript developer sad? He didn't Node how to Express himself!",
         "There are only 10 types of people — those who understand binary and those who don't.",
         "A SQL query walks into a bar, sees two tables, and asks… 'Can I JOIN you?' 🍺",
         "Why do Java developers wear glasses? Because they can't C#!",
         "!false — it's funny because it's true. 😄"],
    ("help","what can you do","features","commands","menu"):
        ["I can do a lot! Try: jokes, riddle, flip coin, roll dice, random number, time, date, math (e.g. 'calculate 5+3'), motivation, fun facts, or just chat!"],
    ("motivat","inspire","encourage","feeling down"):
        ["Remember: every expert was once a beginner. Keep going! 🚀","You're stronger than you think. One step at a time!","Tough times don't last, but tough people do. You've got this! 💪"],
    ("fact","fun fact","did you know","trivia","interesting"):
        ["Fun fact: Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs! 🍯",
         "Did you know? Octopuses have three hearts and blue blood! 🐙",
         "A group of flamingos is called a 'flamboyance'! 🦩",
         "The first computer bug was an actual bug — a moth found in a Harvard computer in 1947! 🦗"],
    ("python","coding","programming","code","developer","software"):
        ["Python is amazing! It's readable, versatile, and has a huge community. 🐍","Coding tip: Write code that your future self will thank you for!","The best way to learn programming is by building projects — like this chatbot!"],
    ("ai","artificial intelligence","machine learning","ml","deep learning"):
        ["AI is transforming everything! From healthcare to self-driving cars. 🤖","Machine Learning is all about teaching computers to learn from data.","Neural networks are inspired by the human brain. Fascinating stuff!"],
    ("space","universe","star","planet","galaxy","moon","nasa","mars"):
        ["Space is mind-blowing! The observable universe is 93 billion light-years across! 🌌","Fun fact: There are more stars in the universe than grains of sand on Earth! ⭐","Mars has the tallest volcano in the solar system — Olympus Mons! 🌋"],
    ("music","song","sing","playlist","band"):
        ["Music is the universal language! What are you listening to lately? 🎵","Fun fact: Listening to music can reduce stress by up to 65%! 🎧"],
    ("movie","film","watch","series","show","anime","netflix"):
        ["I love movie talk! Seen anything good lately? 🎬","Popcorn ready? What's your all-time favorite movie? 🍿"],
    ("food","eat","hungry","cook","recipe","pizza","burger"):
        ["Mmm, food talk! What's your favorite dish? 🍕","Fun fact: The world's most expensive pizza costs over $12,000! 🤯"],
    ("book","read","study","learn","education"):
        ["Reading is a superpower! What's the last book you read? 📚","Learning never exhausts the mind. — Leonardo da Vinci 🎨"],
    ("sleep","tired","insomnia","rest","nap","sleepy"):
        ["Sleep is crucial! Adults need 7-9 hours. Are you getting enough? 😴","Tip: Try avoiding screens 30 minutes before bed for better sleep. 📵"],
    ("health","exercise","gym","workout","fitness","yoga"):
        ["Staying active is key! Even a 30-minute walk makes a big difference. 🏃","Drink plenty of water — your body will thank you! 💧"],
    ("bye","goodbye","quit","exit","see you","later"):
        ["Goodbye! Have an awesome day! 👋","See you later! Take care! ✨","Bye! It was nice chatting with you! 😊"],
}

fallbacks = [
    "Hmm, I'm not sure I understand. Could you rephrase that?",
    "That's interesting! Tell me more. 🤔",
    "I don't have a good answer for that yet, but I'm learning!",
    "I'm a simple bot — try asking about jokes, time, facts, or math!",
]

riddles = [
    ("I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?", "A keyboard!"),
    ("What has hands but can't clap?", "A clock!"),
    ("The more you take, the more you leave behind. What am I?", "Footsteps!"),
    ("What gets wetter the more it dries?", "A towel!"),
    ("What has many teeth but can't bite?", "A comb!"),
]

def evaluate_math(expression):
    try:
        cleaned = re.sub(r"[^0-9+\-*/().%\s]", "", expression)
        if not cleaned.strip():
            return None
        result = eval(cleaned, {"__builtins__": {}}, {"math": math})
        if isinstance(result, float) and result == int(result):
            result = int(result)
        return f"The answer is: **{result}** 🧮"
    except Exception:
        return None

def get_rule_response(user_input):
    text = user_input.lower().strip()
    if text in ("riddle","riddles","brain teaser","puzzle"):
        q, a = random.choice(riddles)
        return f"🧩 **Riddle:** {q}\n\n*Think about it… the answer is: {a}*"
    if text in ("flip","flip coin","coin flip","coin","heads or tails"):
        return f"🪙 *flips coin* … It's **{random.choice(['Heads','Tails'])}**!"
    if text in ("roll","roll dice","dice","dice roll"):
        return f"🎲 *rolls dice* … You got a **{random.randint(1,6)}**!"
    if "random number" in text or text == "random":
        return f"🔢 Your random number: **{random.randint(1,100)}**"

    math_match = re.search(r"(?:calculate|compute|solve|what is|what's)\s+(.+)", text)
    if math_match:
        result = evaluate_math(math_match.group(1))
        if result:
            return result
    if re.match(r"^[\d\s+\-*/().%]+$", text) and len(text.strip()) > 1:
        result = evaluate_math(text)
        if result:
            return result

    for mood, keywords in mood_keywords.items():
        for kw in keywords:
            if kw in text:
                if len(text.split()) <= 5:
                    return random.choice(mood_responses[mood])
                break

    for keywords, replies in responses.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                choice = random.choice(replies)
                return choice() if callable(choice) else choice

    return random.choice(fallbacks)


# ══════════════════════════════════════════════════════════════════════════════
# AI BOT ENGINE  (Groq)
# ══════════════════════════════════════════════════════════════════════════════

def get_ai_response(user_input, history):
    try:
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "⚠️ No GROQ_API_KEY found. Please add it to `Bot/.env`."
        client = Groq(api_key=api_key)
        messages = [{"role":"system","content":"You are a helpful, friendly, and concise chatbot. Use emojis occasionally."}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role":"user","content": user_input})
        resp = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
        return resp.choices[0].message.content
    except ImportError:
        return "⚠️ `groq` package not installed. Run `pip install groq`."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "🧠 Rule-Based (Offline)"
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🤖 ChatBot")
    st.markdown("---")

    mode = st.radio(
        "**Bot Mode**",
        ["🧠 Rule-Based (Offline)", "✨ AI-Powered (Groq)"],
        index=0 if st.session_state.mode == "🧠 Rule-Based (Offline)" else 1,
        help="Switch between offline rule-based bot and AI-powered bot"
    )
    st.session_state.mode = mode

    st.markdown("---")

    # Stats
    elapsed = datetime.now() - st.session_state.start_time
    mins = int(elapsed.total_seconds() // 60)
    secs = int(elapsed.total_seconds() % 60)

    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    col1.metric("Messages", st.session_state.msg_count)
    col2.metric("Duration", f"{mins}m {secs}s")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.session_state.start_time = datetime.now()
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚡ Quick Commands")
    st.markdown("""
- `joke` — Get a programming joke
- `riddle` — Brain teaser
- `flip coin` — Heads or tails
- `roll dice` — Roll a D6
- `random number` — 1–100
- `time` / `date` — Current info
- `calculate 5+3` — Math
- `help` — All features
    """)

    if mode == "✨ AI-Powered (Groq)":
        st.markdown("---")
        st.markdown("### 🔑 API Status")
        if os.getenv("GROQ_API_KEY"):
            st.success("Groq API key loaded ✅")
        else:
            st.error("No API key found ❌")
            st.caption("Add `GROQ_API_KEY` to `Bot/.env`")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# Hero
st.markdown("""
<div class="hero-header">
    <h1>🤖 ChatBot AI</h1>
    <p>Your intelligent conversational companion</p>
</div>
""", unsafe_allow_html=True)

# Mode badge
if st.session_state.mode == "🧠 Rule-Based (Offline)":
    st.markdown('<div style="text-align:center"><span class="mode-badge mode-offline">⚡ OFFLINE MODE</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align:center"><span class="mode-badge mode-ai">🌐 AI MODE — Llama 3.3</span></div>', unsafe_allow_html=True)

st.markdown("")

# Quick action buttons
if not st.session_state.messages:
    st.markdown("#### 💬 Start a conversation or try a quick action:")
    cols = st.columns(4)
    quick_actions = [
        ("😂 Joke", "tell me a joke"),
        ("🧩 Riddle", "riddle"),
        ("🪙 Flip Coin", "flip coin"),
        ("🎲 Roll Dice", "roll dice"),
    ]
    for i, (label, cmd) in enumerate(quick_actions):
        if cols[i].button(label, use_container_width=True, key=f"qa_{i}"):
            st.session_state.messages.append({"role": "user", "content": cmd})
            if st.session_state.mode == "🧠 Rule-Based (Offline)":
                reply = get_rule_response(cmd)
            else:
                reply = get_ai_response(cmd, st.session_state.messages[:-1])
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.msg_count += 2
            st.rerun()

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message here…"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.msg_count += 1

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking…"):
            if st.session_state.mode == "🧠 Rule-Based (Offline)":
                reply = get_rule_response(prompt)
            else:
                ai_history = [m for m in st.session_state.messages if m["role"] in ("user","assistant")][:-1]
                reply = get_ai_response(prompt, ai_history)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.msg_count += 1
    st.rerun()

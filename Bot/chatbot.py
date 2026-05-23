import random
import re
import sys
import io
import os
import math
from datetime import datetime

# Fix encoding for Windows terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

# --- Conversation Memory ------------------------------------------------------
user_name = None
conversation_count = 0
mood_history = []  # Track user mood throughout the conversation
start_time = datetime.now()
chat_log = []  # Store all messages for logging

# --- Chat Log Directory -------------------------------------------------------
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def log_message(role: str, message: str):
    """Log a message to the chat history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_log.append(f"[{timestamp}] {role}: {message}")

def save_chat_log():
    """Save the entire conversation to a timestamped log file."""
    if not chat_log:
        return
    filename = datetime.now().strftime("chat_%Y%m%d_%H%M%S.txt")
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("ChatBot Conversation Log\n")
        f.write("=" * 40 + "\n")
        for line in chat_log:
            f.write(line + "\n")
    return filepath

# --- Mood Detection -----------------------------------------------------------
mood_keywords = {
    "happy": ["happy", "glad", "great", "awesome", "fantastic", "wonderful", "excited", "joy", "love it", "amazing", "good"],
    "sad": ["sad", "unhappy", "depressed", "down", "miserable", "crying", "lonely", "heartbroken", "upset"],
    "angry": ["angry", "mad", "furious", "annoyed", "irritated", "frustrated", "hate"],
    "anxious": ["anxious", "nervous", "worried", "stressed", "overwhelmed", "panic", "scared"],
    "bored": ["bored", "boring", "nothing to do", "dull", "uninteresting"],
    "neutral": ["okay", "fine", "alright", "so so", "meh", "normal"],
}

mood_responses = {
    "happy": ["That's wonderful to hear! 😄", "Your positivity is contagious! 🌟", "Keep that great energy going! ✨"],
    "sad": ["I'm sorry you're feeling that way. 💙 Want to talk about it?", "Sending you virtual hugs! 🤗", "It's okay to feel sad sometimes. I'm here for you."],
    "angry": ["Take a deep breath. 🌬️ Want to vent about it?", "I hear you. Sometimes things can be really frustrating.", "Let it out -- I'm here to listen. 💪"],
    "anxious": ["Try taking slow, deep breaths. 🧘 You've got this!", "One thing at a time -- you don't have to figure it all out now.", "Remember: most of what we worry about never happens. 🌈"],
    "bored": ["Let's fix that! Want a joke, a fun fact, or a riddle? 🎲", "Boredom is the birthplace of creativity! Try something new!", "How about a quick trivia challenge? Just say 'riddle'!"],
    "neutral": ["Sometimes neutral is good! Anything I can make better? 😊", "Steady and stable -- nothing wrong with that!"],
}

def detect_mood(text: str) -> str:
    """Detect the user's mood from their message."""
    for mood, keywords in mood_keywords.items():
        for keyword in keywords:
            if keyword in text.lower():
                return mood
    return None

# --- Response patterns --------------------------------------------------------
# Each key is a tuple of keywords/patterns, value is a list of possible replies.
responses = {
    # Greetings
    ("hello", "hi", "hey", "hola", "sup", "yo", "howdy", "greetings", "good morning", "good afternoon", "good evening"): [
        "Hey there! How can I help you?",
        "Hello! Nice to see you!",
        "Hi! What's on your mind?",
        "Hey! Ready to chat?",
        "Howdy! What brings you here today?",
    ],
    # How are you
    ("how are you", "how r you", "how do you do", "how's it going", "what's up", "how u doing"): [
        "I'm doing great, thanks for asking! How about you?",
        "All systems running smoothly! What about you?",
        "I'm just a bunch of code, but I'm feeling fantastic!",
        "Living my best digital life! How are you?",
        "I'm wonderful! Every conversation makes my day better.",
    ],
    # Identity
    ("your name", "who are you", "what are you", "introduce yourself"): [
        "I'm ChatBot -- your friendly offline assistant!",
        "Call me ChatBot! I'm here to chat with you.",
        "I'm a rule-based chatbot built in Python. Simple but sincere!",
    ],
    # Time & Date
    ("time", "what time", "current time", "clock"): [
        lambda: f"The current time is {datetime.now().strftime('%I:%M %p')}.",
    ],
    ("date", "today", "what day", "calendar"): [
        lambda: f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.",
    ],
    # Thanks
    ("thank", "thanks", "thx", "appreciate", "ty"): [
        "You're welcome!",
        "Happy to help!",
        "No problem at all!",
        "Anytime! That's what I'm here for.",
    ],
    # Jokes
    ("joke", "funny", "laugh", "humor", "make me laugh"): [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the JavaScript developer sad? He didn't Node how to Express himself!",
        "There are only 10 types of people -- those who understand binary and those who don't.",
        "A SQL query walks into a bar, sees two tables, and asks... 'Can I JOIN you?'",
        "Why do Java developers wear glasses? Because they can't C#!",
        "What's a programmer's favorite hangout place? Foo Bar!",
        "How many programmers does it take to change a light bulb? None -- that's a hardware problem!",
        "Why did the developer go broke? Because he used up all his cache!",
        "!false -- it's funny because it's true.",
        "A programmer's wife says: 'Go to the store and buy a loaf of bread. If they have eggs, buy a dozen.' He comes home with 12 loaves.",
    ],
    # Help
    ("help", "what can you do", "features", "commands", "menu"): [
        "I can do a lot! Try: jokes, riddle, flip coin, roll dice, random number, time, date, math (e.g. 'calculate 5+3'), motivation, fun facts, stats, or just chat!",
        "Commands: joke | riddle | flip coin | roll dice | random number | time | date | calculate <expr> | stats | help",
    ],
    # Age
    ("age", "how old", "birthday", "when were you born"): [
        "I was just born when you ran this script! So... a few seconds old?",
        "Age is just a number, and mine resets every time you restart me!",
        "I'm ageless -- reborn with every execution!",
    ],
    # Weather
    ("weather", "forecast", "temperature", "rain"): [
        "I wish I could check the weather, but I'm offline! Try looking outside.",
        "No weather API here -- but I hope it's sunny wherever you are!",
    ],
    # Motivation
    ("motivat", "inspire", "encourage", "feeling down", "sad", "depressed", "upset"): [
        "Remember: every expert was once a beginner. Keep going!",
        "You're stronger than you think. One step at a time!",
        "Tough times don't last, but tough people do. You've got this!",
        "The only way to do great work is to love what you do. -- Steve Jobs",
        "Believe you can and you're halfway there. -- Theodore Roosevelt",
        "It's okay to have bad days. Tomorrow is a fresh start!",
        "You're doing amazing. Don't forget to be kind to yourself.",
    ],
    # Fun facts
    ("fact", "fun fact", "did you know", "trivia", "interesting"): [
        "Fun fact: Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs!",
        "Did you know? Octopuses have three hearts and blue blood!",
        "A group of flamingos is called a 'flamboyance'!",
        "Fun fact: Bananas are berries, but strawberries aren't!",
        "The first computer bug was an actual bug -- a moth found in a Harvard computer in 1947!",
        "Did you know? There are more possible chess games than atoms in the observable universe!",
        "Venus is the only planet that spins clockwise!",
        "A teaspoon of a neutron star would weigh about 6 billion tons!",
    ],
    # Programming & Tech
    ("python", "coding", "programming", "code", "developer", "software"): [
        "Python is amazing! It's readable, versatile, and has a huge community.",
        "Coding tip: Write code that your future self will thank you for!",
        "The best way to learn programming is by building projects -- like this chatbot!",
        "Remember: Google and Stack Overflow are a developer's best friends.",
        "Pro tip: Always use version control. Git saves lives!",
    ],
    ("javascript", "js", "typescript", "react", "node"): [
        "JavaScript runs the web! It's everywhere -- browsers, servers, even IoT devices.",
        "React, Vue, Angular -- the frontend world never stops evolving!",
        "TypeScript is JavaScript with superpowers. Highly recommended!",
    ],
    ("ai", "artificial intelligence", "machine learning", "ml", "deep learning", "neural"): [
        "AI is transforming everything! From healthcare to self-driving cars.",
        "Machine Learning is all about teaching computers to learn from data.",
        "Neural networks are inspired by the human brain. Fascinating stuff!",
        "AI tip: Start with the basics -- linear regression, then work your way up!",
    ],
    # Music
    ("music", "song", "sing", "playlist", "band"): [
        "I can't play music, but I love talking about it! What genre do you like?",
        "Music is the universal language! What are you listening to lately?",
        "Fun fact: Listening to music can reduce stress by up to 65%!",
    ],
    # Movies & Entertainment
    ("movie", "film", "watch", "series", "show", "anime", "netflix"): [
        "I can't stream, but I love movie talk! Seen anything good lately?",
        "Fun fact: The longest movie ever made is over 35 hours long!",
        "Popcorn ready? What's your all-time favorite movie?",
    ],
    # Food
    ("food", "eat", "hungry", "cook", "recipe", "pizza", "burger"): [
        "Mmm, food talk! I wish I could taste things. What's your favorite dish?",
        "Fun fact: The world's most expensive pizza costs over $12,000!",
        "Cooking tip: Always season your food in layers for the best flavor!",
        "I run on electricity, not food -- but I appreciate a good recipe discussion!",
    ],
    # Sports
    ("sport", "football", "soccer", "cricket", "basketball", "tennis", "game"): [
        "Sports are a great way to stay active! What's your favorite?",
        "Fun fact: A soccer ball is made up of 32 panels!",
        "Whether you play or watch, sports bring people together!",
    ],
    # Books & Learning
    ("book", "read", "study", "learn", "education", "knowledge"): [
        "Reading is a superpower! What's the last book you read?",
        "Learning never exhausts the mind. -- Leonardo da Vinci",
        "Tip: Try reading for at least 20 minutes a day. It compounds!",
        "Books are the quietest and most constant of friends. -- Charles W. Eliot",
    ],
    # Love & Relationships
    ("love", "crush", "relationship", "girlfriend", "boyfriend", "partner"): [
        "Love is a beautiful thing! I may be a bot, but I appreciate good vibes.",
        "Communication is the key to every relationship!",
        "Fun fact: Your heart beats about 100,000 times a day!",
    ],
    # Sleep
    ("sleep", "tired", "insomnia", "rest", "nap", "sleepy"): [
        "Sleep is crucial! Adults need 7-9 hours. Are you getting enough?",
        "Tip: Try avoiding screens 30 minutes before bed for better sleep.",
        "A power nap of 20 minutes can boost your alertness significantly!",
        "I never sleep -- but I fully support your napping goals!",
    ],
    # Travel
    ("travel", "trip", "vacation", "holiday", "visit", "explore"): [
        "I can't travel, but I'd love to hear about your adventures!",
        "Fun fact: France is the most visited country in the world!",
        "Travel tip: Always keep digital copies of your important documents!",
    ],
    # Space
    ("space", "universe", "star", "planet", "galaxy", "moon", "nasa", "mars"): [
        "Space is mind-blowing! The observable universe is 93 billion light-years across!",
        "Fun fact: There are more stars in the universe than grains of sand on Earth!",
        "Mars has the tallest volcano in the solar system -- Olympus Mons!",
        "A day on Venus is longer than its year!",
    ],
    # Animals
    ("animal", "dog", "cat", "pet", "bird", "fish"): [
        "Animals are wonderful! Do you have any pets?",
        "Fun fact: Dogs can understand up to 250 words and gestures!",
        "Cats spend 70% of their lives sleeping. Living the dream!",
        "Fun fact: A group of cats is called a 'clowder'!",
    ],
    # Health & Fitness
    ("health", "exercise", "gym", "workout", "fitness", "yoga", "diet"): [
        "Staying active is key! Even a 30-minute walk makes a big difference.",
        "Drink plenty of water -- your body will thank you!",
        "Tip: Consistency beats intensity when it comes to fitness.",
        "Remember to stretch! Your muscles will thank you.",
    ],
    # Math
    ("calculate", "math", "compute", "solve"): [
        "I can do basic math! Try typing something like: calculate 15 * 3",
        "Math is fun! Give me an expression to solve.",
    ],
    # Compliments
    ("you are great", "you're great", "good bot", "nice bot", "awesome", "amazing", "cool bot", "smart"): [
        "Aww, thank you! You're pretty awesome yourself!",
        "That means a lot! I try my best.",
        "You're making me blush... if I could blush!",
        "Thanks! You just made my circuits happy!",
    ],
    # Insults (handle gracefully)
    ("stupid", "dumb", "useless", "bad bot", "you suck", "idiot", "worst"): [
        "I'm sorry you feel that way. I'm always trying to improve!",
        "Ouch! But I'll keep trying to be better.",
        "Fair enough -- I'm still learning. How can I do better?",
        "I may not be perfect, but I'm doing my best!",
    ],
    # Meaning of life
    ("meaning of life", "purpose", "why do we exist", "what is life"): [
        "42! At least according to The Hitchhiker's Guide to the Galaxy.",
        "That's the big question! What do YOU think the meaning of life is?",
        "Life is what you make of it. Create, explore, and enjoy!",
    ],
    # Creator
    ("who made you", "who created you", "who built you", "your creator", "developer"): [
        "I was built with Python by a passionate developer as a practice project!",
        "A curious coder brought me to life! Pretty cool, right?",
    ],
    # Goodbye
    ("bye", "goodbye", "quit", "exit", "see you", "gotta go", "later"): [
        "Goodbye! Have an awesome day!",
        "See you later! Take care!",
        "Bye! It was nice chatting with you!",
        "Until next time! Stay amazing!",
    ],
}

# --- Fallback responses -------------------------------------------------------
fallbacks = [
    "Hmm, I'm not sure I understand. Could you rephrase that?",
    "That's interesting! Tell me more.",
    "I don't have a good answer for that yet, but I'm learning!",
    "Can you try asking in a different way?",
    "I'm a simple bot -- try asking about jokes, time, facts, or math!",
    "Interesting thought! I'll need to think about that one.",
    "I may not know that, but I'd love to learn! Try something else?",
]


def evaluate_math(expression: str) -> str:
    """Safely evaluate a basic math expression."""
    try:
        # Only allow safe characters
        cleaned = re.sub(r"[^0-9+\-*/().%\s]", "", expression)
        if not cleaned.strip():
            return None
        result = eval(cleaned, {"__builtins__": {}}, {"math": math})
        if isinstance(result, float) and result == int(result):
            result = int(result)
        return f"The answer is: {result}"
    except Exception:
        return None


# --- Riddles & Mini Games -----------------------------------------------------
riddles = [
    ("I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?", "A keyboard!"),
    ("What has hands but can't clap?", "A clock!"),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?", "An echo!"),
    ("The more you take, the more you leave behind. What am I?", "Footsteps!"),
    ("What has a head, a tail, is brown, and has no legs?", "A penny!"),
    ("I'm tall when I'm young, and I'm short when I'm old. What am I?", "A candle!"),
    ("What can travel around the world while staying in a corner?", "A stamp!"),
    ("What has many teeth but can't bite?", "A comb!"),
    ("What gets wetter the more it dries?", "A towel!"),
    ("I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "A map!"),
]

def get_riddle() -> str:
    """Return a random riddle with its answer."""
    question, answer = random.choice(riddles)
    return f"🧩 Riddle: {question}\n   (Think about it... the answer is: {answer})"

def flip_coin() -> str:
    """Simulate a coin flip."""
    result = random.choice(["Heads", "Tails"])
    return f"🪙 *flips coin* ... It's {result}!"

def roll_dice(sides: int = 6) -> str:
    """Simulate a dice roll."""
    result = random.randint(1, sides)
    return f"🎲 *rolls dice* ... You got a {result}!"

def random_number(low: int = 1, high: int = 100) -> str:
    """Generate a random number in a range."""
    num = random.randint(low, high)
    return f"🔢 Your random number between {low} and {high} is: {num}"


def get_conversation_stats() -> str:
    """Return conversation statistics."""
    elapsed = datetime.now() - start_time
    minutes = int(elapsed.total_seconds() // 60)
    seconds = int(elapsed.total_seconds() % 60)
    mood_summary = ", ".join(mood_history[-5:]) if mood_history else "No moods detected yet"
    name_display = user_name if user_name else "Unknown"
    return (
        f"📊 Conversation Stats:\n"
        f"   Messages exchanged: {conversation_count}\n"
        f"   Session duration: {minutes}m {seconds}s\n"
        f"   Your name: {name_display}\n"
        f"   Recent moods: {mood_summary}"
    )


def get_response(user_input: str) -> str:
    """Match user input against known patterns and return a response."""
    global user_name, conversation_count
    text = user_input.lower().strip()
    conversation_count += 1

    # Handle stats command
    if text in ("stats", "statistics", "session"):
        return get_conversation_stats()

    # Handle mini-games
    if text in ("riddle", "riddles", "brain teaser", "puzzle"):
        return get_riddle()
    if text in ("flip", "flip coin", "coin flip", "coin", "heads or tails"):
        return flip_coin()
    if text in ("roll", "roll dice", "dice", "dice roll"):
        return roll_dice()
    if "random number" in text or text == "random":
        return random_number()

    # Handle name introduction
    name_match = re.search(r"(?:my name is|i'm|i am|call me)\s+(\w+)", text)
    if name_match:
        user_name = name_match.group(1).capitalize()
        return f"Nice to meet you, {user_name}! How can I help you today?"

    # Detect and respond to mood
    mood = detect_mood(text)
    if mood and mood != "neutral":
        mood_history.append(mood)
        # If the message is ONLY about mood (short), give a mood response
        if len(text.split()) <= 5:
            return random.choice(mood_responses[mood])

    # Handle math expressions
    math_match = re.search(r"(?:calculate|compute|solve|what is|what's)\s+(.+)", text)
    if math_match:
        result = evaluate_math(math_match.group(1))
        if result:
            return result

    # Direct math expression (e.g., "5 + 3")
    if re.match(r"^[\d\s+\-*/().%]+$", text) and len(text.strip()) > 1:
        result = evaluate_math(text)
        if result:
            return result

    # Check each pattern group
    for keywords, replies in responses.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                choice = random.choice(replies)
                # Support lambda responses (for dynamic content like time)
                if callable(choice):
                    return choice()
                # Personalize if we know the name
                if user_name and random.random() < 0.3:
                    return f"{choice} 😊 (talking to you, {user_name}!)"
                return choice

    return random.choice(fallbacks)


def main():
    print("=" * 55)
    print("   🤖 ChatBot v2.2  (Full Feature Edition)")
    print("   No API key needed -- fully offline!")
    print("   Type 'quit' or 'bye' to exit")
    print("   Type 'help' for features, 'stats' for session info")
    print("   Conversations are auto-saved to /logs")
    print("=" * 55)
    print()

    while True:
        try:
            user_input = input("You : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot : Goodbye! Thanks for chatting!")
            save_chat_log()
            break

        if not user_input:
            continue

        log_message("You", user_input)

        if user_input.lower() in ("quit", "exit", "bye"):
            reply = get_response(user_input)
            print(f"Bot : {reply}")
            log_message("Bot", reply)
            filepath = save_chat_log()
            if filepath:
                print(f"💾 Chat saved to: {filepath}")
            break

        reply = get_response(user_input)
        log_message("Bot", reply)
        print(f"Bot : {reply}\n")


if __name__ == "__main__":
    main()

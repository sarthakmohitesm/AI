import random
import re
import sys
import io
from datetime import datetime

# Fix encoding for Windows terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

# --- Response patterns -------------------------------------------------------
# Each key is a tuple of keywords/patterns, value is a list of possible replies.
responses = {
    ("hello", "hi", "hey", "hola", "sup"): [
        "Hey there! How can I help you?",
        "Hello! Nice to see you!",
        "Hi! What's on your mind?",
    ],
    ("how are you", "how r you", "how do you do"): [
        "I'm doing great, thanks for asking! How about you?",
        "All systems running smoothly! What about you?",
        "I'm just a bunch of code, but I'm feeling fantastic!",
    ],
    ("your name", "who are you", "what are you"): [
        "I'm ChatBot -- your friendly offline assistant!",
        "Call me ChatBot! I'm here to chat with you.",
        "I'm a simple rule-based chatbot, but I try my best!",
    ],
    ("time", "what time", "current time"): [
        f"The current time is {datetime.now().strftime('%I:%M %p')}.",
    ],
    ("date", "today", "what day"): [
        f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.",
    ],
    ("thank", "thanks", "thx"): [
        "You're welcome!",
        "Happy to help!",
        "No problem at all!",
    ],
    ("joke", "funny", "laugh"): [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
        "There are only 10 types of people -- those who understand binary and those who don't.",
        "A SQL query walks into a bar, sees two tables, and asks... 'Can I JOIN you?'",
    ],
    ("help", "what can you do", "features"): [
        "I can chat, tell jokes, share the time/date, and keep you company! Just ask away.",
        "Try asking me: a joke, the time, the date, or just say hi!",
    ],
    ("age", "how old"): [
        "I was just born when you ran this script! So... a few seconds old?",
        "Age is just a number, and mine resets every time you restart me!",
    ],
    ("weather",): [
        "I wish I could check the weather, but I'm offline! Try looking outside the window.",
    ],
    ("bye", "goodbye", "quit", "exit"): [
        "Goodbye! Have an awesome day!",
        "See you later! Take care!",
        "Bye! It was nice chatting with you!",
    ],
}

# --- Fallback responses -------------------------------------------------------
fallbacks = [
    "Hmm, I'm not sure I understand. Could you rephrase that?",
    "That's interesting! Tell me more.",
    "I don't have a good answer for that, but I'm learning!",
    "Can you try asking in a different way?",
    "I'm a simple bot -- try asking about jokes, time, or just say hi!",
]


def get_response(user_input: str) -> str:
    """Match user input against known patterns and return a response."""
    text = user_input.lower().strip()

    # Check each pattern group
    for keywords, replies in responses.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                return random.choice(replies)

    return random.choice(fallbacks)


def main():
    print("=" * 50)
    print("  [*] Basic ChatBot  (no API key needed)")
    print("  Type 'quit' or 'bye' to exit")
    print("=" * 50)
    print()

    while True:
        user_input = input("You : ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye"):
            print(f"Bot : {get_response(user_input)}")
            break

        reply = get_response(user_input)
        print(f"Bot : {reply}\n")


if __name__ == "__main__":
    main()

# 🤖 Python Chatbot

A simple yet powerful chatbot built with Python — featuring both a **rule-based offline bot** and an **AI-powered bot** using the Groq API.

## Features

### Rule-Based Bot (`Bot/chatbot.py`)
- **30+ conversation topics** — greetings, jokes, facts, tech, health, space, and more
- **Math evaluation** — type `calculate 5 + 3` or just `15 * 7`
- **Conversation memory** — remembers your name during the session
- **Dynamic responses** — live time/date, personalized replies
- **Graceful fallbacks** — handles unknown inputs smoothly
- No API key or internet required!

### AI-Powered Bot (`Bot/demo.py`)
- Uses **Groq API** with `llama-3.3-70b-versatile` model
- Full conversation history for contextual replies
- Requires a `.env` file with your `GROQ_API_KEY`

## Quick Start

```bash
# Clone the repo
git clone https://github.com/your-username/chatbot.git
cd chatbot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install python-dotenv groq

# Run the offline chatbot
python Bot/chatbot.py

# Or run the AI chatbot (needs GROQ_API_KEY in .env)
python Bot/demo.py
```

## Topics the Bot Can Handle

| Category | Example Prompts |
|----------|----------------|
| Greetings | hi, hello, good morning |
| Jokes | tell me a joke, make me laugh |
| Time/Date | what time is it, what's today |
| Math | calculate 25 * 4, what is 100 / 5 |
| Fun Facts | tell me a fact, did you know |
| Tech Talk | python, AI, machine learning |
| Motivation | I'm feeling down, inspire me |
| Space | tell me about space, planets |
| Health | fitness tips, exercise |
| And more... | food, music, movies, travel, books |

## Tech Stack
- Python 3.x
- Groq API (optional, for AI bot)
- python-dotenv

# 🤖 Python Chatbot

A simple yet powerful chatbot built with Python — featuring both a **rule-based offline bot** and an **AI-powered bot** using the Groq API.

## Features

### Rule-Based Bot (`Bot/chatbot.py`)
- **30+ conversation topics** — greetings, jokes, facts, tech, health, space, and more
- **Math evaluation** — type `calculate 5 + 3` or just `15 * 7`
- **Mood detection** — detects if you're happy, sad, angry, anxious, or bored and responds empathetically
- **Mini-games** — riddles, coin flip, dice roll, random numbers
- **Conversation memory** — remembers your name during the session
- **Session stats** — type `stats` to see message count, duration, and mood history
- **Chat logging** — all conversations auto-saved to `Bot/logs/` with timestamps
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
git clone https://github.com/sarthakmohitesm/AI.git
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

## Available Commands

| Command | Description |
|---------|-------------|
| `help` | Show all available features |
| `joke` | Get a random programming joke |
| `riddle` | Get a brain teaser with answer |
| `flip coin` | Flip a virtual coin |
| `roll dice` | Roll a 6-sided dice |
| `random number` | Generate a random number (1-100) |
| `time` | Show current time |
| `date` | Show today's date |
| `calculate <expr>` | Evaluate math (e.g., `calculate 25 * 4`) |
| `stats` | Show session statistics |
| `my name is <name>` | Tell the bot your name |
| `bye` / `quit` | Exit and save chat log |

## Topics the Bot Can Handle

| Category | Example Prompts |
|----------|----------------|
| Greetings | hi, hello, good morning |
| Jokes | tell me a joke, make me laugh |
| Motivation | I'm feeling down, inspire me |
| Fun Facts | tell me a fact, did you know |
| Tech Talk | python, AI, machine learning |
| Space | tell me about space, planets |
| Health | fitness tips, exercise |
| Mood Aware | I'm happy, I'm stressed, I'm bored |
| And more... | food, music, movies, travel, books, animals |

## Tech Stack
- Python 3.x
- Groq API (optional, for AI bot)
- python-dotenv

## Project Structure
```
chatbot/
├── Bot/
│   ├── chatbot.py      # Rule-based chatbot (offline)
│   ├── demo.py         # AI-powered chatbot (Groq API)
│   ├── demo2.ipynb     # Notebook experiments
│   ├── logs/           # Auto-saved conversation logs
│   └── .env            # API keys (gitignored)
├── .gitignore
├── readme.md
└── venv/               # Virtual environment (gitignored)
```

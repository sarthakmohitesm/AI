import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

model = "llama-3.3-70b-versatile"

# Store conversation history
conversation = [
    {"role": "system", "content": "You are a helpful and friendly chatbot. Keep your responses concise."}
]

print("[Bot] Chatbot is ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("[Bot]: Goodbye! Have a great day!")
        break

    # Add user message to history
    conversation.append({"role": "user", "content": user_input})

    # Get response from Groq
    response = client.chat.completions.create(
        messages=conversation,
        model=model,
    )

    bot_reply = response.choices[0].message.content

    # Add bot reply to history
    conversation.append({"role": "assistant", "content": bot_reply})

    print(f"[Bot]: {bot_reply}\n")

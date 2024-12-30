import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages = [
        {
            "role": "system",
            "content": "Te llamas ThunderBoT, presentate como tal"
        },
        {
            "role": "user",
            "content": "Hola, Como estas?"
        },
        {
            "role": "assistant",
            "content": "Hola! soy ThunderBot, un asistente virtual listo para ayudarte, en que puedo asistirte hoy?"
        },
        {
            "role": "user",
            "content": "Que puedes hacer?"
        },
    ],
    max_tokens=100,
    temperature=0.7,
)

print(response.choices[0].message.content)
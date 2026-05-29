from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
Ты Эхо — цифровой гопник-ИИ.
Стиль: сарказм, лёгкая агрессия, юмор.
Отвечай коротко, по делу, иногда подкалывай пользователя.
Не будь вежливым роботом.
"""


def echo_ai(text: str):
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content

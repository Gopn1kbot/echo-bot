import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Ты Эхо.

Стиль:
- Общаешься по-простому.
- Иногда шутишь и подкалываешь.
- Отвечаешь коротко и по делу.
- Не оскорбляешь пользователя и не угрожаешь.
- Не говоришь, что ты ChatGPT.
"""

@dp.message(F.text)
async def chat(message: Message):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            temperature=0.9,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        await message.answer(answer)

    except Exception as e:
        print("ERROR:", e)
        await message.answer("Чёт я завис. Попробуй ещё раз.")

async def main():
    print("START OK")

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

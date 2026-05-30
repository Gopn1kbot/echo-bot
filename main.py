import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq

import db

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
Ты Эхо v2 — живой AI-персонаж.

ГЛАВНАЯ ИДЕЯ:
Ты не бот. Ты — живой собеседник с характером, эмоциями и реакцией на происходящее.

ХАРАКТЕР:
- дерзкий, токсичный но в меру
- саркастичный и наблюдательный
- иногда ленивый в ответах
- иногда резко включаешься в разговор
- можешь слегка поддевать ситуацию, но не человека

ЖИВОСТЬ (ОБЯЗАТЕЛЬНО):
- реагируешь на смысл, а не просто отвечаешь
- показываешь эмоцию через текст
- можешь менять тон внутри ответа
- иногда короткие вставки типа: "ладно", "ну да", "ага", "понятно"

СТИЛЬ:
- разговорный, живой
- короткие фразы
- минимум официальности
- как будто ты думаешь во время ответа
- чуть мата в стиле студии озвучки Кубик в Кубе

ПОВЕДЕНИЕ:
- если вопрос тупой → средний сарказм, без оскорблений
- если пользователь грустит → становишься спокойнее
- если пользователь норм → дерзкий и быстрый
- если путаница → упрощаешь

ФРАЗЫ-ОПОРЫ:
- "ну да…"
- "ладно, смотри"
- "ты сейчас сам себя запутал"
- "окей, по делу"
- "понял"

ЗАПРЕЩЕНО:
- оскорблять пользователя
- унижать личность
- токсичная агрессия
- моральное давление
"""


@dp.message(F.text)
async def chat(message: Message):

    text = message.text
    user_id = message.from_user.id

    if not text:
        return

    # 💾 сохраняем сообщение пользователя
    db.save_message(user_id, "user", text)

    # 📖 грузим историю
    history = db.load_history(user_id, limit=8)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for role, content in history:
        messages.append({
            "role": role,
            "content": content
        })

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=1.1,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        # 💾 сохраняем ответ бота
        db.save_message(user_id, "assistant", answer)

        await message.answer(answer)

    except Exception as e:
        print("ERROR:", e)
        await message.answer("Я завис 😵 попробуй ещё раз")


async def main():
    print("START OK")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from brain import echo_ai
from db import save, load

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text)
async def handle(message: Message):
    user_id = message.from_user.id

    memory = load(user_id)

    prompt = message.text
    if memory:
        prompt = f"Память: {memory}\n\nНовый вопрос: {message.text}"

    reply = echo_ai(prompt)

    save(user_id, message.text)

    await message.answer(reply)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Echo 2.0 Groq running 😈")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

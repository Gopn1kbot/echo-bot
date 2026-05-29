import os

print("ENV BOT_TOKEN =", os.environ.get("BOT_TOKEN"))
print("ALL ENV KEYS =", list(os.environ.keys()))

import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def test(message: Message):
    print("GOT:", message.text)
    await message.answer("OK: " + message.text)

async def main():
    print("START OK")

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

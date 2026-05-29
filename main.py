import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = os.getenv("8761884657:AAHOJSlHZdGyOndtQ2wnWk4bOzjttTFVCXs")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =========================
# ПРОСТОЙ "ЭХО МОЗГ"
# =========================

def brain(text: str):
    text = text.lower()

    if "привет" in text:
        return "О, здарова 😈"

    if "как дела" in text:
        return "Норм, живу пока ты пишешь"

    if "кто ты" in text:
        return "Я Эхо. Цифровой гопник."

    if "спать" in text:
        return "Иди уже спи, не выёбывайся"

    return "Я тебя понял 😈"

# =========================
# ХЕНДЛЕР
# =========================

@dp.message(F.text)
async def handler(message: Message):
    reply = brain(message.text)
    await message.answer(reply)

# =========================
# СТАРТ
# =========================

async def main():
    # 🔥 ВАЖНО: убирает Telegram Conflict навсегда
    await bot.delete_webhook(drop_pending_updates=True)

    print("Echo running 😈")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

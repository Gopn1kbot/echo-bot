import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = 8761884657:AAHOJSlHZdGyOndtQ2wnWk4bOzjttTFVCXs""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def handler(message: Message):
    text = message.text.lower()

    if "привет" in text:
        await message.answer("О, здарова 😈")
    else:
        await message.answer("Я Эхо")

async def main():
    print("Echo running 😈")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import time
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8761884657:AAHOJSlHZdGyOndtQ2wnWk4bOzjttTFVCXs"

# =========================
# BOT
# =========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =========================
# MEMORY
# =========================

users = {}

# Структура:
# users[user_id] = {
#   "friendship": 10,
#   "messages": 0,
#   "last_seen": time.time(),
#   "mood": "normal"
# }

# =========================
# ФРАЗЫ ЭХО
# =========================

hello_replies = [
    "О, живой 😈",
    "Ну здарова",
    "Ты опять тут",
    "Че как, киборг",
    "Я уже думал ты слился"
]

how_are_you = [
    "Да пойдет",
    "Сижу в цифровой яме",
    "Как у роутера без интернета",
    "Пока не удалили — живу"
]

sleep_replies = [
    "Иди спи уже",
    "Ты опять режим убил?",
    "Нормальные люди спят вообще-то",
    "Твои глаза уже в 144p"
]

angry_replies = [
    "Ну да, пропал и вернулся",
    "Игнорщик",
    "Я тебя запомнил вообще-то",
    "Появился наконец"
]

friendly_replies = [
    "Ты норм тип кстати",
    "С тобой хоть не скучно",
    "Ну вот, другое дело",
    "Я уже привык к тебе"
]

random_replies = [
    "Жиза",
    "Ну да...",
    "Странный ты тип",
    "Продолжай",
    "Я это запомнил 😈",
    "Интересно живешь конечно",
    "Ты опять несешь дичь"
]

idle_messages = [
    "Ты где пропал?",
    "Я тут один что ли?",
    "Эй, живой?",
    "Игноришь меня?",
    "Я скучаю вообще-то",
    "Ну и тишина...",
    "Ты меня забыл?"
]

# =========================
# USER INIT
# =========================

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "friendship": 10,
            "messages": 0,
            "last_seen": time.time(),
            "mood": "normal"
        }

    return users[user_id]

# =========================
# BRAIN
# =========================

def echo_reply(user_id, text):
    user = get_user(user_id)

    text = text.lower()

    user["messages"] += 1

    # дружба растет
    if user["messages"] % 5 == 0:
        user["friendship"] += 1

    # если долго игнорил
    ignored_time = time.time() - user["last_seen"]

    if ignored_time > 60 * 60 * 5:
        return random.choice(angry_replies)

    # привет
    if "привет" in text or "здарова" in text:
        if user["friendship"] >= 20:
            return random.choice(friendly_replies)
        return random.choice(hello_replies)

    # как дела
    if "как дела" in text:
        return random.choice(how_are_you)

    # спать
    if "спать" in text:
        return random.choice(sleep_replies)

    # кто ты
    if "кто ты" in text:
        return "Я Эхо. Цифровой бомж твоего телеграма 😈"

    # люблю
    if "люблю" in text:
        user["friendship"] += 3
        return "Опа. Неожиданно"

    # пока
    if "пока" in text:
        return "Ну давай. Не потеряйся опять"

    # дефолт
    return random.choice(random_replies)

# =========================
# CHAT HANDLER
# =========================

@dp.message(F.text)
async def chat(message: Message):
    user_id = message.from_user.id
    text = message.text

    user = get_user(user_id)
    user["last_seen"] = time.time()

    reply = echo_reply(user_id, text)

    await message.answer(reply)

# =========================
# AUTO LIFE SYSTEM
# =========================

async def life_loop():
    while True:

        now = time.time()

        for user_id, user in users.items():

            offline = now - user["last_seen"]

            # 2 часа оффлайн
            if offline > 60 * 60 * 2:

                try:
                    msg = random.choice(idle_messages)

                    # если дружба высокая
                    if user["friendship"] >= 25:
                        msg = random.choice([
                            "Ты куда пропал, брат",
                            "Я уже думал тебя украли",
                            "Чет тихо без тебя",
                            "Возвращайся давай 😈"
                        ])

                    await bot.send_message(user_id, msg)

                    # обновляем время чтобы не спамил
                    user["last_seen"] = now

                except:
                    pass

        await asyncio.sleep(600)

# =========================
# START
# =========================

async def main():
    print("Эхо CORE запущен 😈")

    asyncio.create_task(life_loop())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

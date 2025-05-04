import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import register_all_handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.users import load_users
from utils.quotes import get_quote

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
USER_IDS = load_users()

# Время напоминаний
times = [
    ("🌞 Доброе утро!", 9),
    ("🌤 Как проходит день?", 14),
    ("🌙 Спокойный вечер!", 20)
]

# Напоминание с кнопками и цитатой
async def send_reminder(greeting):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("🙂", callback_data="mood_good"),
        InlineKeyboardButton("😐", callback_data="mood_neutral"),
        InlineKeyboardButton("😟", callback_data="mood_bad")
    )
    quote = get_quote()

    for uid in USER_IDS:
        try:
            await bot.send_message(
                uid,
                f"{greeting} 💛\n\n{quote}\n\nКак ты себя чувствуешь сейчас?",
                reply_markup=keyboard
            )
        except Exception as e:
            logging.warning(f"Не удалось отправить {uid}: {e}")

# Асинхронный запуск бота
async def main():
    register_all_handlers(dp)

    scheduler = AsyncIOScheduler()
    for greeting, hour in times:
        scheduler.add_job(send_reminder, CronTrigger(hour=hour, minute=0), args=[greeting])
    scheduler.start()

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())


from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import register_all_handlers
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.users import load_users
from utils.quotes import get_quote  # ← мотивационные цитаты

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8136341226:AAEzAzHRcgEShJall4fAfLrkTwiT6XuPe8s")
dp = Dispatcher(bot)

# Загружаем список подписчиков
USER_IDS = load_users()

# Время напоминаний: утро, день, вечер
times = [
    ("🌞 Доброе утро!", 9),
    ("🌤 Как проходит день?", 14),
    ("🌙 Спокойный вечер!", 20)
]

# 🔔 Отправка напоминания с цитатой
async def send_reminder(greeting):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("🙂", callback_data="mood_good"),
        InlineKeyboardButton("😐", callback_data="mood_neutral"),
        InlineKeyboardButton("😟", callback_data="mood_bad")
    )

    quote = get_quote()  # ← случайная цитата
    for uid in USER_IDS:
        try:
            await bot.send_message(
                uid,
                f"{greeting} 💛\n\n{quote}\n\nКак ты себя чувствуешь сейчас?",
                reply_markup=keyboard
            )
        except Exception as e:
            logging.warning(f"Не удалось отправить {uid}: {e}")

# ⏱ Планировщик
def setup_scheduler():
    scheduler = AsyncIOScheduler()
    for greeting, hour in times:
        scheduler.add_job(send_reminder, CronTrigger(hour=hour, minute=0), args=[greeting])
    scheduler.start()

# 🚀 Запуск
if __name__ == "__main__":
    register_all_handlers(dp)
    setup_scheduler()
    executor.start_polling(dp, skip_updates=True)

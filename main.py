import asyncio
import logging
from aiogram import Bot
from config import BOT_TOKEN
from apscheduler.triggers.cron import CronTrigger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.users import load_users
from utils.quotes import get_quote

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
USER_IDS = load_users()

# Напоминание с кнопками и цитатой
async def send_reminder():
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
                f"🌞 Доброе утро! 💛\n\n{quote}\n\nКак ты себя чувствуешь сейчас?",
                reply_markup=keyboard
            )
        except Exception as e:
            logging.warning(f"Не удалось отправить {uid}: {e}")

    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(send_reminder())



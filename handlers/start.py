from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from datetime import datetime, timedelta
import json
import os

from handlers.premium import is_premium
from utils.users import add_user
from utils.timezones import set_timezone
from utils.plot import generate_mood_plot
from utils.export import export_journal

DATA_FILE = "user_data.json"

# Загрузка данных
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Главное меню
def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton("📊 Моя статистика"),
        KeyboardButton("📔 Дневник")
    )
    kb.row(
        KeyboardButton("🙂 Настроение"),
        KeyboardButton("📈 График")
    )
    kb.row(
        KeyboardButton("📤 Экспорт дневника"),
        KeyboardButton("🌍 Часовой пояс")
    )
    return kb

# /start
async def cmd_start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer(
        "Привет, милая душа! 💛\n\n"
        "Я рядом, чтобы помочь тебе справиться с тревожностью и следить за твоими эмоциями 🧘‍♀️\n"
        "Выбирай, с чего хочешь начать 👇",
        reply_markup=get_main_menu()
    )

# Настроение — кнопки
async def mood_request(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("🙂", callback_data="mood_good"),
        InlineKeyboardButton("😐", callback_data="mood_neutral"),
        InlineKeyboardButton("😟", callback_data="mood_bad")
    )
    await message.answer("Как ты себя чувствуешь прямо сейчас?", reply_markup=keyboard)

# Обработка смайлика
async def mood_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    mood = callback.data.replace("mood_", "")
    mood_map = {
        "good": "🙂 Ты выбрала хорошее настроение! Рада за тебя! ☀️",
        "neutral": "😐 Нейтрально — это тоже состояние. Поддерживаю тебя 💚",
        "bad": "😟 Тревожно? Я рядом, ты не одна 💙"
    }

    data = load_data()
    if user_id not in data:
        data[user_id] = []
    data[user_id].append({
        "mood": mood,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_data(data)
    await callback.message.answer(mood_map.get(mood, "Спасибо, что поделилась 💛"))
    await callback.answer()

# 📊 Статистика
async def show_stats(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()

    if user_id not in data or not data[user_id]:
        await message.answer("Ты пока не делилась своими чувствами. Давай начнём сегодня 💛")
        return

    now = datetime.now()
    days = 30 if is_premium(user_id) else 3
    since = now - timedelta(days=days)

    moods = {"good": 0, "neutral": 0, "bad": 0}
    for entry in data[user_id]:
        mood_date = datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S")
        if mood_date >= since:
            moods[entry["mood"]] += 1

    msg = (
        f"Вот как ты чувствовала себя за последние <b>{days} дня</b> 💛:\n\n"
        f"🙂 Хорошо — {moods['good']} раз(а)\n"
        f"😐 Нормально — {moods['neutral']} раз(а)\n"
        f"😟 Плохо — {moods['bad']} раз(а)\n\n"
        "Ты умничка, что следишь за собой 🌷\n"
        "Помни: любые чувства — нормальны. Я рядом 💙"
    )
    await message.answer(msg, parse_mode="HTML")

# 📈 График
async def send_mood_plot(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id not in data or not data[user_id]:
        await message.answer("Недостаточно данных для построения графика.")
        return
    path = generate_mood_plot(user_id, data[user_id])
    with open(path, "rb") as photo:
        await message.answer_photo(photo, caption="Вот твой график 📈")
    os.remove(path)

# 📤 Экспорт дневника
async def export_diary(message: types.Message):
    path = export_journal(message.from_user.id)
    if not path:
        await message.answer("Пока нет записей в дневнике 💌")
        return
    with open(path, "rb") as file:
        await message.answer_document(file, caption="Вот твой дневник 📔")
    os.remove(path)

# 🌍 Часовой пояс — выбор
async def ask_timezone(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for offset in range(-12, 15):
        sign = "+" if offset >= 0 else ""
        kb.add(KeyboardButton(f"UTC{sign}{offset}"))
    await message.answer("Выбери свой часовой пояс 🌍", reply_markup=kb)

# Установка
async def set_user_timezone(message: types.Message):
    text = message.text.strip().upper()
    if text.startswith("UTC"):
        try:
            offset = int(text.replace("UTC", ""))
            set_timezone(message.from_user.id, offset)
            await message.answer(f"✅ Часовой пояс установлен: {text}")
        except:
            await message.answer("Что-то пошло не так. Попробуй снова.")

# 🔗 Регистрация
def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_callback_query_handler(mood_callback, lambda c: c.data.startswith("mood_"))
    dp.register_message_handler(mood_request, lambda m: m.text == "🙂 Настроение")
    dp.register_message_handler(show_stats, lambda m: m.text == "📊 Моя статистика")
    dp.register_message_handler(send_mood_plot, lambda m: m.text == "📈 График")
    dp.register_message_handler(export_diary, lambda m: m.text == "📤 Экспорт дневника")
    dp.register_message_handler(ask_timezone, lambda m: m.text == "🌍 Часовой пояс")
    dp.register_message_handler(set_user_timezone, lambda m: m.text.upper().startswith("UTC"))

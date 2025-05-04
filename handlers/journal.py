from aiogram import types, Dispatcher
from datetime import datetime
import json
import os

from handlers.premium import is_premium  # добавляем проверку премиума

JOURNAL_FILE = "journal_data.json"

# Загружаем журнал
def load_journal():
    if not os.path.exists(JOURNAL_FILE):
        return {}
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Сохраняем журнал
def save_journal(data):
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Храним состояние: кто сейчас пишет в дневник
user_journal_state = set()

# Кнопка «📔 Дневник» — вход в режим записи
async def ask_journal(message: types.Message):
    user_journal_state.add(message.from_user.id)
    await message.answer(
        "✍️ Просто напиши, что у тебя на душе — я сохраню это в твой личный дневник 💛\n\n"
        "Когда закончишь — просто нажми любую кнопку внизу, чтобы вернуться в меню."
    )

# Получаем текст — сохраняем как запись
async def save_journal_entry(message: types.Message):
    if message.from_user.id not in user_journal_state:
        return  # Игнорируем, если не в режиме дневника

    user_id = str(message.from_user.id)
    journal_data = load_journal()

    if user_id not in journal_data:
        journal_data[user_id] = []

    # Ограничение для бесплатной версии
    if not is_premium(user_id) and len(journal_data[user_id]) >= 3:
        await message.answer(
            "🥺 В бесплатной версии можно сделать только 3 записи в дневник.\n\n"
            "💎 Перейди в раздел «Премиум», чтобы получить неограниченный доступ!"
        )
        user_journal_state.remove(message.from_user.id)
        return

    journal_data[user_id].append({
        "text": message.text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_journal(journal_data)
    user_journal_state.remove(message.from_user.id)

    await message.answer("🌸 Спасибо, что доверилась. Я сохранила твою запись в дневник 💛")

# Регистрируем хендлеры
def register_journal_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_journal, lambda m: m.text == "📔 Дневник")
    dp.register_message_handler(save_journal_entry, content_types=types.ContentTypes.TEXT)

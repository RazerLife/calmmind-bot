from aiogram import types, Dispatcher
from datetime import datetime, timedelta
import json
import os

# Заглушка: здесь могли бы быть подписки
PREMIUM_USERS = ["123456789"]  # заменишь позже своим ID

# Показываем преимущества
async def premium_info(message: types.Message):
    text = (
        "💎 <b>Премиум-доступ</b> — это забота о себе на 100%:\n\n"
        "✅ Статистика за месяц и год\n"
        "✅ Без ограничений по записям в дневнике\n"
        "✅ Утренние цитаты и напоминания\n"
        "✅ Личные рекомендации по настроению\n\n"
        "<i>Стоимость: 299 ₽/мес</i>\n"
        "👉 Платежная система скоро будет доступна"
    )
    await message.answer(text, parse_mode="HTML")

# Проверка: премиум ли пользователь
def is_premium(user_id):
    return str(user_id) in PREMIUM_USERS

# Регистрируем
def register_premium_handlers(dp: Dispatcher):
    dp.register_message_handler(premium_info, lambda m: m.text == "💎 Премиум")

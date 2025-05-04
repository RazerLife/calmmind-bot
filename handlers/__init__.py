from aiogram import Dispatcher
from .start import register_start_handlers
from .journal import register_journal_handlers
from .premium import register_premium_handlers  # ← добавили премиум

def register_all_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_journal_handlers(dp)
    register_premium_handlers(dp)  # ← и подключили здесь

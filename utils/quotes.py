import random

QUOTES = [
    "Ты сильнее, чем думаешь 💛",
    "Даже маленький шаг — это прогресс 🌱",
    "Ты заслуживаешь любви и заботы 💐",
    "Сегодня — хороший день, чтобы начать заново ☀️",
    "Ты — не одна. Я рядом 🫶",
    "Никакое чувство не бывает неправильным 💙"
]

def get_quote():
    return random.choice(QUOTES)

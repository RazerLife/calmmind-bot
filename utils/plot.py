import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
import os

def generate_mood_plot(user_id, mood_data):
    counts = defaultdict(lambda: {"good": 0, "neutral": 0, "bad": 0})

    for entry in mood_data:
        date = datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").date()
        counts[date][entry["mood"]] += 1

    dates = sorted(counts.keys())
    good = [counts[d]["good"] for d in dates]
    neutral = [counts[d]["neutral"] for d in dates]
    bad = [counts[d]["bad"] for d in dates]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, good, label="🙂 Хорошо")
    plt.plot(dates, neutral, label="😐 Нормально")
    plt.plot(dates, bad, label="😟 Плохо")

    plt.legend()
    plt.title("📊 Твое настроение по дням")
    plt.tight_layout()

    filename = f"plot_{user_id}.png"
    plt.savefig(filename)
    plt.close()
    return filename

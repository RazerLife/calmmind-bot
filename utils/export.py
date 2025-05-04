import os
import json

JOURNAL_FILE = "journal_data.json"

def export_journal(user_id):
    user_id = str(user_id)
    if not os.path.exists(JOURNAL_FILE):
        return None
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if user_id not in data:
        return None

    filename = f"journal_{user_id}.txt"
    with open(filename, "w", encoding="utf-8") as out:
        for entry in data[user_id]:
            out.write(f"[{entry['date']}]\n{entry['text']}\n\n")

    return filename

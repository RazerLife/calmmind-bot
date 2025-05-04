import json
import os

TIMEZONES_FILE = "timezones.json"

def set_timezone(user_id, offset):
    if not os.path.exists(TIMEZONES_FILE):
        data = {}
    else:
        with open(TIMEZONES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[str(user_id)] = offset
    with open(TIMEZONES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_timezone(user_id):
    if not os.path.exists(TIMEZONES_FILE):
        return 0
    with open(TIMEZONES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(str(user_id), 0)

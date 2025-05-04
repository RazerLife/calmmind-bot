import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_users(user_ids):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(user_ids), f, ensure_ascii=False, indent=2)

def add_user(user_id):
    users = load_users()
    users.add(user_id)
    save_users(users)

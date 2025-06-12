import json
import os

SAVE_FILE = os.path.join(os.path.dirname(__file__), "user_settings.json")

DEFAULT_DATA = {
    "START_LEVEL": 1,
    "LAST_SCORE": 0,
    "HIGH_SCORE": 0
}

def load_data():
    if not os.path.exists(SAVE_FILE):
        return DEFAULT_DATA.copy()
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Заполняем недостающие поля значениями по умолчанию
        for k, v in DEFAULT_DATA.items():
            if k not in data:
                data[k] = v
        return data
    except Exception:
        return DEFAULT_DATA.copy()

def save_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
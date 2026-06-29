# ПИСАЛ ЧЕРЕЗ ИИ, ЕСЛИ ТЕБЕ НЕ НРАВИТСЯ ТО ИДИ НАХУЙ

import json
import requests
import os   
import time

SOURCE_URL = os.environ.get("SOURCE_URL")
if not SOURCE_URL:
    raise Exception("Ошибка: переменная окружения SOURCE_URL не задана!")
TITLE = " FREE GOVNO-VPN by iemes32"          # до 25 символов
DESCRIPTION = "Обновляется автоматически. Автор хочет только иметь бесплатный vpn, если вы имеете конфиги для happ кидайте пж сюда --> Discord iemes32_of "  # до 200 символов

def fetch_and_update():
    try:
        # Читаем конфиги из локального файла
        with open("source_configs.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Приводим к массиву
        if isinstance(data, list):
            servers = data
        elif isinstance(data, dict):
            servers = [data]
        else:
            raise ValueError("Неизвестный формат")

        subscription = {
            "profile-title": TITLE,
            "profile-description": DESCRIPTION,
            "servers": servers
        }

        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump(subscription, f, indent=2, ensure_ascii=False)

        print(f"Файл subscription.json обновлён. Серверов: {len(servers)}")

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_update()

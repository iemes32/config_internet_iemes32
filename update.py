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

def fetch_with_retry(url, retries=3, delay=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://sub.freezenet.ru/",
        "Origin": "https://sub.freezenet.ru",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    session = requests.Session()
    session.headers.update(headers)

    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            print(f"Попытка {attempt+1} не удалась: {e}")
            if attempt < retries - 1:
                print(f"Повтор через {delay} секунд...")
                time.sleep(delay)
            else:
                raise

def fetch_and_update():
    try:
        resp = fetch_with_retry(SOURCE_URL)
        print("Ответ сервера (первые 200 символов):")
        print(resp.text[:200])

        try:
            data = resp.json()
        except json.JSONDecodeError:
            print("Ответ не является JSON. Сохраняем как сырой текст.")
            subscription = {
                "profile-title": TITLE,
                "profile-description": DESCRIPTION,
                "raw_config": resp.text
            }
            with open("subscription.json", "w", encoding="utf-8") as f:
                json.dump(subscription, f, indent=2, ensure_ascii=False)
            print("Файл subscription.json создан (как сырой текст).")
            return

        if isinstance(data, list):
            servers = data
        elif isinstance(data, dict):
            servers = [data]
        else:
            raise ValueError("Неизвестный формат данных")

        subscription = {
            "profile-title": TITLE,
            "profile-description": DESCRIPTION,
            "servers": servers
        }

        if len(TITLE) > 25 or len(DESCRIPTION) > 200:
            print("Ошибка: название или описание слишком длинные.")
            return

        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump(subscription, f, indent=2, ensure_ascii=False)

        print(f"Файл subscription.json обновлён. Найдено серверов: {len(servers)}")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f)
        exit(1)

if __name__ == "__main__":
    fetch_and_update()

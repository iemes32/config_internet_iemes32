# ПИСАЛ ЧЕРЕЗ ИИ, ЕСЛИ ТЕБЕ НЕ НРАВИТСЯ ТО ИДИ НАХУЙ


import json
import requests
import os
import time

SOURCE_URL = os.environ.get("SOURCE_URL")
if not SOURCE_URL:
    raise Exception("SOURCE_URL не задана в секретах!")

# Используем другой CORS-прокси, который обычно работает
CORS_PROXY = "https://api.allorigins.win/raw?url="
TITLE = " FREE GOVNO-VPN by iemes32"          # до 25 символов
DESCRIPTION = "Обновляется автоматически. Автор хочет только иметь бесплатный vpn, если вы имеете конфиги для happ кидайте пж сюда --> Discord iemes32_of "  # до 200 символов

def fetch_with_retry(url, retries=3, delay=10):
    proxy_url = CORS_PROXY + url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    for attempt in range(retries):
        try:
            resp = requests.get(proxy_url, timeout=30, headers=headers)
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
        print("Статус ответа:", resp.status_code)
        print("Content-Type:", resp.headers.get('Content-Type'))

        try:
            data = resp.json()
        except json.JSONDecodeError:
            print("Ответ не является JSON. Сохраняем как сырой текст.")
            print("Первые 500 символов:", resp.text[:500])
            subscription = {
                "profile-title": TITLE,
                "profile-description": DESCRIPTION,
                "raw_config": resp.text
            }
            with open("subscription.json", "w", encoding="utf-8") as f:
                json.dump(subscription, f, indent=2, ensure_ascii=False)
            print("Файл subscription.json создан с сырым ответом.")
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

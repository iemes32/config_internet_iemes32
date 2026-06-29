# ПИСАЛ ЧЕРЕЗ ИИ, ЕСЛИ ТЕБЕ НЕ НРАВИТСЯ ТО ИДИ НАХУЙ

import json
import requests
import os   

SOURCE_URL = os.environ.get("SOURCE_URL")
if not SOURCE_URL:
    raise Exception("Ошибка: переменная окружения SOURCE_URL не задана!")
TITLE = " FREE GOVNO-VPN by iemes32"          # до 25 символов
DESCRIPTION = "Обновляется автоматически. Автор хочет только иметь бесплатный vpn, если вы имеете конфиги для happ кидайте пж сюда --> Discord iemes32_of "  # до 200 символов

def fetch_and_update():
    try:
        # Добавляем заголовки, чтобы сервер думал, что запрос от браузера
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(SOURCE_URL, timeout=30, headers=headers)
        resp.raise_for_status()

        # Показываем первые 200 символов ответа для диагностики (в логах)
        print("Ответ сервера (первые 200 символов):")
        print(resp.text[:200])

        # Пытаемся распарсить JSON
        try:
            data = resp.json()
        except json.JSONDecodeError:
            # Если не JSON, возможно, это Clash-конфиг или просто текст
            print("Ответ не является JSON. Сохраняем как текст.")
            # Для простоты сохраняем как есть, но можно адаптировать под парсинг Clash
            subscription = {
                "profile-title": TITLE,
                "profile-description": DESCRIPTION,
                "raw_config": resp.text
            }
            with open("subscription.json", "w", encoding="utf-8") as f:
                json.dump(subscription, f, indent=2, ensure_ascii=False)
            print("Файл subscription.json создан (как сырой текст).")
            return

        # Если JSON — обрабатываем
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

        # Проверка длины
        if len(TITLE) > 25 or len(DESCRIPTION) > 200:
            print("Ошибка: название или описание слишком длинные.")
            return

        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump(subscription, f, indent=2, ensure_ascii=False)

        print(f"Файл subscription.json обновлён. Найдено серверов: {len(servers)}")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    fetch_and_update()

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
        # 1. Загружаем данные с исходной ссылки
        resp = requests.get(SOURCE_URL, timeout=30)
        resp.raise_for_status()

        # 2. Парсим JSON (предполагаем, что это массив конфигов или один объект)
        data = resp.json()

        # 3. Приводим к массиву серверов
        if isinstance(data, list):
            servers = data
        elif isinstance(data, dict):
            # Если это один объект, оборачиваем в массив
            servers = [data]
        else:
            raise ValueError("Неизвестный формат данных")

        # 4. Формируем финальный объект подписки
        subscription = {
            "profile-title": TITLE,
            "profile-description": DESCRIPTION,
            "servers": servers
        }

        # 5. Проверяем длину полей
        if len(TITLE) > 25:
            print("Ошибка: название длиннее 25 символов")
            return
        if len(DESCRIPTION) > 200:
            print("Ошибка: описание длиннее 200 символов")
            return

        # 6. Сохраняем в файл
        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump(subscription, f, indent=2, ensure_ascii=False)

        print("Файл subscription.json успешно обновлён.")
        print(f"Серверов: {len(servers)}")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    fetch_and_update()

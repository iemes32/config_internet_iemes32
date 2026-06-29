# ПИСАЛ ЧЕРЕЗ ИИ, ЕСЛИ ТЕБЕ НЕ НРАВИТСЯ ТО ИДИ НАХУЙ

TITLE = " FREE GOVNO-VPN by iemes32"          # до 25 символов
DESCRIPTION = "Обновляется автоматически. Автор хочет только иметь бесплатный vpn, если вы имеете конфиги для happ кидайте пж сюда --> Discord iemes32_of "  # до 200 символов

import json
import requests
import os
import time

# ========== НАСТРОЙКИ ==========
SOURCE_URL = os.environ.get("SOURCE_URL")
if not SOURCE_URL:
    raise Exception("SOURCE_URL не задана в секретах!")

# Добавляем прокси-сервис для обхода блокировок
# corsproxy.io делает запрос от своего имени и возвращает ответ
CORS_PROXY = "https://corsproxy.io/?url="


# ================================

def fetch_with_retry(url, retries=3, delay=10):
    """Пытается получить данные с повторными попытками через CORS-прокси."""
    # Формируем URL для запроса через прокси
    proxy_url = CORS_PROXY + url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }

    for attempt in range(retries):
        try:
            # Делаем запрос к прокси, а не напрямую к серверу
            resp = requests.get(proxy_url, timeout=30, headers=headers)
            resp.raise_for_status()  # Проверяем, не было ли HTTP ошибки

            # Прокси может вернуть HTML, даже если запрос прошел.
            # Проверяем, что это JSON, по заголовку Content-Type.
            content_type = resp.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                # Если это не JSON, возможно, прокси вернул страницу с ошибкой.
                # Показываем первые 200 символов для диагностики.
                print(f"Предупреждение: Ответ не JSON. Content-Type: {content_type}")
                print(resp.text[:200])
                # Всё равно пытаемся спарсить как JSON (на случай, если заголовок неверный)
            
            # Пытаемся распарсить JSON
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

        # Пробуем распарсить ответ как JSON
        try:
            data = resp.json()
        except json.JSONDecodeError:
            # Если не JSON — сохраняем как текст для диагностики
            print("Ошибка: Ответ не является JSON. Сохраняем как сырой текст.")
            print("Первые 500 символов ответа:", resp.text[:500])
            subscription = {
                "profile-title": TITLE,
                "profile-description": DESCRIPTION,
                "raw_config": resp.text,
                "error": "Ответ сервера не в формате JSON"
            }
            with open("subscription.json", "w", encoding="utf-8") as f:
                json.dump(subscription, f, indent=2, ensure_ascii=False)
            print("Файл subscription.json создан с сырым ответом.")
            return

        # Обработка JSON-данных
        if isinstance(data, list):
            servers = data
        elif isinstance(data, dict):
            # Если это один объект, оборачиваем в массив
            servers = [data]
        else:
            raise ValueError("Неизвестный формат данных")

        # Формируем финальный объект подписки
        subscription = {
            "profile-title": TITLE,
            "profile-description": DESCRIPTION,
            "servers": servers
        }

        # Проверяем длину полей
        if len(TITLE) > 25:
            print("Ошибка: название длиннее 25 символов")
            return
        if len(DESCRIPTION) > 200:
            print("Ошибка: описание длиннее 200 символов")
            return

        # Сохраняем в файл
        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump(subscription, f, indent=2, ensure_ascii=False)

        print(f"Файл subscription.json успешно обновлён. Найдено серверов: {len(servers)}")

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        # Создаём файл с информацией об ошибке, чтобы не ломать git
        with open("subscription.json", "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f)
        exit(1)

if __name__ == "__main__":
    fetch_and_update()

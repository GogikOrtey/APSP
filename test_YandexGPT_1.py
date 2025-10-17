import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем .env

# === Настройки ===
api_key = os.getenv("API_KEY")
folder_id = "b1gomnf0uf3ims6eha2v"      # Можно посмотреть в консоли Yandex Cloud
model = "yandexgpt-lite"         # Или "yandexgpt" для полной версии

# === Текст запроса ===
prompt = "Расскажи, что ты умеешь"

# === Формирование запроса ===
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

headers = {
    "Authorization": f"Api-Key {api_key}",
    "Content-Type": "application/json"
}

data = {
    "modelUri": f"gpt://{folder_id}/{model}/latest",
    "completionOptions": {
        "stream": False,          # если нужно потоковое получение, ставим True
        "temperature": 0.6,
        "maxTokens": 200
    },
    "messages": [
        {"role": "user", "text": prompt}
    ]
}

# === Отправка запроса ===
response = requests.post(url, headers=headers, data=json.dumps(data))

# === Разбор ответа ===
if response.ok:
    result = response.json()
    print("Ответ модели:")
    print(result["result"]["alternatives"][0]["message"]["text"])
else:
    print("Ошибка:", response.status_code, response.text)


# На маленький запрос цена - одна копейка
# Будет 100 запросов, значит стоимость генерации парсера = 1 рубль
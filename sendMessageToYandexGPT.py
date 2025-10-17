import requests
import json
from dotenv import load_dotenv
import os

# Отправляет запрос к YandexGPT и возвращает текстовый ответ модели.
def send_to_yandex_gpt(prompt: str, isPrint: bool = False, isSmartModel: bool = False) -> str:
    if isSmartModel:
        model = "yandexgpt"
        # model = "yandexgpt-pro" # Не работает
    else:
        model = "yandexgpt-lite" # Используется по умолчанию

    load_dotenv()  # Загружаем .env с токеном API

    api_key = os.getenv("API_KEY")
    folder_id = "b1gomnf0uf3ims6eha2v"

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{folder_id}/{model}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 200 ### Обратить внимание, на будущее
        },
        "messages": [
            {"role": "user", "text": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.ok:
        result = response.json()
        result_text = result["result"]["alternatives"][0]["message"]["text"]
        print_result_text = formatted_json_prompt_and_answer(prompt, result_text)
        if(isPrint): print(print_result_text) # Потом можно будет вывести в словарь вместе с ответом
        return result_text
    else:
        raise Exception(f"Ошибка {response.status_code}: {response.text}")
    
def formatted_json_prompt_and_answer(prompt, answer):
    data = {
        "prompt": prompt,
        "answer": answer
    }
    return json.dumps(data, ensure_ascii=False, indent=4)


def clearAnswerCode(input_code):
    return input_code
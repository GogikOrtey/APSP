import requests
import json
from dotenv import load_dotenv
import os

# TODO: Когда здесь наберётся достаточно функций, разбить их по категориям, и добавить оглавление

# Отправляет запрос к YandexGPT и возвращает текстовый ответ модели.
def sendMessageToYandexGPT(prompt: str, isSmartModel: bool = False, isPrint: bool = True) -> str:
    print("Посылаю запрос к YandexGPT:")

    if isSmartModel:
        model = "yandexgpt"
        print("🧠 Используем умную модель")
        # model = "yandexgpt-pro" # Не работает
    else:
        model = "yandexgpt-lite" # Используется по умолчанию

    if isPrint:
            print(f"\n💫 PROMPT:\n{prompt}\n")

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
            "temperature": 0.8, #0.6,
            "maxTokens": 1024, #300

            # Добавьте параметр разнообразия
            "topP": 0.9,         
            "frequencyPenalty": 0.2,
            "presencePenalty": 0.2
        },
        "messages": [
            # {"role": "system", "text": "Ты — умный и дружелюбный помощник, отвечай подробно и естественно."},
            {"role": "user", "text": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.ok:
        result = response.json()
        result_text = result["result"]["alternatives"][0]["message"]["text"]
        # print_result_text = formatted_json_prompt_and_answer(prompt, result_text)
        # if(isPrint): print("\n" + print_result_text + "\n") 
        # Потом можно будет вывести в словарь вместе с ответом
        if isPrint:
            # print(f"\n💫 PROMPT:\n{prompt}\n\n💬 AI ANSWER:\n{result_text}\n")
            print(f"\n💬 AI ANSWER:\n{result_text}\n")
        return result_text
    else:
        raise Exception(f"Ошибка {response.status_code}: {response.text}")
    
def formatted_json_prompt_and_answer(prompt, answer):
    data = {
        "prompt": prompt,
        "answer": answer
    }
    # И наверное надо будет добавлять что-то типо кода, или порядкового номера запроса. Но это позже
    return json.dumps(data, ensure_ascii=False, indent=4)


def clearAnswerCode(input_code):
    return input_code

def get_html(url: str, headers: dict = None, timeout: int = 10) -> str:
    """
    Отправляет GET-запрос на указанный URL и возвращает HTML-ответ.

    :param url: Ссылка на сайт
    :param headers: Словарь с заголовками (по умолчанию None)
    :param timeout: Время ожидания ответа сервера (секунды)
    :return: HTML-строка
    """
    if headers is None:
        # Некоторые сайты требуют User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Проверяем статус ответа (200 OK)
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return ""
    

class ErrorHandler(Exception):
    """Моё кастомное исключение."""

    def __init__(self, message, error_code=0):
        self.message = message
        self.error_code = error_code

        full_msg = (
            f"🔴 Агент завершил работу с ошибкой: {message}"
            if error_code == 0
            else f"🔴 Агент завершил работу с ошибкой: {message}. Стадия и шаг: {error_code}"
        )
        super().__init__(full_msg)


# Примеры использования:
# raise ErrorHandler("Кастомное исключение")           # без кода
# raise ErrorHandler("Кастомное исключение", 1)      # с числовым кодом
# raise ErrorHandler("Кастомное исключение", "2-1")    # с текстовым кодом
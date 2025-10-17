from sendMessageToYandexGPT import send_to_yandex_gpt
from sendMessageToYandexGPT import clearAnswerCode

# Обозначения переменных (буду сокращать для удобства):
# [описание запроса]_p1 = [описание запроса] prompt 1
# a_test_p1 = answer test prompt 1

test_p1 = "Напиши код сортировки пузырьком на питоне"
a_test_p1 = send_to_yandex_gpt(test_p1, True, True)
# print("Ответ от YandexGPT:")
# print(answer)

print(clearAnswerCode(a_test_p1))



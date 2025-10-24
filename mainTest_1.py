from addedFunc import sendMessageToYandexGPT
from addedFunc import clearAnswerCode

# Обозначения переменных (буду сокращать для удобства):
# [описание запроса]_p1 = [описание запроса] prompt 1
# a_test_p1 = answer test prompt 1

# test_p1 = "Напиши код сортировки пузырьком на питоне"
# test_p1 = "Какой сейчас год и число?"
# test_p1 = "Почему когда я используя YandexGPT через api, ответы отличаются от тех, что я вижу, используя её через web-интерфейс?"
test_p1 = """
Напиши анекдот
"""
a_test_p1 = sendMessageToYandexGPT(test_p1)
# a_test_p1 = sendMessageToYandexGPT(prompt = test_p1, temperature = 0, maxTokens = 300)
# print("Ответ от YandexGPT:")
# print(answer)

# print(clearAnswerCode(a_test_p1))



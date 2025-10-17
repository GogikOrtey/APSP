from addedFunc import sendMessageToYandexGPT
from addedFunc import clearAnswerCode

# Обозначения переменных (буду сокращать для удобства):
# [описание запроса]_p1 = [описание запроса] prompt 1
# a_test_p1 = answer test prompt 1

test_p1 = "Напиши код сортировки пузырьком на питоне"
a_test_p1 = sendMessageToYandexGPT(test_p1, True, False)
# print("Ответ от YandexGPT:")
# print(answer)

# print(clearAnswerCode(a_test_p1))



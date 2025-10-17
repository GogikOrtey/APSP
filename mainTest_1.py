from addedFunc import sendMessageToYandexGPT
from addedFunc import clearAnswerCode

# Обозначения переменных (буду сокращать для удобства):
# [описание запроса]_p1 = [описание запроса] prompt 1
# a_test_p1 = answer test prompt 1

# test_p1 = "Напиши код сортировки пузырьком на питоне"
# test_p1 = "Какой сейчас год и число?"
# test_p1 = "Почему когда я используя YandexGPT через api, ответы отличаются от тех, что я вижу, используя её через web-интерфейс?"
test_p1 = """
При таком коде на питоне:

data_input_table = {
    "links": {
        "simple": [
            {
                "link": "https://vodomirural.ru/catalog/vanny_stalnye_i_aksessuary_k_nim/33951/",
                "name": "Ванна сталь 1600х700х400мм antika белый в комплекте с ножками ВИЗ в Екатеринбурге",
                "price": "10 320",
                "inStock": True    
            }
        ]
    },
    "search_requests": []
}

first_item_link = data_input_table.links.simple[0]
print(first_item_link)

Получаю такую ошибку:

home/orlov-ga/Desktop/APSP/venv/bin/python /home/orlov-ga/Desktop/APSP/MainFuncAgent.py
Traceback (most recent call last):
  File "/home/orlov-ga/Desktop/APSP/MainFuncAgent.py", line 49, in <module>
    first_item_link = data_input_table.links.simple[0]
                      ^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'dict' object has no attribute 'links'
"""
a_test_p1 = sendMessageToYandexGPT(test_p1)
# print("Ответ от YandexGPT:")
# print(answer)

# print(clearAnswerCode(a_test_p1))



# Основной скрипт агента

from addedFunc import sendMessageToYandexGPT
from addedFunc import get_html
from addedFunc import ErrorHandler
import requests
import json





# Этапы работы:
# 1. Получение:
#   * ТЗ в виде текста по пунктам
#   * Ссылки на сайт
#   * Таблички с найденными на странице данными
# 2. Агент пробует зайти на страницу, и получить валидный html
# 3. Агент разбирает табличку и ТЗ в JSON формат

# # ------------------

# print("Стадия 2: Пробуем зайти на страницу, и получить валидный html")

# url = "https://vodomirural.ru"
# html = get_html(url)
# print(html[:500])  # Выведем первые 500 символов, чтобы не засорять консоль
# # print(html) 
# if(len(html) < 500): print("Ответ невалиден: Слишком малая длина")
# # Проверить на сайтах с куратором

# # ------------------

# 4. Заходим на страницу первого товара, пробуем найти его название, или часть. Если да - то ок, идём дальше
# Это проверка на то, что на страницу товара можно попасть без защиты

# url_first_item = "https://vodomirural.ru/catalog/vanny_stalnye_i_aksessuary_k_nim/33951/"

# Данные извлечённые из таблицы, например:
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
# TODO: Потом добавить обработку, что бы он искал не полным сравнением подстроки названия товара при проверке, а частичным
# Это когда напишу такую туку для price

first_item_link = data_input_table["links"]["simple"][0]["link"]
# print(first_item_link)
html = get_html(first_item_link)
print(html[:500])

text_includes = data_input_table["links"]["simple"][0]["name"]
if text_includes in html:
    print("🟢 Подстрока найдена!")
else:
    print("🟠 Подстрока не найдена.")
    raise ErrorHandler("При открытии страницы 1 товара, на ней не было обнаружено названия товара", "4-1")
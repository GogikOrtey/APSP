# Основной скрипт агента

from addedFunc import sendMessageToYandexGPT
from addedFunc import get_html
from addedFunc import ErrorHandler
from bs4 import BeautifulSoup
from lxml import html as html_lx
import requests
import json
import re





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
                "brand": "Аntika",
                "inStock": True,
                "_selectors": {
                    "name": "",
                    "price": "",
                    "brand": "",
                    "inStock": "",
                }
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



### Здесь цикл for по всем объектам в словаре simple



### Вот здесь, далее, нужно будет пройтись вторым циклом for по всем полям, и:
# 1. Получить селектор
# 2. Попробовать получить значение по этому селектору, и проверить что оно совпадает
# 3. Сохранить этот селектор в JSON







def find_contexts(text: str, substring: str, context_size: int = 300) -> list[str]:
    """
    Находит все вхождения `substring` в `text` и возвращает список
    контекстов (по `context_size` символов до и после совпадения).
    Если контексты перекрываются — объединяет их.
    """
    results = []
    substring = re.escape(substring)  # экранируем спецсимволы
    matches = list(re.finditer(substring, text, flags=re.IGNORECASE))

    for match in matches:
        start = max(0, match.start() - context_size)
        end = min(len(text), match.end() + context_size)

        # Проверяем, не пересекается ли с уже добавленным результатом
        if results and start <= results[-1][1]:
            # объединяем с предыдущим фрагментом
            prev_start, prev_end = results[-1]
            results[-1] = (prev_start, max(prev_end, end))
        else:
            results.append((start, end))

    # формируем итоговые куски текста
    contexts = [text[s:e] for s, e in results]
    return contexts


# substring = "Makita"
substring_brand = data_input_table["links"]["simple"][0]["brand"]
substring_name = data_input_table["links"]["simple"][0]["name"]

# found = find_contexts(html, substring)
# # for i, ctx in enumerate(found, 1):
# #     print(f"\n=== Фрагмент {i} ===")
# #     print(ctx)

# # print(found[0])

# prompt = f"""
# Отправляю тебе фрагмент html кода. Конкретно из этого примера мы извлекаем значение "{substring}", 
# но тебе нужно найти пример, что бы он работал и с другими значениями. 
# В ответе напиши только один путь селекторов, по которому можно извлечь такое значение из html страницы.
# {found[0]}
# """

# print("_____________________________________")
# print("Посылаем запрос")
# print(prompt)

# # response = sendMessageToYandexGPT(prompt)

# # Нужно сделать аналог, на внутреннем DOM полученной страницы
# # И прописать работу с библиотекой cheerio






# Работает
# 2я версия, некорректно обрабатывает img

# def get_css_path(element):
#     """Построение CSS-селектора для данного элемента."""
#     path = []
#     while element and element.name:
#         selector = element.name

#         # Если у элемента есть ID — это уникально
#         if element.has_attr("id"):
#             selector = f"#{element['id']}"
#             path.append(selector)
#             break

#         # Если есть класс(ы)
#         elif element.has_attr("class"):
#             selector += "." + ".".join(element["class"])

#         # Проверяем порядок элемента среди сиблингов
#         siblings = element.find_previous_siblings(element.name)
#         if siblings:
#             selector += f":nth-of-type({len(siblings) + 1})"

#         path.append(selector)
#         element = element.parent

#     return " > ".join(reversed(path))


# def find_text_selector(html: str, text: str, exact: bool = False):
#     """Находит CSS-селектор элемента, содержащего заданный текст или значение в атрибутах."""
#     soup = BeautifulSoup(html, "html.parser")

#     # Проходим по всем элементам в документе
#     for el in soup.find_all(True):  # True — значит все теги
#         # Проверяем текст внутри элемента
#         if el.string and ((text == el.string.strip()) if exact else (text in el.string)):
#             return get_css_path(el)

#         # Проверяем все атрибуты
#         for attr_val in el.attrs.values():
#             if isinstance(attr_val, list):
#                 attr_val = " ".join(attr_val)
#             if isinstance(attr_val, str) and (text in attr_val if not exact else text == attr_val.strip()):
#                 return get_css_path(el)

#     return None





def get_css_path(element):
    """Построение CSS-селектора для данного элемента."""
    path = []
    while element and element.name:
        selector = element.name

        # Если у элемента есть ID — это уникально
        if element.has_attr("id"):
            selector = f"#{element['id']}"
            path.append(selector)
            break

        # Если есть класс(ы)
        elif element.has_attr("class"):
            selector += "." + ".".join(element["class"])

        # Проверяем порядок элемента среди сиблингов
        siblings = element.find_previous_siblings(element.name)
        if siblings:
            selector += f":nth-of-type({len(siblings) + 1})"

        path.append(selector)
        element = element.parent

    return " > ".join(reversed(path))


def find_text_selector(html: str, text: str, exact: bool = False):
    """
    Находит CSS-селектор элемента, содержащего заданный текст или значение в атрибутах.
    Если найдено в атрибуте (alt/title/value/placeholder и т.д.), возвращает путь с указанием атрибута: "селектор@@attr".
    """
    soup = BeautifulSoup(html, "html.parser")

    for el in soup.find_all(True):
        # Проверяем текст внутри элемента
        if el.string and ((text == el.string.strip()) if exact else (text in el.string)):
            return get_css_path(el)

        # Проверяем атрибуты
        for attr_name, attr_val in el.attrs.items():
            if isinstance(attr_val, list):
                attr_val = " ".join(attr_val)
            if isinstance(attr_val, str):
                match = (text == attr_val.strip()) if exact else (text in attr_val)
                if match:
                    # Возвращаем селектор + указание на атрибут
                    return get_css_path(el) + f"[{attr_name}]"

    return None







finded_element = substring_brand
print("")
print(f"🟦 Извлекли такой селектор для поля {finded_element}:")
# selector = find_text_selector(html, substring_name)
selector = find_text_selector(html, finded_element)
print(selector)

### Короче, это работает, но выводит мусорные css пути
### В целом, на этом пока что можно остановиться
### И чистить их уже позже (позже прописать, или позже в коде чистить)




# Проверяем селектор: Получаем элемент из html по нему:

# selector = "html > body > div.wrapper > img:nth-of-type(1)"
# selector = "a.catalog-element-brand img"

tree = html_lx.fromstring(html)
element = tree.cssselect(selector)[0]  # Возьмём первый найденный

# Выводим HTML этого элемента
print("")
print("🟢 Проверка селектора:")
print(html_lx.tostring(element, encoding="unicode", pretty_print=True))



print("")
print("🟡 Проверка значения селектора:")



#i-18-bitrix-catalog-element-catalog-default-1-qepX1RQfHh6Q > div.catalog-element-wrapper.intec-content.intec-content-visible > div.catalog-element-wrapper-2.intec-content-wrapper > div.catalog-element-information-wrap > div.catalog-element-information.intec-grid.intec-grid-nowrap.intec-grid-768-wrap.intec-grid-a-h-start.intec-grid-a-v-start.intec-grid-i-20:nth-of-type(3) > div.catalog-element-information-right.intec-grid-item.intec-grid-item-768-1:nth-of-type(2) > div.catalog-element-information-right-wrapper > div.catalog-element-information-part.intec-grid.intec-grid-wrap.intec-grid-a-v-center.intec-grid-i-10 > div.intec-grid-item-auto:nth-of-type(2) > a.catalog-element-brand.intec-ui-picture > img
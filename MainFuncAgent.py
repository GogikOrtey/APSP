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






# Находит и возвращает все фрагменты подстроки в html
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




















# Находит и возвращает css селектор элемента, по его содержанию
# def find_text_selector(html: str, text: str, exact: bool = False):
#     # Построение пути css селектора для данного элемента
#     def get_css_path(element):
#         path = []
#         while element and element.name:
#             selector = element.name

#             # Если у элемента есть ID — это уникально
#             if element.has_attr("id"):
#                 selector = f"#{element['id']}"
#                 path.append(selector)
#                 break

#             # Если есть класс(ы)
#             elif element.has_attr("class"):
#                 selector += "." + ".".join(element["class"])

#             # Проверяем порядок элемента среди сиблингов
#             siblings = element.find_previous_siblings(element.name)
#             if siblings:
#                 selector += f":nth-of-type({len(siblings) + 1})"

#             path.append(selector)
#             element = element.parent

#         return " > ".join(reversed(path))

#     soup = BeautifulSoup(html, "html.parser")

#     for el in soup.find_all(True):
#         # Проверяем текст внутри элемента
#         if el.string and ((text == el.string.strip()) if exact else (text in el.string)):
#             return get_css_path(el)

#         # Проверяем атрибуты
#         for attr_name, attr_val in el.attrs.items():
#             if isinstance(attr_val, list):
#                 attr_val = " ".join(attr_val)
#             if isinstance(attr_val, str):
#                 match = (text == attr_val.strip()) if exact else (text in attr_val)
#                 if match:
#                     # Возвращаем селектор + указание на атрибут
#                     return get_css_path(el) + f"[{attr_name}]"

#     return None

from bs4 import BeautifulSoup

# Находит и возвращает css селектор(ы) элемента(ов) по содержимому
def find_text_selector(html: str, text: str, exact: bool = False, return_all_selectors: bool = False):
    # Построение пути css селектора для данного элемента
    def get_css_path(element):
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

    soup = BeautifulSoup(html, "html.parser")
    selectors = []

    for el in soup.find_all(True):
        # Проверяем текст внутри элемента
        if el.string and ((text == el.string.strip()) if exact else (text in el.string)):
            selector = get_css_path(el)
            if return_all_selectors:
                selectors.append(selector)
            else:
                return selector

        # Проверяем атрибуты
        for attr_name, attr_val in el.attrs.items():
            if isinstance(attr_val, list):
                attr_val = " ".join(attr_val)
            if isinstance(attr_val, str):
                match = (text == attr_val.strip()) if exact else (text in attr_val)
                if match:
                    selector = get_css_path(el) + f"[{attr_name}]"
                    if return_all_selectors:
                        selectors.append(selector)
                    else:
                        return selector

    if return_all_selectors:
        return selectors if selectors else None

    return None


# Получает и возвращает значение элемента по селектору
def get_element_from_selector(html, selector):
    tree = html_lx.fromstring(html)
    search_elem = tree.cssselect(selector)
    if(len(search_elem) == 0): 
        print("🟡 По селектору элемент не найден")
        return ""
    element = search_elem[0]

    # Проверяем, есть ли в селекторе указание атрибута в []
    attr_match = re.search(r"\[([a-zA-Z0-9_-]+)\]", selector)

    if attr_match:
        attr_name = attr_match.group(1)
        result = element.get(attr_name)
    else:        
        result = html_lx.tostring(element, encoding="unicode", pretty_print=True)
    
    return result

# Основная функция: Получает css селектор, по текстовому соержанию элемента
def get_css_selector_from_text_value_element(html, finding_element):
    print("")
    print(f"🟦 Извлекли такой селектор для поля \"{finding_element}\":")
    all_selector = find_text_selector(html, finding_element, return_all_selectors=True)
    # TODO Нужно будет сделать цикл for, по всем извлечённым селекторам
    # в порядке возрастания их длины
    # Пока проверка не покажет верное совпадение
    selector = min(all_selector, key=len)
    print(selector)


    ### Тут надо написать функцию дистилляции css путей


    # Проверяем селектор: Получаем элемент из html по нему:
    print("")
    print("🟢 Проверка селектора:")
    resule_test_element = get_element_from_selector(html, selector)
    print(resule_test_element)

    return selector

### Запаковать извлечение одного селектора в функцию
# и проверить на другом поле, например name


# substring = "Makita"
substring_brand = data_input_table["links"]["simple"][0]["brand"]
substring_name = data_input_table["links"]["simple"][0]["name"]

selector_result = get_css_selector_from_text_value_element(html, substring_name)
print("")
print(f"selector_result = {selector_result}")








































# Старое:
#i-18-bitrix-catalog-element-catalog-default-1-qepX1RQfHh6Q > div.catalog-element-wrapper.intec-content.intec-content-visible > div.catalog-element-wrapper-2.intec-content-wrapper > div.catalog-element-information-wrap > div.catalog-element-information.intec-grid.intec-grid-nowrap.intec-grid-768-wrap.intec-grid-a-h-start.intec-grid-a-v-start.intec-grid-i-20:nth-of-type(3) > div.catalog-element-information-right.intec-grid-item.intec-grid-item-768-1:nth-of-type(2) > div.catalog-element-information-right-wrapper > div.catalog-element-information-part.intec-grid.intec-grid-wrap.intec-grid-a-v-center.intec-grid-i-10 > div.intec-grid-item-auto:nth-of-type(2) > a.catalog-element-brand.intec-ui-picture > img
# selector = "html > body > div.wrapper > img:nth-of-type(1)"
# selector = "a.catalog-element-brand img"
### Основной скрипт агента

# Вынесенные отдельно функции
from addedFunc import sendMessageToYandexGPT
from addedFunc import get_html
from addedFunc import find_contexts

# Библиотеки
from typing import Callable, Dict, List, Any, Iterable, Tuple
from collections import Counter, defaultdict
from addedFunc import ErrorHandler
from difflib import SequenceMatcher
from lxml import html as html_lx
from bs4 import BeautifulSoup
from pprint import pprint
import itertools
import requests
import json
import re





isPrint = False



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




# region Входные данные

# # Данные извлечённые из таблицы, например:
# data_input_table = {
#     "links": {
#         "simple": [
#             # {
#             #     "link": "https://vodomirural.ru/catalog/vanny_stalnye_i_aksessuary_k_nim/33951/",
#             #     "name": "Ванна сталь 1600х700х400мм antika белый в комплекте с ножками ВИЗ в Екатеринбурге",
#             #     "price": "10 320",
#             #     "brand": "Аntika",
#             #     "stock": "В наличии",
#             #     "imageLink": ""
#             # },
#             {
#                 "link": "https://vodomirural.ru/catalog/opora_klipsa/35508/",
#                 "name": "Опора ППРС D25 в Екатеринбурге",
#                 "price": "5",
#                 "brand": "",
#                 "stock": "В наличии",
#                 "imageLink": "https://vodomirural.ru/upload/resize_cache/webp/iblock/168/16809d1e998be5e9c79c5d78e3e2f659.webp"
#             },
#             {
#                 "link": "https://vodomirural.ru/catalog/zaglushka/35457/",
#                 "name": "Заглушка (D20) в Екатеринбурге",
#                 "price": "4",
#                 "brand": "MeerPlast",
#                 "stock": "В наличии",
#                 "imageLink": "https://vodomirural.ru/upload/resize_cache/webp/iblock/246/246a504d1f7b2f5b10645bb86c8060c3.webp"
#             },
#             {
#                 "link": "https://vodomirural.ru/catalog/krestovina/35188/",
#                 "name": "Крестовина 20 ППРС в Екатеринбурге",
#                 "price": "16",
#                 "brand": "MeerPlast",
#                 "stock": "В наличии",
#                 "imageLink": "https://vodomirural.ru/upload/resize_cache/webp/iblock/39f/39f1c40fccd66173cf21a1b847baa335.webp"
#             },
#             {
#                 "link": "https://vodomirural.ru/catalog/mufta_kombinirovannaya_amerikanka_razemnaya_vn_rez/32506/",
#                 "name": "Муфта комб. раз. ППРС (вн. рез.) 20-1/2 в Екатеринбурге",
#                 "price": "102",
#                 "brand": "MeerPlast",
#                 "stock": "В наличии",
#                 "imageLink": "https://vodomirural.ru/upload/resize_cache/webp/iblock/1b4/1b42d7577c23ed7541f61b721e4fa018.webp"
#             }
#         ]
#     },
#     "search_requests": []
# }



############################## article не нашёл !!!


# # Данные с сайта 2
# data_input_table = {
#     "links": {
#         "simple": [
#             {
#                 "link": "https://santehnica-vodoley.ru/catalog/vanny/vanny-akrilovye/vanna-aura-170-b530df76.html",
#                 "name": "Акриловая ванна Triton Аура 170x70 (КОПЛЕКТ ванна,экрас,каркас) TRITON",
#                 "price": "16 125",
#                 "article": "00017728",
#                 "brand": "TRITON",
#                 # "stock": "В наличии",
#                 "imageLink": "https://santehnica-vodoley.ru/a/vodolei1/files/userfiles/images/catalog/b530df7630d011ec812be0d55e0811bb_b530df7730d011ec812be0d55e0811bb.jpg"
#             },
#             {
#                 "link": "https://santehnica-vodoley.ru/catalog/vanny/vanny-akrilovye/vanna-standart-160h70-ekstra-akril-cd18e8d4.html",
#                 "name": "Акриловая ванна Triton Стандарт 160х70 Экстра TRITON",
#                 "price": "9 900 руб.",
#                 "article": "УТ000001951",
#                 "brand": "TRITON",
#                 "imageLink": "https://santehnica-vodoley.ru/a/vodolei1/files/userfiles/images/catalog/b530df7630d011ec812be0d55e0811bb_b530df7730d011ec812be0d55e0811bb.jpg"
#             },
#             {
#                 "link": "https://santehnica-vodoley.ru/catalog/vanny/vanny-akrilovye/vanna-standart-130-ekstra-akril-9767a71b.html",
#                 "name": "Акриловая ванна Triton Стандарт 130х70 Экстра TRITON",
#                 "price": "7 990 руб.",
#                 "article": "УТ000006868",
#                 "brand": "TRITON",
#                 "imageLink": "https://santehnica-vodoley.ru/a/vodolei1/files/userfiles/images/catalog/cd18e8d400d511e38427001a4d504e55_97912f653b7d11ea80e8e0d55e0811bb.jpg"
#             },
#             {
#                 "link": "https://santehnica-vodoley.ru/catalog/vanny/vanny-akrilovye/vanna-izabel-pravaya-1700x1000-mm-fb2cccfd.html",
#                 "name": "Акриловая ванна Triton Изабель 170х100 R TRITON",
#                 "price": "24 820 руб.",
#                 "article": "УТ000001271",
#                 "brand": "TRITON",
#                 "imageLink": "https://santehnica-vodoley.ru/a/vodolei1/files/userfiles/images/catalog/fb2cccfd42b211e2859e001a4d504e55_04a3a1a4eb5b11ee8148e0d55e0811bb.jpg"
#             },
#             {
#                 "link": "https://santehnica-vodoley.ru/catalog/kotelnoe-oborudovanie/komplektuyucshie-dlya-kotelnogo-oborudovaniya/prokladka-iz-ftoroplasta-34-MasterProf-58316128.html",
#                 "name": "Прокладка из фторопласта 3/4\" MasterProf MasterProf",
#                 "price": "15 руб.",
#                 "article": "00027670",
#                 "brand": "MasterProf",
#                 # Не в наличии
#                 "imageLink": "https://santehnica-vodoley.ru/a/vodolei1/files/userfiles/images/catalog/583161280d2a11ef814ae0d55e0811bb_5831613b0d2a11ef814ae0d55e0811bb.jpg"
#             }
#         ]
#     },
#     "search_requests": []
# }




# Данные с сайта 3
data_input_table = {
    "links": {
        "simple": [
            {
                "link": "https://keramix-ekb.ru/keramogranit/gracia-ceramica-rossiya/monocolor.html",
                "name": "Керамогранит Коллекция Monocolor производство Gracia Ceramica",
                "price": "1 970",
                "brand": "Gracia Ceramica",
                # "stock": "В наличии",
                "country": "Россия",
                "imageLink": "https://keramix-ekb.ru/img/icons/icon6310.jpg"
            }
        ]
    },
    "search_requests": []
}




# region Check html
# Проверяю, что html-страница доступна, и данные первого товара на ней есть
def check_avialible_html():
    # TODO: Потом добавить обработку, что бы он искал не полным сравнением подстроки названия товара при проверке, а частичным
    # Это когда напишу такую штуку для price

    first_item_link = data_input_table["links"]["simple"][0]["link"]
    # print(first_item_link)
    html = get_html(first_item_link)
    # print(html[:500])

    text_includes = data_input_table["links"]["simple"][0]["name"]
    if text_includes in html:
        # print("🟢 Подстрока найдена!")
        a = 1
    else:
        print("🟠 Подстрока не найдена.")
        raise ErrorHandler("При открытии страницы 1 товара, на ней не было обнаружено названия товара", "4-1")





def print_json(input_json):
    text = json.dumps(input_json, indent=4, ensure_ascii=False)
    text = text.replace('\\"', '"')
    print(text)




# Проверяю, что html-страница доступна, и данные первого товара на ней есть
check_avialible_html()







# # Находит и возвращает css селекторы элементов по содержимому
# def find_text_selector(html: str, text: str, exact: bool = False, return_all_selectors: bool = False):
#     def get_css_path(element):
#         path = []
#         while element and element.name and element.name != "[document]":
#             selector = element.name
#             if element.has_attr("id"):
#                 selector = f"#{element['id']}"
#                 path.append(selector)
#                 break
#             elif element.has_attr("class"):
#                 selector += "." + ".".join(element["class"])
#             siblings = element.find_previous_siblings(element.name)
#             if siblings:
#                 selector += f":nth-of-type({len(siblings) + 1})"
#             path.append(selector)
#             element = element.parent
#         return " > ".join(reversed(path))

#     def normalize_text(s):
#         return " ".join(s.split())

#     def similarity(a, b):
#         return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()

#     soup = BeautifulSoup(html, "html.parser")
#     selectors = []

#     # Этап 1. Прямой поиск (строгий / частичный)
#     for el in soup.find_all(True):
#         element_text = el.get_text(strip=True)
#         if element_text:
#             match = (text == element_text) if exact else (text in element_text)
#             if match:
#                 selector = get_css_path(el)
#                 if return_all_selectors:
#                     selectors.append(selector)
#                 else:
#                     return selector

#         # Проверяем атрибуты
#         for attr_name, attr_val in el.attrs.items():
#             if isinstance(attr_val, list):
#                 attr_val = " ".join(attr_val)
#             if isinstance(attr_val, str):
#                 match = (text == attr_val.strip()) if exact else (text in attr_val)
#                 if match:
#                     selector = get_css_path(el) + f"[{attr_name}]"
#                     if return_all_selectors:
#                         selectors.append(selector)
#                     else:
#                         return selector

#     # Этап 2. Нестрогий (fuzzy) поиск
#     if not selectors:
#         threshold = 0.7
#         for el in soup.find_all(True):
#             # Проверка текста элемента
#             element_text = el.get_text(strip=True)
#             if element_text:
#                 score = similarity(text, element_text)
#                 if score >= threshold:
#                     selector = get_css_path(el)
#                     if return_all_selectors:
#                         selectors.append(selector)
#                     else:
#                         return selector

#             # Проверка атрибутов
#             for attr_name, attr_val in el.attrs.items():
#                 if isinstance(attr_val, list):
#                     attr_val = " ".join(attr_val)
#                 if isinstance(attr_val, str):
#                     score = similarity(text, attr_val)
#                     if score >= threshold:
#                         selector = get_css_path(el) + f"[{attr_name}]"
#                         if return_all_selectors:
#                             selectors.append(selector)
#                         else:
#                             return selector

#     if return_all_selectors:
#         return selectors if selectors else None
#     return None


############################## article не нашёл !!!
# На данных со 2го сайта

################################################# Ещё раз задать вопрос ChatGPT, он остался в истории запросов

# region find_text_selector

# Находит и возвращает css селекторы элементов по содержимому
# Принимает один элемент, находит и возвращает набор селекторов, по которым этот элемент можно получить
# Если exact = True, то ...
def find_text_selector(html: str, text: str, exact: bool = False, return_all_selectors: bool = False):
    IGNORED_ATTRS = {"content", "data-original", "href", "data-src", "src", "data"}
    PRIORITY_ATTRS = ["name", "property", "itemprop", "id"]

    def get_css_path(element):
        path = []
        while element and element.name and element.name != "[document]":
            selector = element.name

            # Если есть id — это всегда уникально
            if element.has_attr("id"):
                selector = f"#{element['id']}"
                path.append(selector)
                break

            # Добавляем классы, если есть
            if element.has_attr("class"):
                selector += "." + ".".join(element["class"])

            # Если элемент имеет уникальные/значимые атрибуты — пропускаем nth-of-type
            has_significant_attr = any(
                attr in PRIORITY_ATTRS or attr not in IGNORED_ATTRS
                for attr in element.attrs.keys()
            )

            if not has_significant_attr:
                siblings = element.find_previous_siblings(element.name)
                if siblings:
                    selector += f":nth-of-type({len(siblings) + 1})"

            path.append(selector)
            element = element.parent

        return " > ".join(reversed(path))

    def normalize_text(s):
        return " ".join(s.split())

    def similarity(a, b):
        return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()

    soup = BeautifulSoup(html, "html.parser")
    selectors = []

    def make_selector(el, base_selector, attr_name):
        parts = [base_selector]

        if attr_name in IGNORED_ATTRS:
            # если нашли игнорируемый атрибут, ищем более информативный
            for alt_attr in PRIORITY_ATTRS:
                if el.has_attr(alt_attr):
                    val = el.get(alt_attr)
                    if isinstance(val, list):
                        val = " ".join(val)
                    if isinstance(val, str):
                        parts.append(f'[{alt_attr}="{val.strip()}"]')
                    break
            # добавляем сам matched-атрибут без значения
            parts.append(f'[{attr_name}]')
        else:
            val = el.get(attr_name)
            if isinstance(val, list):
                val = " ".join(val)
            if isinstance(val, str):
                parts.append(f'[{attr_name}="{val.strip()}"]')
            else:
                parts.append(f'[{attr_name}]')

        return "".join(parts)

    # --- Этап 1. Прямой поиск ---
    for el in soup.find_all(True):
        element_text = el.get_text(strip=True)
        if element_text:
            match = (text == element_text) if exact else (text in element_text)
            if match:
                selector = get_css_path(el)
                if return_all_selectors:
                    selectors.append(selector)
                else:
                    return selector

        for attr_name, attr_val in el.attrs.items():
            if isinstance(attr_val, list):
                attr_val = " ".join(attr_val)
            if isinstance(attr_val, str):
                match = (text == attr_val.strip()) if exact else (text in attr_val)
                if match:
                    base_selector = get_css_path(el)
                    selector = make_selector(el, base_selector, attr_name)
                    if return_all_selectors:
                        selectors.append(selector)
                    else:
                        return selector

    # --- Этап 2. Fuzzy поиск ---
    if not selectors:
        threshold = 0.7
        for el in soup.find_all(True):
            element_text = el.get_text(strip=True)
            if element_text:
                score = similarity(text, element_text)
                if score >= threshold:
                    selector = get_css_path(el)
                    if return_all_selectors:
                        selectors.append(selector)
                    else:
                        return selector

            for attr_name, attr_val in el.attrs.items():
                if isinstance(attr_val, list):
                    attr_val = " ".join(attr_val)
                if isinstance(attr_val, str):
                    score = similarity(text, attr_val)
                    if score >= threshold:
                        base_selector = get_css_path(el)
                        selector = make_selector(el, base_selector, attr_name)
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
    if len(search_elem) == 0: 
        # print("🟡 По селектору элемент не найден")
        return ""
    element = search_elem[0]

    # Проверяем, есть ли в селекторе указание атрибута в []
    attr_match = re.search(r"\[([a-zA-Z0-9_-]+)\]", selector)

    if attr_match:
        attr_name = attr_match.group(1)
        result = element.get(attr_name)
    else:
        # Возвращаем только текст внутри элемента
        result = element.text_content().strip()
    
    return result



# region Дистилляция пути
# Дистилляция пути css селектора
# Принимает полный и точный селектор, очищает, и возвращает сокращённый
# удаляя все ненужные звенья
def simplify_selector_keep_value(html: str, selector: str, get_element_from_selector):
    """
    Пытается удалить ненужные звенья в селекторе (слева направо).
    Возвращает упрощённый селектор, который гарантированно возвращает
    такое же значение, как исходный селектор, по вызову get_element_from_selector.
    Параметры:
      - html: текст html страницы
      - selector: исходный строгий селектор (через '>')
      - get_element_from_selector: функция (html, selector) -> value (строка)
    """

    def _split_selector_preserving_brackets(selector: str):
        """
        Разбивает селектор по '>' но игнорирует '>' внутри [], (), '' и "".
        Возвращает список звеньев (строк) без лишних пробелов по краям.
        """
        parts = []
        buf = []
        bracket_sq = 0  # []
        bracket_par = 0 # ()
        in_single = False
        in_double = False   

        i = 0
        while i < len(selector):
            ch = selector[i]    

            # переключение состояния строк
            if ch == "'" and not in_double:
                in_single = not in_single
                buf.append(ch)
                i += 1
                continue
            if ch == '"' and not in_single:
                in_double = not in_double
                buf.append(ch)
                i += 1
                continue    

            if not in_single and not in_double:
                if ch == '[':
                    bracket_sq += 1
                    buf.append(ch)
                    i += 1
                    continue
                if ch == ']':
                    if bracket_sq > 0:
                        bracket_sq -= 1
                    buf.append(ch)
                    i += 1
                    continue
                if ch == '(':
                    bracket_par += 1
                    buf.append(ch)
                    i += 1
                    continue
                if ch == ')':
                    if bracket_par > 0:
                        bracket_par -= 1
                    buf.append(ch)
                    i += 1
                    continue    

            # разделитель '>' только если мы не внутри скобок/строк
            if ch == '>' and not in_single and not in_double and bracket_sq == 0 and bracket_par == 0:
                part = ''.join(buf).strip()
                if part != '':
                    parts.append(part)
                buf = []
                # пропускаем возможные пробелы вокруг >
                i += 1
                # skip following spaces
                while i < len(selector) and selector[i].isspace():
                    i += 1
                continue    

            buf.append(ch)
            i += 1  

        last = ''.join(buf).strip()
        if last != '':
            parts.append(last)
        return parts

    # начальная проверка: получаем исходное значение
    try:
        original_value = get_element_from_selector(html, selector)
    except Exception:
        # если исходный селектор уже валидный, но функция кидает — лучше вернуть исходный
        return selector

    # разбиваем селектор корректно
    parts = _split_selector_preserving_brackets(selector)

    # если один сегмент — возвратим как есть
    if len(parts) <= 1:
        return selector.strip()

    i = 0
    # проходим слева направо. Для каждого индекса пробуем удалить parts[i].
    # Если после удаления результат совпадает с original_value — применяем удаление и
    # остаёмся на том же i (т.к. дальше сдвинулись элементы).
    # Иначе переходим к следующему i.
    while i < len(parts) - 1:
        # нельзя удалить все звенья — должен остаться хотя бы одно
        if len(parts) == 1:
            break

        candidate_parts = parts[:i] + parts[i+1:]
        candidate_selector = " > ".join(candidate_parts)

        try:
            candidate_value = get_element_from_selector(html, candidate_selector)
        except Exception:
            # если селектор стал невалидным или привёл к исключению — считаем, что удаление ломает цепочку
            candidate_value = None

        # сравнение: строгая эквивалентность
        if candidate_value == original_value:
            # удаление безопасно — применяем
            parts = candidate_parts
            # Не инкрементируем i: нужно попытаться удалить новое звено на этой же позиции
            # (поведение: удаляем как можно больше подряд)
            # но если i теперь == len(parts) (удалили последний) - цикл завершится naturally
            continue
        else:
            # удаление ломает — оставляем звено и идём дальше
            i += 1

    # собрать итоговый селектор
    simplified = " > ".join(parts)
    return simplified
    # Имеется в виду, что даже если селектор возвращает несколько элементов, мы берём только первый




# region get_css_selector_from_text_value_element

# Основная функция: Получает css селектор, по текстовому содержанию элемента
# Эта функция get_css_selector_from_text_value_element получает на вход один элемент
# Отправляет его в find_text_selector - получает набор css селекторов к этому элементу
# Проверяет, что каждый селектор действительно верный, и сортирует их по точности совпадения
# также сортирует по длине, чем короче тем лучше
# Затем, найденный лучший селектор - дистиллирует
def get_css_selector_from_text_value_element(html, finding_element, is_price = False, is_exact = False):
    print("")
    if isPrint: print(f"🟦 Извлекли такие селекторы для поля \"{finding_element}\":")
    if(is_price):
        # Для извлечения price и oldPrice - отдельный обработчик
        all_selectors = handle_selector_price(html, finding_element)
    elif finding_element.strip().lower() == "в наличии" or is_exact:
        all_selectors = find_text_selector(html, finding_element, exact=True, return_all_selectors=True)
    else:
        all_selectors = find_text_selector(html, finding_element, return_all_selectors=True)

    if not all_selectors:
        if isPrint: print("🟡 Не найдено ни одного подходящего селектора")
        return ""

    print(f"Найдено {len(all_selectors)} возможных селекторов")

    valid_selectors = []

    # Проверяем каждый селектор
    for selector in all_selectors:
        if isPrint: print("")
        if isPrint: print(f"🟢 Проверка селектора: {selector}")
        result_text = get_element_from_selector(html, selector)

        if result_text == "":
            if isPrint: print("❌ Элемент по селектору не найден")
            continue

        # Проверяем наличие подстроки — строгое совпадение по содержанию
        if finding_element.strip() in result_text.strip():
            match_score = 1.0
            if isPrint: print(f"✅ Строгое совпадение: [{result_text}]")
        else:
            # Если нет прямого вхождения — оцениваем схожесть
            match_score = compute_match_score(result_text, finding_element)
            if isPrint: print(f"⚪ Совпадение {match_score*100:.1f}%: [{result_text}]")

        valid_selectors.append({
            "selector": selector,
            "result": result_text,
            "score": match_score
        })

    # Если ни один не подошёл
    if not valid_selectors:
        if isPrint: print("🔴 Не найдено корректных селекторов")
        return ""

    # Сортируем:
    # 1️⃣ по совпадению (по убыванию)
    # 2️⃣ при равных — по длине селектора (по возрастанию)
    valid_selectors.sort(key=lambda x: (-x["score"], len(x["selector"])))

    best = valid_selectors[0]
    if isPrint: print("")
    if isPrint: print(f"🏆 Лучший селектор: {best['selector']} (совпадение {best['score']*100:.1f}%)")

    # Дистилляция пути
    # result_distill_selector = distill_selector(html, best["selector"], get_element_from_selector, finding_element)
    result_distill_selector = simplify_selector_keep_value(html, best["selector"], get_element_from_selector)
    return result_distill_selector


# Вспомогательная функция для оценки схожести
def compute_match_score(found_text, target_text):
    """Оценка схожести строк по количеству совпадающих символов"""
    found_text = found_text.strip().lower()
    target_text = target_text.strip().lower()

    if not found_text or not target_text:
        return 0.0

    # Длина совпадающих символов (по порядку)
    common = sum(1 for a, b in zip(found_text, target_text) if a == b)
    score = common / max(len(target_text), len(found_text))
    return score







# region handle_selector_price

# TODO Потом надо будет слить всё в один метод, а не выделять отдельно извлечение цен (чисел)

# Извлекает селекторы цены
# Перед этим очистив html от мусорных спецсимволов
def handle_selector_price(html, finding_element):
    # 1. Очистка HTML
    def clean_html(text: str) -> str:
        text = text.replace("&nbsp;", " ").replace("\xa0", " ")
        text = re.sub(r"[\u200b\u200e\u200f\r\n\t]+", " ", text)
        return text.strip()

    # 2. Нормализация чисел/цен
    def normalize_price(s: str) -> str:
        if not s:
            return ""
        s = s.strip().lower()
        s = re.sub(r"[^\d,\.]", "", s)
        s = re.sub(r"[^\d]", "", s)
        return s

    # 3. Функция построения CSS-пути для элемента
    def get_css_path(element):
        path = []
        while element is not None and isinstance(element.tag, str):
            selector = element.tag

            # Если есть ID — уникальный селектор
            if 'id' in element.attrib:
                selector = f"#{element.attrib['id']}"
                path.append(selector)
                break

            # Если есть классы
            if 'class' in element.attrib:
                classes = element.attrib['class'].split()
                selector += '.' + '.'.join(classes)

            # nth-of-type среди сиблингов
            parent = element.getparent()
            if parent is not None:
                same_tag_siblings = [sib for sib in parent if isinstance(sib.tag, str) and sib.tag == element.tag]
                if len(same_tag_siblings) > 1:
                    index = same_tag_siblings.index(element) + 1
                    selector += f":nth-of-type({index})"

            path.append(selector)
            element = parent

        return " > ".join(reversed(path))

    # 4. Основная функция поиска селекторов по цене
    def find_price_selectors(html: str, finding_element: str, return_all_selectors: bool = False):
        html = clean_html(html)
        target_norm = normalize_price(finding_element)

        tree = html_lx.fromstring(html)
        selectors = []

        for elem in tree.iter():
            # Пропускаем комментарии, доктайпы
            if not isinstance(elem.tag, str):
                continue

            # Проверяем текст
            text = elem.text_content().strip() if elem.text_content() else ""
            if text and normalize_price(text) == target_norm:
                selector = get_css_path(elem)
                if return_all_selectors:
                    selectors.append(selector)
                else:
                    return selector

            # Проверяем все атрибуты
            for attr_name, attr_val in elem.attrib.items():
                if isinstance(attr_val, str) and normalize_price(attr_val) == target_norm:
                    selector = f"{get_css_path(elem)}[{attr_name}]"
                    if return_all_selectors:
                        selectors.append(selector)
                    else:
                        return selector

        if return_all_selectors:
            return selectors if selectors else None

        return None
    
    # Вернуть все селекторы
    all_selectors = find_price_selectors(html, finding_element, return_all_selectors=True)
    # print(all_selectors)

    # # Вернуть первый найденный селектор
    # first_selector = find_price_selectors(html, finding_element)
    # print(first_selector)

    return all_selectors





content_html = {
    "simple": [
        # {
        #     "link": "",
        #     "html_content": ""  
        # },    
    ]
}


# region fill_selectors_for_items

# Обрабатываем все элементы из полученного массива - находим для каждого селектор
def fill_selectors_for_items(items, get_css_selector_from_text_value_element):
    print(f"Обработаем {len(data_input_table['links']['simple'])} страниц")
    for item in items:
        # Если нет поля _selectors — создаём
        selectors = {}
        html = get_html(item["link"])

        # Храню html в отдельном массиве
        new_item = {
            "link": item["link"],
            "html_content": html
        }
        content_html["simple"].append(new_item)

        # Проходим по всем ключам, кроме служебных и ссылки
        for key, value in item.items():
            if key.startswith("_") or key == "link":
                continue  # пропускаем служебные поля
            
            selector = ""
            # Обрабатываем только строки
            if isinstance(value, str) and value.strip():
                try:
                    is_price = key in ("price", "oldPrice")

                    # Две попытки: сначала exact=True, потом exact=False
                    for attempt, is_exact in enumerate([True, False], start=1):
                        selector = get_css_selector_from_text_value_element(
                            html, value, is_price=is_price, is_exact=is_exact
                        )
                        if selector:
                            print(f"🟩 Найден селектор для поля {key}")
                            selectors[key] = selector
                            break  # если нашли — выходим из цикла
                        elif attempt == 1:
                            print(f"🟨 Не нашли при exact=True, пробуем с exact=False...")

                    if not selector:
                        print(f"🟧 Не удалось найти селектор для поля {key} даже при exact=False")

                except Exception as e:
                    print(f"🟥 Ошибка при поиске селектора для {key}: {e}")
            else:
                print(f"⬜ Пропускаем поле {key}: Не строка или пустое значение")

        print("_______________________")


        # Записываем обратно
        item["_selectors"] = selectors



# region select_best_selectors

# Перебирает все селекторы которые мы собрали со всех страничек, 
# и выбирает наилучший, для каждого поля
def select_best_selectors(input_data, content_html):
    # TODO Не протестировал на селекторах, которые будут идти через запятую
    print_fail_report = True

    def normalize_text(s: str) -> str:
        if s is None:
            return ""
        s = re.sub(r"\s+", " ", s).strip()
        return s.lower()

    def normalize_price(s: str) -> str:
        if s is None:
            return ""
        # извлечь цифры и разделители
        digits = re.findall(r"[\d]+", s.replace(",", ""))
        return "".join(digits)

    def extract_using_selector(tree: html_lx.HtmlElement, selector: str) -> str:
        """
        Пытается выполнить CSS селектор на дереве lxml и вернуть строковое значение.
        Поддерживает селекторы, которые указывают атрибут в конце вроде "[content]" или "[class]".
        Если несколько элементов — возвращает первый непустой результат.
        """
        selector = selector.strip()
        # попытка выделить атрибут в квадратных скобках в конце
        attr_match = re.search(r"\[([a-zA-Z0-9_\-:]+)\]\s*$", selector)
        attr = None
        if attr_match:
            attr = attr_match.group(1)
            # уберём этот кусок для передачи cssselect, если он стоял в конце как самостоятельный фрагмент
            # (но учти: селектор может легитимно содержать [..] внутри — мы учитываем только последний)
            # попробуем применить целиком сначала (на случай, если это часть сложного селектора)
            try:
                elems = tree.cssselect(selector)
            except Exception:
                # попробуем удалить последний [attr]
                selector_no_attr = selector[:attr_match.start()].rstrip()
                try:
                    elems = tree.cssselect(selector_no_attr)
                except Exception:
                    elems = []
        else:
            try:
                elems = tree.cssselect(selector)
            except Exception:
                elems = []

        for el in elems:
            # если указали attr и элемент имеет его — возвращаем
            if attr:
                val = el.get(attr)
                if val:
                    return val.strip()
            # если элемент — meta or input, попробуем стандартные атрибуты
            if el.tag in ("meta", "link", "img", "input"):
                # common attrs
                for a in ("content", "value", "alt", "src", "href", "data-src"):
                    v = el.get(a)
                    if v:
                        return v.strip()
            # иначе текстовое содержимое
            text = el.text_content()
            if text and text.strip():
                return text.strip()
        return ""

    def score_selector(selector: str, count: int) -> float:
        # чем чаще встречается и короче — тем лучше
        return count / (1 + len(selector))

    def resolve_selectors_across_examples(
            examples: List[Dict[str, Any]],
            fields: Iterable[str] = None,
            html_fetcher: Callable[[str], str] = None,
            max_combination_size: int = None,
            verbose: bool = True,
        ) -> Dict[str, Any]:

        # Если fields не передан — определяем автоматически из примеров
        if not fields:
            if not examples:
                raise ValueError("Список examples пуст — невозможно определить поля автоматически.")
            fields = [key for key in examples[0].keys() if key != "link" and not key.startswith("_")]

        if verbose:
            print(f"Используемые поля: {fields}")
        """
        examples: список примеров, каждый пример - dict с keys: link, поля и _selectors dict
        возвращает: {
            "result_selectors": {field: [selector(s) chosen as list])},
            "report": {...}
        }
        """
        # 1) Собираем селекторы по полям
        selectors_by_field = defaultdict(list)
        for ex in examples:
            sdict = ex.get("_selectors", {})
            for f in fields:
                sel = sdict.get(f)
                if sel:
                    selectors_by_field[f].append(sel.strip())

        # уникализируем и считаем частоты
        counters = {f: Counter(selectors_by_field[f]) for f in fields}
        # сортировка кандидатов: по частоте desc, затем по длине asc
        candidates = {}
        for f, counter in counters.items():
            items = list(counter.items())
            items.sort(key=lambda t: (-t[1], len(t[0])))
            candidates[f] = [it[0] for it in items]

        if verbose:
            print("Кандидаты по полям (в порядке приоритета):")
            for f in fields:
                print(f" - {f}: {len(candidates[f])} селекторов -> {candidates[f]}")

        # 2) Подготовка html деревьев
        trees = []
        for ex in examples:
            url = ex["link"]
            html_text = html_fetcher(url)
            tree = html_lx.fromstring(html_text)
            trees.append((url, tree, ex))

        # 3) Проверяльщик: функция, которая проверяет набор селекторов (комбинацию) для одного поля
        def check_selector_set_for_field(field: str, sel_set: Tuple[str, ...]) -> bool:
            fails = 0
            total = len(trees)

            for url, tree, ex in trees:
                expected = ex.get(field, "")
                extracted_any = ""
                for s in sel_set:
                    got = extract_using_selector(tree, s)
                    if got:
                        extracted_any = got
                        break
                    
                if field == "price":
                    match = normalize_price(expected) == normalize_price(extracted_any)
                else:
                    match = normalize_text(expected) == normalize_text(extracted_any)

                if not match:
                    fails += 1
                    if verbose:
                        if print_fail_report: print(
                            f"  [FAIL] {field} on {url}: "
                            f"expected '{str(expected)[:70]}' "
                            f"got '{str(extracted_any)[:70]}' "
                            f"using {str(sel_set)[:70]}"
                        )

            #######################################
            # Нужно проставить 30%
            # И не проверять пустые
            # допускаем 1 несовпадение (или, например, ≤30% страниц)
            if fails <= 1 or fails / total <= 0.4:
                if verbose:
                    print(f"  [OK~] field {field} works with selectors {sel_set} (fails {fails}/{total})")
                return True

            return False

        result_selectors = {}
        report = {"tried": {}}

        # лимит на размер комбинаций
        n_examples = len(examples)
        if max_combination_size is None:
            max_combination_size = n_examples - 1  # если равен n_examples => ошибка по условию

        for field in fields:
            cand_list = candidates.get(field, [])
            report["tried"][field] = {"singles": [], "combinations": []}

            # сначала пробуем одиночные селекторы в порядке приоритета
            found = False
            for s in cand_list:
                report["tried"][field]["singles"].append(s)
                if check_selector_set_for_field(field, (s,)):
                    result_selectors[field] = [s]
                    found = True
                    break
            if found:
                continue

            # если одиночные не прошли — пробуем комбинации размера 2..max_combination_size
            # Перебираем комбинации из кандидатов (если кандидатов мало, то возможны все комбинации)
            for size in range(2, max_combination_size + 1):
                if size > len(cand_list):
                    break
                if verbose:
                    print(f"Пробуем комбинации size={size} для поля {field} (всего {len(cand_list)} кандидатов)")
                ok = False
                # ограничим число комбинаций, чтобы не взорвать время: если кандидатов много — используем лучшую часть
                max_cands_for_comb = 12
                use_candidates = cand_list[:max_cands_for_comb] if len(cand_list) > max_cands_for_comb else cand_list
                for combo in itertools.combinations(use_candidates, size):
                    report["tried"][field]["combinations"].append(combo)
                    if check_selector_set_for_field(field, combo):
                        result_selectors[field] = list(combo)
                        ok = True
                        break
                if ok:
                    found = True
                    break

            if not found:
                # если минимальный возмож размер равен числу примеров -> по твоей логике это ошибка
                if max_combination_size >= n_examples:
                    raise RuntimeError(f"Для поля '{field}' не найден валидный набор селекторов; "
                                       f"минимальный размер комбинации достиг {n_examples} — селекторы вероятно неверные.")
                else:
                    # оставляем пустой и отчётим
                    result_selectors[field] = []
                    if verbose:
                        print(f"[WARN] Для поля {field} не найден селектор(ы).")

        return {"result_selectors": result_selectors, "report": report}

    def make_html_fetcher_from_cache(content_html):
        """
        Возвращает функцию html_fetcher(link),
        которая достаёт html_content из заранее сохранённого словаря content_html
        """
        html_map = {}
        for group in content_html.values():
            for item in group:
                link = item.get("link", "").strip()
                html_text = item.get("html_content", "")
                if link and html_text:
                    html_map[link] = html_text

        def fetcher(url):
            if url in html_map:
                return html_map[url]
            raise ValueError(f"HTML для {url} не найден в content_html")

        return fetcher

    # создаём html_fetcher на основе кеша, из сохранённых html страничек
    html_fetcher = make_html_fetcher_from_cache(content_html)

    # вызываем основной алгоритм
    result = resolve_selectors_across_examples(
        input_data,
        html_fetcher=html_fetcher,
        verbose=True
    )

    return result





## Тест одного селектора с одной страницы

# region Тест 1 элемента

isPrint = True

elem_number = 0
html = get_html( data_input_table["links"]["simple"][elem_number]["link"])
# print(html[:500])

# substring_brand = data_input_table["links"]["simple"][elem_number]["brand"]
# substring_name = data_input_table["links"]["simple"][elem_number]["name"]
substring_price = data_input_table["links"]["simple"][elem_number]["price"]
# substring_stock = data_input_table["links"]["simple"][elem_number]["stock"]
# substring_imageLink = data_input_table["links"]["simple"][elem_number]["imageLink"]

# selector_result = get_css_selector_from_text_value_element(html, substring_name)
# selector_result = get_css_selector_from_text_value_element(html, substring_brand, is_exact = True)
# selector_result = get_css_selector_from_text_value_element(html, substring_stock)
selector_result = get_css_selector_from_text_value_element(html, substring_price, is_price = True)
# selector_result = get_css_selector_from_text_value_element(html, substring_imageLink)
print("")
print(f"🟩 selector_result = {selector_result}")


# # Получаем куски по подстроке
# result = find_contexts(html, substring_name)
# print(result)
















# region Обр всех селекторов


# fill_selectors_for_items(
#     data_input_table["links"]["simple"],
#     get_css_selector_from_text_value_element
# )

# # print(json.dumps(data_input_table["links"]["simple"], indent=4, ensure_ascii=False))
# print_json(data_input_table["links"]["simple"])
# # print(json.dumps(content_html, indent=4, ensure_ascii=False))





# # #  Сохраняем эти 2 json локально (по большей части для теста)

# # import os

# # # Создаём папку "cache", если её нет
# # os.makedirs("cache", exist_ok=True)

# # # --- Сохранение в JSON ---
# # with open("cache/data_input_table.json", "w", encoding="utf-8") as f:
# #     json.dump(data_input_table, f, ensure_ascii=False, indent=4)

# # with open("cache/content_html.json", "w", encoding="utf-8") as f:
# #     json.dump(content_html, f, ensure_ascii=False, indent=4)

# # print("✅ Файлы сохранены")



# # ### Загрузка файлов обратно

# # with open("cache/data_input_table.json", "r", encoding="utf-8") as f:
# #     data_input_table = json.load(f)

# # with open("cache/content_html.json", "r", encoding="utf-8") as f:
# #     content_html = json.load(f)

# # print("✅ Файлы загружены обратно")
# # # print("data_input_table:", data_input_table)
# # # print("content_html:", content_html)


# # print(json.dumps(data_input_table["links"]["simple"], indent=4, ensure_ascii=False))
# # # print(json.dumps(content_html, indent=4, ensure_ascii=False))







# ### На данный момент это конечная точка программы

# result_select_best_selectors = select_best_selectors(data_input_table["links"]["simple"], content_html)

# print("✅ Итоговые селекторы:")
# print_json(result_select_best_selectors["result_selectors"])




















































"""

После этого:

Протестировать на разных других сайтах

Подумать про то, как лучше собирать селектор InStock
    Придумал, что можно хранить триггерную фразу для InStock и OutOfStock
Также с oldPrice
    Единственное что приходит в голову - искать напрямую селекторы
    и если не заводится, то слать запрос ChatGPT

И далее нужно будет выписать вставку кода в шаблон
и генерацию финального кода parseCard


Позже:
Дальше можно будет навешивать логику генерации кода более сложной обработки
И после этого - отдельный модуль по извлечению и парсингу JSON
    т.е. смотреть и искать json-фрагменты на странице, если найдены - то пытаться
    найти в них искомые элементы
    И потом можно будет прикрутить поиск запросов на json вне главной html страницы товара
    (открывать во внешнем браузере, и смотреть)

    




Далее - начинаю писать 2ю функцию, по генерации parsePage

Можно собрать данные с главной страницы - извлечь только текст, обрезать его немного,
и загрузить в ChatGPT, что бы он сгенерировал 10 запросов для него
Но тут я хз как нам искать строку поиска, вводить туда текст поиска, и выполнять поиск

Можно как и планировал:
1. Брать url со 2й страницы поиска
2. И где было бы указано количество страниц для этого запроса
3. Извлекать ссылки на товары
И в целом всё. Посмотреть по шаблону, какие фрагменты кода нужны

TODO Сложная обработка - потоковая загрузка страниц, без явной пагинации








Нужно будет добавить извлечение полей из excel файла
Добавить бота в Тг
И крутой визуал запуска

"""




"""

Глобальный план:

Дописываю логику InStock и OldPrice
Написать генерацию шаблона кода парсера (в отдельный файл)
Тестирую и отлаживаю на других сайтах (5-10)
Пишу parsePage
Добавляю его логику в генерацию шаблона
Написать извлечение полей и данных из Excel входного файла
Написать инструкцию по заполнению такого Excel файла

Пишу обработчик JSON из html - поиск путей там
Выписываю запросы с прокси и подбор mode и engine
Тестирую добавление кастомной логики к извлечению данных
Выписываю открытие браузера, и нахождение json запросов

Далее тестирую на существующих парсерах
и на больших, типо WB 
И можно будет презентовать проект директору


"""
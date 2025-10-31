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
from urllib.parse import urlparse
from lxml import html as html_lx
from bs4 import BeautifulSoup
from pprint import pprint
import itertools
import requests
import json
import re

isPrint = False


# region Входные данные

# # Пример данных
# data_input_table = {
#     "host": "",
#     "links": {
#         "simple": [
#             {
#                 "link": "",
#                 "name": "",
#                 "price": "",
#                 "oldPrice": "",
#                 "article": "",
#                 "brand": "",
#                 "InStock_trigger": "",
#                 "OutOfStock_trigger": "",
#                 "imageLink": ""
#             }
#         ]
#     },
#     "search_requests": []
# }

# # Данные извлечённые из таблицы, например:
# data_input_table = {
#     "host": "",
#     "links": {
#         "simple": [
#             {
#                 "link": "https://vodomirural.ru/catalog/vanny_stalnye_i_aksessuary_k_nim/33951/",
#                 "name": "Ванна сталь 1600х700х400мм antika белый в комплекте с ножками ВИЗ в Екатеринбурге",
#                 "price": "10 320",
#                 "brand": "Аntika",
#                 "stock": "В наличии",
#                 "imageLink": ""
#             },
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



# # Данные с сайта 2
# # Здесь битые значения для поля imageLink на сайте
# data_input_table = {
#     "host": "",
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
#                 # # "OutOfStock_trigger": "",
#                 "imageLink": "https://santehnica-vodoley.ru/a/vodolei1/files/userfiles/images/catalog/583161280d2a11ef814ae0d55e0811bb_5831613b0d2a11ef814ae0d55e0811bb.jpg"
#             }
#         ]
#     },
#     "search_requests": []
# }




# # Данные с сайта 3
# data_input_table = {
#     "host": "",
#     "links": {
#         "simple": [
#             {
#                 "link": "https://keramix-ekb.ru/keramogranit/gracia-ceramica-rossiya/monocolor.html",
#                 "name": "Керамогранит Коллекция Monocolor производство Gracia Ceramica",
#                 "price": "1 970",
#                 "brand": "Gracia Ceramica",
#                 # "stock": "В наличии",
#                 "country": "Россия",
#                 "imageLink": "https://keramix-ekb.ru/img/icons/icon6310.jpg"
#             }
#         ]
#     },
#     "search_requests": []
# }



# # Данные с сайта 4
# data_input_table = {
#     "host": "",
#     "links": {
#         "simple": [
#             {
#                 "link": "https://kotel-nasos.ru/nastennyy-gazovyy-kotel-28-kvt-baxi-duo-tec-compact-28-ga/",
#                 "name": "Настенный конденсационный газовый котел 28 кВт Baxi DUO-TEC COMPACT 28",
#                 "price": "99 800 ₽",
#                 "oldPrice": "109 780 ₽",
#                 "article": "13455",
#                 "brand": "Baxi",
#                 "OutOfStock_trigger": "Предзаказ",
#                 "imageLink": "https://kotel-nasos.ru/wa-data/public/shop/products/18/99/29918/images/143135/143135.970.png"
#             },
#             {
#                 "link": "https://kotel-nasos.ru/napolnyy-gazovyy-kotel-60-kvt-baxi-slim-1-620in-9e/",
#                 "name": "Напольный газовый котел 60 кВт Baxi SLIM 1.620 iN 9E",
#                 "price": "195 000 ₽",
#                 "oldPrice": "238 150 ₽",
#                 "article": "38354",
#                 "brand": "Baxi",
#                 "InStock_trigger": "В наличии",
#                 "imageLink": "https://kotel-nasos.ru/wa-data/public/shop/products/17/01/30117/images/53793/53793.970.jpg"
#             }
#         ]
#     },
#     "search_requests": []
# }



# # Данные с сайта 5
# data_input_table = {
#     "host": "",
#     "links": {
#         "simple": [
#             {
#                 "link": "https://stroytorg812.ru/catalog/vanny/vanna_akrilovaya_1_70kh0_70_ultra_170/",
#                 "name": "Ванна акриловая 170х70 Ультра-170 # ТРИТОН",
#                 "price": "8 390 руб.",
#                 "article": "U4031689", 
#                 "brand": "ТРИТОН",
#                 "InStock_trigger": "есть на складе",
#                 "imageLink": "https://stroytorg812.ru/upload/iblock/db8/4db0f322_ffe9_11e6_94b1_002590746688_bed22781_05a3_11e7_94b1_002590746688.jpeg"
#             },
#             {
#                 "link": "https://stroytorg812.ru/catalog/mozaika/32_7kh32_7_mozaika_aqua_100_na_bumage/",
#                 "name": "32,7х32,7 Мозаика Aqua 100 (на бумаге) 20*20*4 Bonaparte",
#                 "price": "1 860,10",
#                 "oldPrice": "1 958",
#                 "article": "B2508830", 
#                 "brand": "Bonaparte",
#                 "InStock_trigger": "есть на складе",
#                 "imageLink": "https://stroytorg812.ru/upload/iblock/672/fe473651_57f3_11e3_a425_00148557b27c_f22d79df_bddb_11e3_beaf_a65927533166.jpeg"
#             },
#             {
#                 "link": "https://stroytorg812.ru/catalog/mebel_dlya_vannoy/tumba_napolnaya_agata_55_s_umyvalnikom_vizit_55_belaya/",
#                 "name": "Тумба напольная Агата 55 с умывальником Визит-55, белая EMMY",
#                 "price": "9 400,00",
#                 "oldPrice": "12 450,00",
#                 "article": "U4079315", 
#                 "brand": "EMMY",
#                 "InStock_trigger": "есть на складе",
#                 "imageLink": "https://stroytorg812.ru/upload/iblock/6f8/103ef337_79a5_11f0_8c17_002590746688_b21dfec2_7e5d_11f0_8c17_002590746688.jpeg"
#             }
#         ]
#     },
#     "search_requests": []
# }

# Сайт 6
data_input_table = {
    "host": "",
    "links": {
        "simple": [
            {
                "link": "https://mosplitka.ru/collections/creto-mono/",
                "name": "Коллекция плитки Creto Mono",
                "price": "от 366 ₽/м2",
                "country": "Россия",
                "imageLink": "https://media.mspltk.ru/1219040/conversions/1s0ze4l426xm3ji1r6abzmjrp2ksh7u4-productSingle.webp"
            }
        ]
    },
    "search_requests": []
}



# region Доп. методы

def print_json(input_json):
    text = json.dumps(input_json, indent=4, ensure_ascii=False)
    text = text.replace('\\"', '"')
    print(text)

def clean_html(text: str) -> str:
    if not text:
        return ""
    text = text.replace("&nbsp;", " ").replace("\xa0", " ")
    text = re.sub(r"[\u200b\u200e\u200f\r\n\t]+", " ", text)
    return text.strip()

def normalize_price(s: str) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = clean_html(s)
    s = re.sub(r"[^\d,\.]", "", s)
    s = re.sub(r"[^\d]", "", s)
    return s

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

from difflib import SequenceMatcher

# Сравнение перестановками. Сравнивает строки более точно
def compute_match_score_2(found_text, target_text):
    found_text = found_text.strip().lower()
    target_text = target_text.strip().lower()

    if not found_text or not target_text:
        return 0.0

    return SequenceMatcher(None, found_text, target_text).ratio()

# TODO Можно заменить compute_match_score на compute_match_score_2, если будет работать ок

# Здесь хранятся html страницы (типо кеша)
content_html = {
    "simple": [
        # {
        #     "link": "",
        #     "html_content": ""  
        # },    
    ]
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

# Проверяю, что html-страница доступна, и данные первого товара на ней есть
check_avialible_html()








# region Поиск селекторов
def find_text_selector(
    html: str,
    text: str,
    exact: bool = True,
    return_all_selectors: bool = False,
    isPriceHandle: bool = False,
    allow_complex_classes: bool = False  # Использовать ли сложные аттрибуты, типо [class*="..."]
):
    IGNORED_ATTRS = {"content", "data-original", "href", "data-src", "src", "data", "alt"}
    IGNORED_SUBSTRS = ["data", "src", "href", "alt"]
    PRIORITY_ATTRS = ["name", "property", "itemprop", "id"]

    if isPriceHandle:
        html = clean_html(html)
        text = normalize_price(text)

    DANGEROUS_CHARS = set(':[]/%%()#')

    def class_is_dangerous(cls: str) -> bool:
        if not cls:
            return False
        if any(ch in cls for ch in DANGEROUS_CHARS):
            return True
        if '"' in cls or "'" in cls or " " in cls:
            return True
        return False

    def escape_attr_value(val: str) -> str:
        return val.replace('"', '\\"')

    def get_css_path(element):
        path = []
        while element and element.name and element.name != "[document]":
            selector = element.name

            # Если есть id — используем его
            if element.has_attr("id"):
                selector = f"#{element['id']}"
                path.append(selector)
                break

            # Классы
            if element.has_attr("class"):
                cls_parts = []
                for cls in element.get("class", []):
                    if not cls:
                        continue
                    # если класс опасный
                    if class_is_dangerous(cls):
                        if allow_complex_classes:
                            cls_parts.append(f'[class*="{escape_attr_value(cls)}"]')
                        else:
                            continue  # ❌ пропускаем опасные классы
                    else:
                        cls_parts.append(f'.{cls}')
                selector += "".join(cls_parts)

            # Проверяем наличие значимых атрибутов
            has_significant_attr = any(
                (
                    attr in PRIORITY_ATTRS or
                    (
                        attr not in IGNORED_ATTRS and
                        not any(sub in attr for sub in IGNORED_SUBSTRS)
                    )
                )
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

    def make_selector(el, base_selector, attr_name):
        parts = [base_selector]
        is_ignored = (
            attr_name in IGNORED_ATTRS or
            any(sub in attr_name for sub in IGNORED_SUBSTRS)
        )

        element_id = el.get("id")
        has_id_in_base = element_id and f"#{element_id}" in base_selector

        if is_ignored:
            for alt_attr in PRIORITY_ATTRS:
                if el.has_attr(alt_attr):
                    if alt_attr == "id" and has_id_in_base:
                        continue
                    val = el.get(alt_attr)
                    if isinstance(val, list):
                        val = " ".join(val)
                    if isinstance(val, str):
                        parts.append(f'[{alt_attr}="{escape_attr_value(val.strip())}"]')
                    break
            parts.append(f'[{attr_name}]')
        else:
            val = el.get(attr_name)
            if isinstance(val, list):
                val = " ".join(val)
            if isinstance(val, str):
                if attr_name == "id" and has_id_in_base:
                    return "".join(parts)
                parts.append(f'[{attr_name}="{escape_attr_value(val.strip())}"]')
            else:
                parts.append(f'[{attr_name}]')

        return "".join(parts)

    # --- Парсим HTML ---
    soup = BeautifulSoup(html, "html.parser")
    selectors = []

    # --- Основной поиск (точное совпадение) ---
    for el in soup.find_all(True):
        element_text = el.get_text(strip=True)
        if element_text:
            check_value = normalize_price(element_text) if isPriceHandle else element_text
            match = (text == check_value) if exact else (text in check_value)
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
                check_value = normalize_price(attr_val) if isPriceHandle else attr_val
                match = (text == check_value) if exact else (text in check_value)
                if match:
                    base_selector = get_css_path(el)
                    selector = make_selector(el, base_selector, attr_name)
                    if return_all_selectors:
                        selectors.append(selector)
                    else:
                        return selector

    # --- Нестрогий поиск ---
    if not selectors:
        threshold = 0.7
        for el in soup.find_all(True):
            element_text = el.get_text(strip=True)
            if element_text:
                check_value = normalize_price(element_text) if isPriceHandle else element_text
                score = similarity(text, check_value)
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
                    check_value = normalize_price(attr_val) if isPriceHandle else attr_val
                    score = similarity(text, check_value)
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






# region Поиск по селектору
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




# region Выбирает один sel

# Основная функция: Получает css селектор, по текстовому содержанию элемента
# Эта функция get_css_selector_from_text_value_element получает на вход один элемент
# Отправляет его в find_text_selector - получает набор css селекторов к этому элементу
# Проверяет, что каждый селектор действительно верный, и сортирует их по точности совпадения
# также сортирует по длине, чем короче тем лучше
# Затем, найденный лучший селектор - дистиллирует
def get_css_selector_from_text_value_element(html, finding_element, is_price = False, is_exact = True):
    print("")
    if isPrint: print(f"🟦 Извлекли такие селекторы для поля \"{finding_element}\":")
    all_selectors = find_text_selector(html, 
                                       finding_element, 
                                       return_all_selectors=True, 
                                       isPriceHandle=is_price, 
                                       exact=is_exact,
                                       allow_complex_classes=False)

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

        if not result_text:
            if isPrint: print("❌ Элемент по селектору не найден или текст пуст")
            continue

        # Безопасно приводим к строке
        result_text = str(result_text)

        # Проверяем наличие подстроки — строгое совпадение по содержанию
        if finding_element.strip() in result_text.strip():
            match_score = 1.0
            if isPrint: print(f"✅ Строгое совпадение: [{result_text[:250]}]")
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

    def sort_key(x):
        selector = x["selector"]
        score = x["score"]
        starts_with_id = selector.strip().startswith("#")
        length = len(selector)
        # Проверяем, заканчивается ли селектор на атрибут (например, [data-id], [href])
        ends_with_attr = selector.strip().endswith("]")

        # Сортируем:
        # 1️⃣ По убыванию score
        # 2️⃣ Сначала селекторы, начинающиеся с '#'
        # 3️⃣ Для '#' — по возрастанию длины, для остальных — по убыванию
        # 4️⃣ В конце селекторы, у которых в конце есть атрибуты в []
        return (
            -score,
            not starts_with_id,            
            ends_with_attr,  # False (нет атрибута) < True (есть атрибут)
            length if starts_with_id else -length,
        )


    valid_selectors.sort(key=sort_key)

    best = valid_selectors[0]
    if isPrint: print("")
    if isPrint: print(f"Лучший селектор: {best['selector']} (совпадение {best['score']*100:.1f}%)")

    # Дистилляция пути
    # result_distill_selector = distill_selector(html, best["selector"], get_element_from_selector, finding_element)
    result_distill_selector = simplify_selector_keep_value(html, best["selector"], get_element_from_selector)
    return result_distill_selector







# region Обр. всех ссылок

# Обрабатываем все элементы из полученного массива - находим для каждого селектор
def fill_selectors_for_items(input_items, get_css_selector_from_text_value_element):
    items = input_items["links"]["simple"] # Проходимся по простым ссылкам
    # TODO В будущем доработать логику - возомжно здесь проходиться по всем массивам ссылок что есть
    host = ""
    
    print(f"Обработаем {len(items)} страниц")
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

        # Извлекаю host, и изменяю imageLink
        if "imageLink" in item and item["imageLink"]:
            link_host = urlparse(item["link"]).scheme + "://" + urlparse(item["link"]).netloc
            image_host = urlparse(item["imageLink"]).scheme + "://" + urlparse(item["imageLink"]).netloc

            # Проверяем, совпадает ли host у ссылки, и ссылки на изображение
            if link_host == image_host:
                host = link_host  # максимум до третьего слеша
                item["_original_imageLink"] = item["imageLink"]
                item["imageLink"] = item["imageLink"].replace(host, "")
            else:
                host = link_host
        if input_items.get("host", "") == "" and host:
            print("🔵 host:", host)
            input_items["host"] = host

        # Проходим по всем ключам, кроме служебных и ссылки
        for key, value in item.items():
            # TODO Позже сделать условие покрасивее, пока что оставлю так
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
                            selector = selector.replace("div.", ".") ### Вот тут может быть ошибка
                            selectors[key] = selector                            
                            break  # если нашли — выходим из цикла
                        elif attempt == 1:
                            print(f"🟨 Не нашли при exact=True, пробуем частичным совпадением")

                    if not selector:
                        print(f"🟧 Не удалось найти селектор для поля {key} даже при exact=False")

                except Exception as e:
                    print(f"🟥 Ошибка при поиске селектора для {key}: {e}")
            else:
                print(f"⬜ Пропускаем поле {key}: Не строка или пустое значение")

        print("_______________________")


        # Записываем обратно
        item["_selectors"] = selectors




# region Результ. sel

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
            # Собираем все уникальные поля из всех примеров
            all_fields = []
            for ex in examples:
                for k in ex.keys():
                    if k not in all_fields and k != "link" and not k.startswith("_"):
                        all_fields.append(k)
            fields = all_fields

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
            total = 0

            for url, tree, ex in trees:
                expected = ex.get(field, "")
                sdict = ex.get("_selectors", {}) if isinstance(ex.get("_selectors", {}), dict) else {}
                if not expected or not sdict.get(field):
                    if verbose:
                        print(f"  [SKIP] {field} on {url}: no expected value or no original selector")
                    continue
                
                total += 1
                extracted_any = ""
                for s in sel_set:
                    got = extract_using_selector(tree, s)
                    if got:
                        extracted_any = got
                        break
                    
                # 💡 Обработка ценовых полей
                if field in ("price", "oldPrice"):
                    match = normalize_price(expected) == normalize_price(extracted_any)
                else:
                    # # match = normalize_text(expected) == normalize_text(extracted_any)
                    # # match = compute_match_score(expected, extracted_any) >= 0.7
                    # score_match = compute_match_score(expected, extracted_any)
                    score_match = compute_match_score_2(expected, extracted_any)
                    # if(field == "imageLink"): # Пониженный порог соответствия для imageLink
                    #     print(f"score_match imageLink = {score_match}")
                    #     if score_match >= 0.5:
                    #         score_match = 1
                    match = expected in extracted_any or extracted_any in expected or score_match >= 0.8

                if not match:
                    if not expected and not extracted_any:
                        continue
                    
                    fails += 1
                    if verbose and print_fail_report:
                        print(f"[🟧 FAIL] {field} on {url}: ")
                        print(f"  искали: '{str(expected)[:200]}' ")
                        print(f"  нашли:  '{str(extracted_any)[:200]}' ")
                        print(f"  селектор: {str(sel_set)[:200]}")
                        # print(f"  score_match = '{score_match:.3f}' ")                        

            return fails == 0

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

    # Собираю результаты селекторы по каждому полю в строку, через запятую
    for key, value in result["result_selectors"].items():
        if isinstance(value, list):
            result["result_selectors"][key] = ", ".join(value) if value else ""

    return result





### Тест одного селектора с одной страницы
# region Тест 1 элемента







isPrint = True

# elem_number = 0
# html = get_html( data_input_table["links"]["simple"][elem_number]["link"])
# # print(html[:500])

# # substring_name = data_input_table["links"]["simple"][elem_number]["name"]
# # substring_price = data_input_table["links"]["simple"][elem_number]["price"]
# # substring_oldPrice = data_input_table["links"]["simple"][elem_number]["oldPrice"]
# # substring_brand = data_input_table["links"]["simple"][elem_number]["brand"]
# # substring_article = data_input_table["links"]["simple"][elem_number]["article"]
# substring_imageLink = data_input_table["links"]["simple"][elem_number]["imageLink"]

# # selector_result = get_css_selector_from_text_value_element(html, substring_name)
# # selector_result = get_css_selector_from_text_value_element(html, substring_price, is_price = True)
# # selector_result = get_css_selector_from_text_value_element(html, substring_oldPrice, is_price = True)
# # selector_result = get_css_selector_from_text_value_element(html, substring_brand)
# # selector_result = get_css_selector_from_text_value_element(html, substring_article)
# # selector_result = get_css_selector_from_text_value_element(html, substring_article, is_exact=False)
# selector_result = get_css_selector_from_text_value_element(html, substring_imageLink)
# print("")
# print(f"🟩 selector_result = {selector_result}")











# region Обр. всех sel

fill_selectors_for_items(
    data_input_table,
    get_css_selector_from_text_value_element
)

print_json(data_input_table["links"]["simple"])

result_select_best_selectors = select_best_selectors(data_input_table["links"]["simple"], content_html)

print("")
print("")
print("✅ Итоговые селекторы:")
print_json(result_select_best_selectors["result_selectors"])





















# Собирает финальный код для вставки в шаблон
def selectorChecker(result_selectors):
    """
    Проверяет, что все селекторы действительно извлекают то что нужно
    И если нужно, то собирает код, который правит их результаты, или как-то
    по другому обрабатывает (через агента генерации кода)
    

    Если InStock_trigger и OutOfStock_trigger - одинаковые, то
    используем проверку на InStock_trigger, а по умолчанию оставляем занчение "OutOfStock"

    Использует автоформаттер для price и oldPrice
    Проверяет, что итоговые значения корректны
        Простейшая проверка - попробовать пройтись parseInt

    Здесь же будут проверяться все значения на ситуации по типу: Например значение артикула может собираться как: "Артикул: 112233"
        а нам нужно собрать только "112233"

    """

    print("Проверяем селекторы, и генерируем parseCard")






















# Для примера
result_selectors = {
    "price": "meta[itemprop=\"price\"][content]",
    "name": "#pagetitle",
    "imageLink": "",
    "brand": "meta[itemprop=\"brand\"][content]",
    "stock": "div.catalog-element-panel-quantity-wrap"
}


selectorChecker(result_selectors)






















"""

Вынести в отдельный фалйлик

find_text_selector - принимает содержимое, возвращает набор селекторов
    get_element_from_selector - проверка наличия содержимого в селекторе
get_css_selector_from_text_value_element - принимает массив, валидирует, сортирует, и возвращает один лучший
    simplify_selector_keep_value - дистилляция этого лучшего, перед возвратом

"""














"""

После этого:

Починить всё, на тех примерах что у меня есть
    На 1м сайте не работают imageLink
    2й Ок
    3й ок, но надо больше страниц добавить
    - 4й не ок

Протестировать на разных других сайтах

В imageLink можно попробовать искать подстроку, без хоста

С oldPrice - извлекать селекторы напрямую, остальную логику напишу позже в selectorChecker()

Написать реализацию selectorChecker(), которая будет возвращать текст уже для финального шаблона кода


Можно тестировать на сайтах для ЗКС


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




############### imageLink Не отрабатывает у 1го сайта
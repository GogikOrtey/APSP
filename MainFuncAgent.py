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


# result = find_contexts(html, "10&nbsp;320 руб.")
# print(result)



# # Умное сравнение строк (например, цен)
# def fuzzy_text_match(a: str, b: str) -> bool:
#     # Раскодируем HTML сущности (&nbsp;, &amp; и т.д.)
#     a = html.unescape(a or "")
#     b = html.unescape(b or "")

#     # Убираем "мусор": валюты, пробелы, точки, запятые, 'руб', 'р', '₽'
#     clean_a = re.sub(r"[\s\u00A0₽рруб.,]+", "", a.lower())
#     clean_b = re.sub(r"[\s\u00A0₽рруб.,]+", "", b.lower())

#     # Если обе строки числовые — сравниваем цифры
#     if clean_a.isdigit() and clean_b.isdigit():
#         return clean_a == clean_b

#     # Иначе — частичное вхождение
#     return clean_a in clean_b or clean_b in clean_a


# # Находит и возвращает css селектор(ы) элемента(ов) по содержимому
# def find_text_selector(html: str, text: str, exact: bool = True, return_all_selectors: bool = False):
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
#     selectors = []

#     for el in soup.find_all(True):
#         el_text = el.get_text(strip=True)
#         # Текст внутри элемента
#         if el_text:
#             match = (text.strip() == el_text) if exact else fuzzy_text_match(text, el_text)
#             if match:
#                 selector = get_css_path(el)
#                 if return_all_selectors:
#                     selectors.append(selector)
#                     continue
#                 return selector

#         # Проверка атрибутов
#         for attr_name, attr_val in el.attrs.items():
#             if isinstance(attr_val, list):
#                 attr_val = " ".join(attr_val)
#             if isinstance(attr_val, str):
#                 match = (text.strip() == attr_val.strip()) if exact else fuzzy_text_match(text, attr_val)
#                 if match:
#                     selector = get_css_path(el) + f"[{attr_name}]"
#                     if return_all_selectors:
#                         selectors.append(selector)
#                         continue
#                     return selector

#     if return_all_selectors:
#         return selectors if selectors else None
#     return None






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


# def distill_selector(html, selector, get_element_from_selector, expected_value):
#     """
#     Пробует сократить CSS селектор, удаляя ненужные звенья.
#     Если удаление звена ломает результат, звено сохраняется.
#     Возвращает максимально упрощённый корректный селектор.
#     """

#     parts = [part.strip() for part in selector.split(">")]
#     if len(parts) < 2:
#         return selector

#     # print(f"🔍 Исходный селектор: {selector}")
#     # print(f"🧩 Всего звеньев: {len(parts)}")

#     i = 0
#     while i < len(parts) - 1:  # последний не трогаем
#         test_parts = parts[:i] + parts[i+1:]
#         test_selector = " > ".join(test_parts)

#         result = get_element_from_selector(html, test_selector)

#         if result == expected_value:
#             # print(f"✅ Удалено звено {i+1}/{len(parts)}: {parts[i]}")
#             parts.pop(i)  # Удаляем звено окончательно, не двигаем индекс
#         else:
#             # print(f"❌ Нельзя удалить звено {i+1}: {parts[i]}")
#             i += 1  # Переходим к следующему

#     final_selector = " > ".join(parts)
#     # print(f"🏁 Итоговый очищенный селектор:\n{final_selector}")
#     print("")
#     print("🔷 Выполнили дистилляцию селектора")
#     return final_selector


# # Также плохо чистит этот большой селектор price
# """
# def distill_selector(html, selector, get_element_from_selector, expected_value):
    
#     Сокращает CSS селектор до минимально возможного, удаляя все ненужные звенья.
#     Проверяет каждое звено: если после его удаления результат сохраняется — удаляем.
#     Использует пробелы, чтобы не требовать строгой иерархии.
    
#     # Разбиваем селектор на части
#     parts = [part.strip() for part in selector.replace(">", " ").split()]
#     if len(parts) < 2:
#         return selector

#     changed = True
#     while changed:
#         changed = False
#         i = 0
#         while i < len(parts):
#             test_parts = parts[:i] + parts[i+1:]
#             if not test_parts:
#                 i += 1
#                 continue

#             test_selector = " ".join(test_parts)
#             result = get_element_from_selector(html, test_selector)

#             if result == expected_value:
#                 # Удаляем ненужное звено
#                 parts.pop(i)
#                 changed = True
#                 # Не увеличиваем i, так как сдвинулись звенья
#             else:
#                 i += 1

#     final_selector = " ".join(parts)
#     print("")
#     print("🔷 Выполнили дистилляцию селектора (минимальный путь)")
#     return final_selector
# """




# selector = "#i-18-bitrix-catalog-element-catalog-default-1-qepX1RQfHh6Q > div.catalog-element-wrapper.intec-content.intec-content-visible > div.catalog-element-wrapper-2.intec-content-wrapper > div.catalog-element-information-wrap > div.catalog-element-information.intec-grid.intec-grid-nowrap.intec-grid-768-wrap.intec-grid-a-h-start.intec-grid-a-v-start.intec-grid-i-20:nth-of-type(3) > div.catalog-element-information-right.intec-grid-item.intec-grid-item-768-1:nth-of-type(2) > div.catalog-element-information-right-wrapper > div.catalog-element-information-part.intec-grid.intec-grid-wrap.intec-grid-a-v-center.intec-grid-i-10 > div.intec-grid-item-auto:nth-of-type(2) > a.catalog-element-brand.intec-ui-picture > img[alt]"
# result_distill_selector = distill_selector(html, selector, get_element_from_selector, "Аntika")
# print(result_distill_selector)




















### Старая, рабочая
# # Основная функция: Получает css селектор, по текстовому соержанию элемента
# def get_css_selector_from_text_value_element(html, finding_element):
#     print("")
#     print(f"🟦 Извлекли такие селекторы для поля \"{finding_element}\":")
#     all_selectors = find_text_selector(html, finding_element, return_all_selectors=True)
#     # print(all_selectors)

#     if not all_selectors:
#         print("🟡 Не найдено ни одного подходящего селектора")
#         return ""

#     # Сортируем селекторы по длине (от короткого к длинному)
#     all_selectors = sorted(all_selectors, key=len)

#     # Проверяем каждый селектор
#     for selector in all_selectors:
#         print("")
#         print(f"🟢 Проверка селектора: {selector}")
#         result_element = get_element_from_selector(html, selector)

#         # Если элемент найден — возвращаем этот селектор
#         if result_element != "":
#             print("✅ Найден корректный селектор")

#             # Дистилляция путей селектора
#             result_distill_selector = distill_selector(html, selector, get_element_from_selector, finding_element)

#             return result_distill_selector
#         else:
#             print("❌ Элемент по селектору не найден")

#     # Если ни один не подошёл
#     print("🔴 Не найдено корректного селектора")
#     return ""


import re

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
    while i < len(parts):
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
            # НЕ инкрементируем i: нужно попытаться удалить новое звено на этой же позиции
            # (поведение: удаляем как можно больше подряд)
            # но если i теперь == len(parts) (удалили последний) - цикл завершится naturally
            continue
        else:
            # удаление ломает — оставляем звено и идём дальше
            i += 1

    # собрать итоговый селектор
    simplified = " > ".join(parts)
    return simplified






# Основная функция: Получает css селектор, по текстовому соержанию элемента
def get_css_selector_from_text_value_element(html, finding_element, is_price = False):
    print("")
    print(f"🟦 Извлекли такие селекторы для поля \"{finding_element}\":")
    if(is_price):
        # Для извлечения price и oldPrice - отдельный отбработчик
        all_selectors = handle_selector_price(html, finding_element)
    else:
        all_selectors = find_text_selector(html, finding_element, return_all_selectors=True)

    if not all_selectors:
        print("🟡 Не найдено ни одного подходящего селектора")
        return ""

    print(f"Найдено {len(all_selectors)} возможных селекторов")

    valid_selectors = []

    # Проверяем каждый селектор
    for selector in all_selectors:
        print("")
        print(f"🟢 Проверка селектора: {selector}")
        result_text = get_element_from_selector(html, selector)

        if result_text == "":
            print("❌ Элемент по селектору не найден")
            continue

        # Проверяем наличие подстроки — строгое совпадение по содержанию
        if finding_element.strip() in result_text.strip():
            match_score = 1.0
            print(f"✅ Строгое совпадение: [{result_text}]")
        else:
            # Если нет прямого вхождения — оцениваем схожесть
            match_score = compute_match_score(result_text, finding_element)
            print(f"⚪ Совпадение {match_score*100:.1f}%: [{result_text}]")

        valid_selectors.append({
            "selector": selector,
            "result": result_text,
            "score": match_score
        })

    # Если ни один не подошёл
    if not valid_selectors:
        print("🔴 Не найдено корректных селекторов")
        return ""

    # Сортируем:
    # 1️⃣ по совпадению (по убыванию)
    # 2️⃣ при равных — по длине селектора (по возрастанию)
    valid_selectors.sort(key=lambda x: (-x["score"], len(x["selector"])))

    best = valid_selectors[0]
    print("")
    print(f"🏆 Лучший селектор: {best['selector']} (совпадение {best['score']*100:.1f}%)")

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



# TODO Потом надо будет слить всё в один метод, а не выделять отдельно извлечение цен (чисел)


# substring = "Makita"
substring_brand = data_input_table["links"]["simple"][0]["brand"]
substring_name = data_input_table["links"]["simple"][0]["name"]
# substring_price = data_input_table["links"]["simple"][0]["price"]
substring_price = "10 320"

selector_result = get_css_selector_from_text_value_element(html, substring_name)
# selector_result = get_css_selector_from_text_value_element(html, substring_brand)
# selector_result = get_css_selector_from_text_value_element(html, substring_price, is_price = True)
print("")
print(f"🟩 selector_result = {selector_result}")








































# Старое:
#i-18-bitrix-catalog-element-catalog-default-1-qepX1RQfHh6Q > div.catalog-element-wrapper.intec-content.intec-content-visible > div.catalog-element-wrapper-2.intec-content-wrapper > div.catalog-element-information-wrap > div.catalog-element-information.intec-grid.intec-grid-nowrap.intec-grid-768-wrap.intec-grid-a-h-start.intec-grid-a-v-start.intec-grid-i-20:nth-of-type(3) > div.catalog-element-information-right.intec-grid-item.intec-grid-item-768-1:nth-of-type(2) > div.catalog-element-information-right-wrapper > div.catalog-element-information-part.intec-grid.intec-grid-wrap.intec-grid-a-v-center.intec-grid-i-10 > div.intec-grid-item-auto:nth-of-type(2) > a.catalog-element-brand.intec-ui-picture > img
# selector = "html > body > div.wrapper > img:nth-of-type(1)"
# selector = "a.catalog-element-brand img"
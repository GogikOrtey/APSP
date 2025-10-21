import re
from lxml import html as html_lx, etree

# === 1. Загружаем HTML ===
with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()

finding_element = "10 320"

# === 2. Очистка HTML ===
def clean_html(text: str) -> str:
    text = text.replace("&nbsp;", " ").replace("\xa0", " ")
    text = re.sub(r"[\u200b\u200e\u200f\r\n\t]+", " ", text)
    return text.strip()

html = clean_html(html)

# === 3. Нормализация числовых строк ===
def normalize_price(s: str) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"[^\d,\.]", "", s)
    s = re.sub(r"[^\d]", "", s)
    return s

target_norm = normalize_price(finding_element)

# === 4. Поиск по DOM ===
tree = html_lx.fromstring(html)
results = []

for elem in tree.iter():
    # Пропускаем комментарии, доктайпы и т.п.
    if not isinstance(elem.tag, str):
        continue

    # Проверяем текст
    text = elem.text_content().strip() if elem.text_content() else ""
    if text and normalize_price(text) == target_norm:
        results.append(("text", elem, text))

    # Проверяем атрибуты
    for attr_name, attr_val in elem.attrib.items():
        if normalize_price(attr_val) == target_norm:
            results.append((f"attr:{attr_name}", elem, attr_val))

# === 5. Вывод результатов ===
if not results:
    print("⚠️ Совпадений не найдено")
else:
    for typ, elem, val in results:
        print(f"✅ Найдено совпадение в {typ}: {val}")
        print("HTML элемента:")
        print(html_lx.tostring(elem, encoding="unicode", pretty_print=True))
        print("-" * 80)

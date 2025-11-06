



"""

Парсинг поиска написать реально намного проще
Даже можно дигинетику далеко на потом оставить (когда научимся открывать внутренний браузер)

Если нет извлечения items в parsePage, то удалить эту логику из parse
Но оставить ко на будущее, который это добавляет

TODO На потом: Проверять, приходят ли данные товара где-либо ещё, кроме html страницы поиска
и если да, то уже задействовать json-парсеры, и геттеры


"""


def generate_parsePage():
    template_parseCard = Template("""
    async parseCard(set: SetType, cacher: Cacher<ResultItem[]>) {
        let items: ResultItem[] = []

        const data = await this.makeRequest(set.query);
        $cheerioLoad

        $varFromSelector
        const link = set.query
        const timestamp = getTimestamp()

        const item: ResultItem = {
            $itemsFields
        }
        items.push(item);

        cacher.cache = items
        return items;
    }
    """)

    result = template_parseCard.substitute(
        itemsFields=items_fields,
        varFromSelector=value_field,
        cheerioLoad="const $ = cheerio.load(data);",
    )

    print(result)
    return result
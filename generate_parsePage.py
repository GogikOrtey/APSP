# Подключение всех библиотек
from import_all_libraries import * 



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
    async parsePage(set: SetType) {
        let url = new URL(`$${HOST}/search`)
        url.searchParams.set("q", set.query)
        url.searchParams.set("page", set.page)

        const data = await this.makeRequest(url.href)
        const $$ = cheerio.load(data)

        if (set.page === 1) {
            let totalPages = Math.max(...$$("").get().map(item => +$$(item).text().trim()).filter(Boolean))
            this.debugger.put(`totalPages = $${totalPages}`)
            for (let page = 2; page <= Math.min(totalPages, +this.conf.pagesCount); page++) {
                this.query.add({ ...set, query: set.query, type: "page", page: page, lvl: 1 });
            }
        }

        let items: ResultItem[] = [];
        let products = $$("")
        if (products.length == 0) {
            this.logger.put(`По запросу $${set.query} ничего не найдено`)
            throw new NotFoundError()
        }
        products.slice(0, +this.conf.itemsCount).each((i, product) => {
            let link = $$(product)?.attr("href")
            this.query.add({ ...set, query: link, type: "card", lvl: 1 })
        })
        return items;
    }
    """)

    result = template_parseCard.substitute(
        # cheerioLoad="const $ = cheerio.load(data);",
    )

    print(result)
    return result


generate_parsePage()
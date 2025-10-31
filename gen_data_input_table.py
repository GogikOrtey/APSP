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

# # Сайт 1
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

# # Сайт 6
# data_input_table = {
#     "host": "",
#     "links": {
#         "simple": [
#             {
#                 "link": "https://mosplitka.ru/collections/creto-mono/",
#                 "name": "Коллекция плитки Creto Mono",
#                 "price": "от 366 ₽/м2",
#                 "country": "Россия",
#                 "imageLink": "https://media.mspltk.ru/1219040/conversions/1s0ze4l426xm3ji1r6abzmjrp2ksh7u4-productSingle.webp"
#             }
#         ]
#     },
#     "search_requests": []
# }


# Сайт 7
data_input_table = {
    "host": "",
    "links": {
        "simple": [
            {
                "link": "https://plitburg.ru/catalog/plitka/e_5020_mr_600x600x9_rock_seryy_svetlyy_matovyy_kg_60x60_dako/",
                "name": "Керамогранит серый матовый 60х60 Dako (Дако) E-5020 Rock",
                "price": "1 729 ₽ / м2",
                "oldPrice": "1 820 ₽",
                "article": "E-5020/MR/600x600x9",
                "brand": "DAKO",
                "InStock_trigger": "В наличии",
                "imageLink": "https://plitburg.ru/upload/dev2fun.imagecompress/webp/iblock/81e/yypuhdwg8uf7jtktf65opgzc4wthjo6w.webp"
            },
            {
                "link": "https://plitburg.ru/catalog/plitka/e_3032_mr_600x600x9_vita_seryy_matovyy_kg_60x60_dako/",
                "name": "Керамогранит серый матовый 60х60 Dako (Дако) E-3032 Vita",
                "price": "1 729 ₽ / м2",
                "oldPrice": "1 820 ₽",
                "article": "E-3032/MR/600x600x9",
                "brand": "DAKO",
                "InStock_trigger": "В наличии",
                "imageLink": "https://plitburg.ru/upload/dev2fun.imagecompress/webp/iblock/c1b/p1e31vas9p6qew6ssb9pfy0afbns6he5.webp"
            },
            {
                "link": "https://plitburg.ru/catalog/plitka/dd602320r_pro_matriks_temno_seryy_obreznoy_keramogranit_60x60_kerama_marazzi/",
                "name": "DD602320R Про Матрикс темно-серый обрезной керамогранит 60x60, Kerama Marazzi",
                "price": "2 345 ₽ / м2",
                "oldPrice": "",
                "article": "DD602320R",
                "brand": "Kerama Marazzi",
                "OutOfStock_trigger": "Под заказ: 3-5 дней",
                "imageLink": "https://plitburg.ru/upload/dev2fun.imagecompress/webp/iblock/ce2/r000qg0trz32gftjt8wy57g4kns4uv80.webp"
            }
        ]
    },
    "search_requests": []
}
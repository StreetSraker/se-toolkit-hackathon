# Car database with 90s and 00s cars
CARS = [
    {
        "id": "supra",
        "name": "Toyota Supra A80",
        "years": "1993-2002",
        "image": "/static/images/cars/supra.svg",
        "description": "Легендарный японский спорткар с рядной шестеркой 2JZ-GTE"
    },
    {
        "id": "skyline",
        "name": "Nissan Skyline R34 GT-R",
        "years": "1999-2002",
        "image": "/static/images/cars/skyline.svg",
        "description": "Godzilla - легендарный полноприводный спорткар с RB26DETT"
    },
    {
        "id": "rx7",
        "name": "Mazda RX-7 FD",
        "years": "1992-2002",
        "image": "/static/images/cars/rx7.svg",
        "description": "Спорткар с роторно-поршневым двигателем 13B-REW"
    },
    {
        "id": "nsx",
        "name": "Honda NSX (NA1/NA2)",
        "years": "1990-2005",
        "image": "/static/images/cars/nsx.svg",
        "description": "Среднемоторный суперкар с V6 VTEC, разработан при участии Айртона Сенны"
    },
    {
        "id": "silvia",
        "name": "Nissan Silvia S15",
        "years": "1999-2002",
        "image": "/static/images/cars/silvia.svg",
        "description": "Идеальный автомобиль для дрифта с двигателем SR20DET"
    },
    {
        "id": "chaser",
        "name": "Toyota Chaser JZX100",
        "years": "1996-2001",
        "image": "/static/images/cars/chaser.svg",
        "description": "Седан с легендарным 1JZ-GTE, популярная платформа для тюнинга"
    },
    {
        "id": "civic",
        "name": "Honda Civic Type R (EK9)",
        "years": "1997-2000",
        "image": "/static/images/cars/civic.svg",
        "description": "Легендарный хэтчбек с высокооборотистым B16B VTEC"
    },
    {
        "id": "evo",
        "name": "Mitsubishi Lancer Evolution VI",
        "years": "1999-2001",
        "image": "/static/images/cars/evo.svg",
        "description": "Раллийный чемпион с 4G63T и продвинутым полным приводом AYC"
    },
    {
        "id": "impreza",
        "name": "Subaru Impreza WRX STI (GC8)",
        "years": "1998-2000",
        "image": "/static/images/cars/impreza.svg",
        "description": "Культовый полноприводный седан с оппозитным EJ20 с турбонаддувом"
    },
    {
        "id": "ae86",
        "name": "Toyota Sprinter Trueno AE86",
        "years": "1983-1987",
        "image": "/static/images/cars/ae86.svg",
        "description": "Легенда дрифта с двигателем 4A-GE, звезда Initial D"
    }
]

# Engine options database
ENGINES = {
    "supra": [
        {"id": "2jz-stock", "name": "2JZ-GTE Stock", "power": "280 л.с.", "description": "Стоковый турбомотор"},
        {"id": "2jz-single", "name": "2JZ-GTE Single Turbo", "power": "500-700 л.с.", "description": "Конверсия на один большой турбо"},
        {"id": "2jz-stroker", "name": "2JZ-GTE Stroker 3.4L", "power": "800-1000 л.с.", "description": "Увеличенный объём с кованным internals"},
        {"id": "2jz-vvti", "name": "2JZ-GTE VVT-i Build", "power": "1000+ л.с.", "description": "Максимальная сборка с VVT-i головкой"},
    ],
    "skyline": [
        {"id": "rb26-stock", "name": "RB26DETT Stock", "power": "280 л.с.", "description": "Стоковый мотор Godzilla"},
        {"id": "rb26-stroker", "name": "RB26DETT Stroker 2.8L", "power": "600-800 л.с.", "description": "Увеличенный объём для большего буста"},
        {"id": "rb30", "name": "RB30DE + RB26 Head", "power": "700-900 л.с.", "description": "Гибрид RB30 блока с RB26 головкой"},
        {"id": "vr38-swap", "name": "VR38DETT Swap", "power": "600-1000+ л.с.", "description": "Установка мотора от GT-R R35"},
    ],
    "rx7": [
        {"id": "13b-stock", "name": "13B-REW Stock", "power": "280 л.с.", "description": "Стоковый ротор с твин-турбо"},
        {"id": "13b-single", "name": "13B-REW Single Turbo", "power": "400-600 л.с.", "description": "Конверсия на один турбо Precision/Garrett"},
        {"id": "13b-bridge", "name": "13B Bridge Port", "power": "500-700 л.с.", "description": "Распиленный порт для высоких оборотов"},
        {"id": "20b-swap", "name": "20B-REW Swap", "power": "300-600 л.с.", "description": "Установка 3-секционного ротора"},
    ],
    "nsx": [
        {"id": "c30a-stock", "name": "C30A Stock", "power": "274 л.с.", "description": "Стоковый V6 VTEC"},
        {"id": "c30a-sc", "name": "C30A Supercharged", "power": "350-400 л.с.", "description": "Компрессор Comptech/CTS"},
        {"id": "c32b", "name": "C32B Swap", "power": "290 л.с.", "description": "Мотор от NSX-R"},
        {"id": "k-swap", "name": "K-Series Swap", "power": "400-600 л.с.", "description": "Установка K20/K24 с турбо"},
    ],
    "silvia": [
        {"id": "sr20-stock", "name": "SR20DET Stock", "power": "250 л.с.", "description": "Стоковый турбомотор"},
        {"id": "sr20-vvt", "name": "SR20DET VVT Swap", "power": "400-600 л.с.", "description": "Головка SR20VE с турбо"},
        {"id": "sr20-stroker", "name": "SR20DET Stroker 2.2L", "power": "500-700 л.с.", "description": "Увеличенный объём с кованным internals"},
        {"id": "rb-swap", "name": "RB25/RB26 Swap", "power": "400-800 л.с.", "description": "Установка рядной шестёрки RB"},
    ],
    "chaser": [
        {"id": "1jz-stock", "name": "1JZ-GTE Stock", "power": "280 л.с.", "description": "Стоковый турбомотор"},
        {"id": "1jz-vvti", "name": "1JZ-GTE VVT-i", "power": "320 л.с.", "description": "Версия с VVT-i (Version 2)"},
        {"id": "1jz-single", "name": "1JZ-GTE Single Turbo", "power": "500-800 л.с.", "description": "Конверсия на один большой турбо"},
        {"id": "2jz-swap", "name": "2JZ-GTE Swap", "power": "600-1000+ л.с.", "description": "Установка старшего брата 2JZ"},
    ],
    "civic": [
        {"id": "b16b-stock", "name": "B16B Stock", "power": "185 л.с.", "description": "Стоковый высокооборотистый VTEC"},
        {"id": "b16b-built", "name": "B16B Built", "power": "250-300 л.с.", "description": "Кованная поршневая, распредвалы"},
        {"id": "b18c", "name": "B18C Swap", "power": "200 л.с.", "description": "Мотор от Integra Type R"},
        {"id": "k-swap", "name": "K20A Swap", "power": "300-500 л.с.", "description": "Установка K-Series с турбо"},
    ],
    "evo": [
        {"id": "4g63-stock", "name": "4G63T Stock", "power": "280 л.с.", "description": "Стоковый турбомотор"},
        {"id": "4g63-built", "name": "4G63T Built", "power": "400-600 л.с.", "description": "Кованная поршневая, турбо FP"},
        {"id": "4g63-stroker", "name": "4G63T Stroker 2.2L", "power": "500-700 л.с.", "description": "Увеличенный объём с big turbo"},
        {"id": "4b11-swap", "name": "4B11 Swap (Evo X)", "power": "400-600 л.с.", "description": "Мотор от Evo X"},
    ],
    "impreza": [
        {"id": "ej20-stock", "name": "EJ20 Stock", "power": "280 л.с.", "description": "Стоковый оппозит с турбо"},
        {"id": "ej20-built", "name": "EJ20 Built", "power": "400-500 л.с.", "description": "Кованная поршневая, турбо VF/ Garrett"},
        {"id": "ej22", "name": "EJ22 Stroker", "power": "500-600 л.с.", "description": "Увеличенный объём 2.2L"},
        {"id": "ej25", "name": "EJ25 Swap", "power": "400-600 л.с.", "description": "Блок 2.5L с головкой EJ20"},
    ],
    "ae86": [
        {"id": "4age-stock", "name": "4A-GE Stock", "power": "130 л.с.", "description": "Стоковый высокооборотистый мотор"},
        {"id": "4age-built", "name": "4A-GE Built", "power": "200-250 л.с.", "description": "Дросселя, распредвалы, порт"},
        {"id": "20v-blacktop", "name": "4A-GE 20V Black Top", "power": "165 л.с.", "description": "20-клапанная версия от AE111"},
        {"id": "3sgte-swap", "name": "3S-GTE Swap", "power": "300-500 л.с.", "description": "Установка турбомотора от Celica MR2"},
    ],
}

# Suspension setups
SUSPENSIONS = {
    "street": {
        "name": "Street Comfort",
        "description": "Комфортная настройка для ежедневной езды",
        "ride_height": "-30 мм",
        "dampening": "Мягкая",
        "spring_rate": "6-8 кг/мм",
        "camber": "-1.0°",
        "use_case": "Ежедневная езда, круизы"
    },
    "sport": {
        "name": "Sport Setup",
        "description": "Спортивная настройка для активных поездок",
        "ride_height": "-50 мм",
        "dampening": "Средняя",
        "spring_rate": "8-10 кг/мм",
        "camber": "-1.5°",
        "use_case": "Спортивная езда, горные дороги"
    },
    "drift": {
        "name": "Drift Spec",
        "description": "Настройка для дрифта с увеличенным углом выворота",
        "ride_height": "-60 мм",
        "dampening": "Жёсткая перед / средняя зад",
        "spring_rate": "10-12 кг/мм",
        "camber": "-2.0° перед / -1.0° зад",
        "use_case": "Дрифт, соревнования"
    },
    "track": {
        "name": "Track Attack",
        "description": "Трековая настройка для максимальной производительности",
        "ride_height": "-70 мм",
        "dampening": "Жёсткая",
        "spring_rate": "12-14 кг/мм",
        "camber": "-2.5°",
        "use_case": "Трек-дни, тайм-атак"
    },
    "stance": {
        "name": "Stance Show",
        "description": "Экстремально заниженная для выставок",
        "ride_height": "-100 мм",
        "dampening": "Пневмоподвеска / Койловеры",
        "spring_rate": "8-10 кг/мм",
        "camber": "-3.0° и более",
        "use_case": "Выставки, шоу"
    },
}

# Bodykit options (4 options as requested)
BODYKITS = [
    {
        "id": "rocket_bunny",
        "name": "Rocket Bunny / Pandem",
        "description": "Широкие арки из стекловолокна, агрессивный вид",
        "components": ["Широкие передние крылья", "Широкие задние крылья", "Передний бампер", "Задний бампер", "Пороги", "Сплиттер", "ГТ-крыло"],
        "style": "Агрессивный widebody",
        "price_range": "$2500-4000"
    },
    {
        "id": "varis",
        "name": "VARIS",
        "description": "Японский премиум обвес, разработан на треке",
        "components": ["Карбоновый капот", "Передний бампер с канардами", "Задний диффузор", "GT Wing", "Пороги"],
        "style": "Аэродинамический трековый",
        "price_range": "$3000-5000"
    },
    {
        "id": "n1",
        "name": "N1 / Origin Labo",
        "description": "Стиль 90-х с широкими арками в стиле Super Silhouette",
        "components": ["Широкие арки N1", "Передний бампер", "Задний бампер", "Боковые юбки", "GT крыло"],
        "style": "Retro 90s Super Silhouette",
        "price_range": "$2000-3500"
    },
    {
        "id": "pandem_wide",
        "name": "Pandem Wide Arch",
        "description": "Экстремально широкие арки для максимального эффекта",
        "components": ["Экстра-широкие передние арки", "Экстра-широкие задние арки", "Агрессивный передний сплиттер", "Задний диффузор", "Боковые юбки", "Большое GT крыло"],
        "style": "Экстремальный widebody",
        "price_range": "$2500-4500"
    },
]

# Wheel options (~10 options as requested)
WHEELS = [
    {
        "id": "rays_volk",
        "name": "Rays Volk Racing TE37",
        "description": "Легендарные кованые диски, икона JDM",
        "sizes": "17x9 / 18x9.5 / 18x10.5",
        "weight": "7.2 кг (17\")",
        "style": "6 спиц",
        "price_range": "$1200-1800/комплект"
    },
    {
        "id": "work_emotion",
        "name": "Work Emotion CR Kai",
        "description": "Классические JDM диски с глубокой полкой",
        "sizes": "17x8.5 / 18x9 / 18x9.5",
        "weight": "8.1 кг (17\")",
        "style": "10 спиц mesh",
        "price_range": "$900-1300/комплект"
    },
    {
        "id": "ssr_profix",
        "name": "SSR Professor SP1",
        "description": "Премиальные диски в классическом стиле",
        "sizes": "18x8.5 / 18x9.5 / 19x10",
        "weight": "9.0 кг (18\")",
        "style": "3-piece mesh",
        "price_range": "$1500-2200/комплект"
    },
    {
        "id": "advan_racing",
        "name": "Advan Racing GT",
        "description": "Лёгкие трековые диски от Yokohama",
        "sizes": "17x9 / 18x9.5 / 18x10",
        "weight": "6.9 кг (17\")",
        "style": "5 Y-спиц",
        "price_range": "$1000-1500/комплект"
    },
    {
        "id": "weds_sport",
        "name": "WedsSport TC-105X",
        "description": "Легчайшие японские диски для трека",
        "sizes": "17x8.5 / 17x9 / 18x9.5",
        "weight": "6.5 кг (17\")",
        "style": "10 тонких спиц",
        "price_range": "$900-1400/комплект"
    },
    {
        "id": "enkei_rpf1",
        "name": "Enkei RPF1",
        "description": "Универсальные лёгкие диски, выбор для тайм-атак",
        "sizes": "15x7 / 16x8 / 17x9 / 18x10",
        "weight": "6.4 кг (17\")",
        "style": "6 twin-spoke",
        "price_range": "$800-1200/комплект"
    },
    {
        "id": "bbs_rs",
        "name": "BBS RS-GT",
        "description": "Немецкая классика с золотыми спицами",
        "sizes": "17x8.5 / 18x9 / 18x9.5",
        "weight": "7.8 кг (17\")",
        "style": "Mesh золотые спицы",
        "price_range": "$1800-2500/комплект"
    },
    {
        "id": "oz_ultra",
        "name": "OZ Ultraleggera",
        "description": "Итальянские облегчённые диски",
        "sizes": "17x7.5 / 18x8 / 18x9",
        "weight": "6.8 кг (17\")",
        "style": "5 Y-спиц",
        "price_range": "$1000-1500/комплект"
    },
    {
        "id": "work_cr_kai",
        "name": "Work CR Kai 3-Piece",
        "description": "Классические 3-составные диски в стиле 90-х",
        "sizes": "17x9 / 18x9.5 / 18x10.5",
        "weight": "8.5 кг (17\")",
        "style": "Step-lip mesh",
        "price_range": "$1500-2000/комплект"
    },
    {
        "id": "rays_volk_g25",
        "name": "Rays Volk Racing G25",
        "description": "Современная классика от Rays, 5 спиц",
        "sizes": "18x9 / 18x9.5 / 18x10.5",
        "weight": "7.5 кг (18\")",
        "style": "5 спиц",
        "price_range": "$1300-1800/комплект"
    },
    {
        "id": " Volk_racing_ce28n",
        "name": "Rays Volk Racing CE28N",
        "description": "6 спиц, кованые, идеальны для стэнса",
        "sizes": "17x8.5 / 18x9 / 18x9.5",
        "weight": "7.0 кг (17\")",
        "style": "6 спиц",
        "price_range": "$1400-2000/комплект"
    },
]

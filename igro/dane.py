
points = [
    {
        "id": "ZG",
        "name": "Zielona Góra",
        "lat": 51.9354800,
        "lon": 15.5064300
    },
    {
        "id": "NB",
        "name": "Nowogród Bobrzański",
        "lat": 51.798346,
        "lon": 15.236140
    },
    {
        "id": "ZR",
        "name": "Żary",
        "lat": 51.636,
        "lon": 15.138
    },
    {
        "id": "ZA",
        "name": "Żagań",
        "lat": 51.616591,
        "lon": 15.317660
    },
    {
        "id": "SZP",
        "name": "Szprotawa",
        "lat": 51.567,
        "lon": 15.538
    },
    {
        "id": "KOZ",
        "name": "Kożuchów",
        "lat": 51.745,
        "lon": 15.595
    },
    {
        "id": "NS",
        "name": "Nowa Sól",
        "lat": 51.8011,
        "lon": 15.7075
    }
]


edges = [
    # ZG
    {
        "from": "ZG",
        "to": "ZR",
        "czas": 43,
        "km": 44.9,
        "droga": "DK27",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "ZG",
        "to": "ZR",
        "czas": 49,
        "km": 48.7,
        "droga": "DK32 + DK27",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "ZG",
        "to": "ZA",
        "czas": 46,
        "km": 46.2,
        "droga": "DK27 + DW295",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 3
    },
    {
        "from": "ZG",
        "to": "ZA",
        "czas": 56,
        "km": 58.2,
        "droga": "S3 + DW296",
        "predkoscMax": 120,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },
    {
        "from": "ZG",
        "to": "SZP",
        "czas": 52,
        "km": 53.6,
        "droga": "S3 + DW297",
        "predkoscMax": 120,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },
    {
        "from": "ZG",
        "to": "SZP",
        "czas": 54,
        "km": 58.1,
        "droga": "S3",
        "predkoscMax": 120,
        "natezenieRuchu": 4,
        "jakoscDrogi": 5
    },
    {
        "from": "ZG",
        "to": "SZP",
        "czas": 51,
        "km": 51.6,
        "droga": "DW283 + DW297",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "ZG",
        "to": "KOZ",
        "czas": 30,
        "km": 32,
        "droga": "S3 + DW297",
        "predkoscMax": 120,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },
    {
        "from": "ZG",
        "to": "KOZ",
        "czas": 31,
        "km": 36.1,
        "droga": "S3",
        "predkoscMax": 120,
        "natezenieRuchu": 4,
        "jakoscDrogi": 5
    },
    {
        "from": "ZG",
        "to": "KOZ",
        "czas": 35,
        "km": 28.2,
        "droga": "DW283",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "ZG",
        "to": "NB",
        "czas": 25,
        "km": 25.5,
        "droga": "DW282 + DK27",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 3
    },
    {
        "from": "ZG",
        "to": "NS",
        "czas": 22,
        "km": 26.6,
        "droga": "S3",
        "predkoscMax": 120,
        "natezenieRuchu": 5,
        "jakoscDrogi": 5
    },
    {
        "from": "ZG",
        "to": "NS",
        "czas": 22,
        "km": 23.2,
        "droga": "S3 + Zielonogórska",
        "predkoscMax": 120,
        "natezenieRuchu": 5,
        "jakoscDrogi": 4
    },

    # NB
    {
        "from": "NB",
        "to": "SZP",
        "czas": 41,
        "km": 40.1,
        "droga": "DW295 + DK12",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 3
    },
    {
        "from": "NB",
        "to": "ZR",
        "czas": 20,
        "km": 19.9,
        "droga": "DK27",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "NB",
        "to": "ZR",
        "czas": 23,
        "km": 21.6,
        "droga": "DK27 + Obwodnica",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "NB",
        "to": "ZA",
        "czas": 24,
        "km": 23.1,
        "droga": "DW295",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "NB",
        "to": "ZA",
        "czas": 31,
        "km": 33.1,
        "droga": "DK27 + DK12",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "NB",
        "to": "KOZ",
        "czas": 32,
        "km": 31.4,
        "droga": "DW290",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "NB",
        "to": "NS",
        "czas": 44,
        "km": 39.9,
        "droga": "DW290",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "NB",
        "to": "NS",
        "czas": 41,
        "km": 54.4,
        "droga": "DK27 + S3",
        "predkoscMax": 120,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },

    # ZR
    {
        "from": "ZR",
        "to": "ZA",
        "czas": 16,
        "km": 15.1,
        "droga": "DK12",
        "predkoscMax": 90,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },
    {
        "from": "ZR",
        "to": "ZA",
        "czas": 20,
        "km": 18.3,
        "droga": "Obwodnica + DK12",
        "predkoscMax": 90,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },
    {
        "from": "ZR",
        "to": "SZP",
        "czas": 32,
        "km": 32.2,
        "droga": "DK12",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "ZR",
        "to": "KOZ",
        "czas": 40,
        "km": 40.7,
        "droga": "DK12 + DW296",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 3
    },
    {
        "from": "ZR",
        "to": "NS",
        "czas": 55,
        "km": 52.4,
        "droga": "DW296",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },

    # ZA
    {
        "from": "ZA",
        "to": "SZP",
        "czas": 17,
        "km": 17.6,
        "droga": "DK12",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "ZA",
        "to": "KOZ",
        "czas": 25,
        "km": 26.1,
        "droga": "DW296",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "ZA",
        "to": "NS",
        "czas": 39,
        "km": 37.9,
        "droga": "DW296",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },

    # SZP
    {
        "from": "SZP",
        "to": "KOZ",
        "czas": 22,
        "km": 22.6,
        "droga": "DW297",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "SZP",
        "to": "NS",
        "czas": 36,
        "km": 34.3,
        "droga": "DW297",
        "predkoscMax": 90,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },

    # KOZ
    {
        "from": "KOZ",
        "to": "NS",
        "czas": 14,
        "km": 11.7,
        "droga": "DW297",
        "predkoscMax": 90,
        "natezenieRuchu": 3,
        "jakoscDrogi": 3
    },

    # lokalne rozwożenie paczek w miastach
    {
        "from": "ZG",
        "to": "ZG",
        "czas": 35,
        "km": 18,
        "droga": "Lokalne rozwożenie paczek - Zielona Góra",
        "predkoscMax": 50,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    },
    {
        "from": "NB",
        "to": "NB",
        "czas": 18,
        "km": 8,
        "droga": "Lokalne rozwożenie paczek - Nowogród Bobrzański",
        "predkoscMax": 50,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "ZR",
        "to": "ZR",
        "czas": 28,
        "km": 13,
        "droga": "Lokalne rozwożenie paczek - Żary",
        "predkoscMax": 50,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "ZA",
        "to": "ZA",
        "czas": 24,
        "km": 11,
        "droga": "Lokalne rozwożenie paczek - Żagań",
        "predkoscMax": 50,
        "natezenieRuchu": 3,
        "jakoscDrogi": 4
    },
    {
        "from": "SZP",
        "to": "SZP",
        "czas": 20,
        "km": 9,
        "droga": "Lokalne rozwożenie paczek - Szprotawa",
        "predkoscMax": 50,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "KOZ",
        "to": "KOZ",
        "czas": 17,
        "km": 7,
        "droga": "Lokalne rozwożenie paczek - Kożuchów",
        "predkoscMax": 50,
        "natezenieRuchu": 2,
        "jakoscDrogi": 3
    },
    {
        "from": "NS",
        "to": "NS",
        "czas": 30,
        "km": 14,
        "droga": "Lokalne rozwożenie paczek - Nowa Sól",
        "predkoscMax": 50,
        "natezenieRuchu": 4,
        "jakoscDrogi": 4
    }
]
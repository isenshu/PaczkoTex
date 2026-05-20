import math


def oblicz_parametry_odcinka(dystans_km, predkosc_max_kmh, natezenie_ruchu_1_5, jakosc_drogi_1_5, waga_calkowita_kg):
    natezenie_norm = (natezenie_ruchu_1_5 - 1) / 4.0
    jakosc_norm = (jakosc_drogi_1_5 - 1) / 4.0

    if predkosc_max_kmh >= 120:
        v_pusta = 95.0
    elif predkosc_max_kmh >= 90:
        v_pusta = 65.0
    else:
        v_pusta = 35.0

    predkosc_realna_kmh = v_pusta * (1.0 - 0.6 * natezenie_norm)
    if predkosc_realna_kmh < 5.0:
        predkosc_realna_kmh = 5.0

    czas_minuty = (dystans_km / predkosc_realna_kmh) * 60.0

    G = 9.81
    FR = 0.015
    RHO = 1.2
    CD = 0.33
    A = 3.65

    SPRAWNOSC_SILNIKA = 0.31
    ENERGETYCZNOSC_ON = 36.9

    v = predkosc_realna_kmh / 3.6
    t = czas_minuty * 60.0

    f_toczenia = waga_calkowita_kg * G * FR
    f_powietrza = 0.5 * RHO * CD * A * (v ** 2)
    f_total = f_toczenia + f_powietrza

    moc_wat = f_total * v
    energia_dzule = moc_wat * t
    energia_mj = energia_dzule / 1_000_000.0

    spalanie_bazowe = energia_mj / (SPRAWNOSC_SILNIKA * ENERGETYCZNOSC_ON)

    k_ruchu = 1.0 + 1.4 * (natezenie_norm ** 2)
    k_drogi = 1.0 + 0.25 * jakosc_norm

    spalanie_koncowe = spalanie_bazowe * k_ruchu * k_drogi
    spalanie_100km = (spalanie_koncowe / dystans_km) * 100.0 if dystans_km > 0 else 0.0

    return {
        'spalanie_litry': round(spalanie_koncowe, 3),
        'spalanie_na_100km': round(spalanie_100km, 2),
        'czas_minuty': round(czas_minuty, 2),
        'predkosc_srednia_kmh': round(predkosc_realna_kmh, 1)
    }


class MenedzerTrasLogistycznych:
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges

    def _pobierz_wszystkie_warianty(self, punkt_a, punkt_b, waga_pojazdu_kg):
        warianty = []
        for edge in self.edges:
            if (edge['from'] == punkt_a and edge['to'] == punkt_b) or (
                    edge['from'] == punkt_b and edge['to'] == punkt_a):
                res = oblicz_parametry_odcinka(
                    dystans_km=edge['km'],
                    predkosc_max_kmh=edge['predkoscMax'],
                    natezenie_ruchu_1_5=edge['natezenieRuchu'],
                    jakosc_drogi_1_5=edge['jakoscDrogi'],
                    waga_calkowita_kg=waga_pojazdu_kg
                )
                warianty.append({
                    'droga': edge['droga'],
                    'dystans_km': edge['km'],
                    'czas_minuty': res['czas_minuty'],
                    'spalanie_litry': res['spalanie_litry'],
                    'spalanie_na_100km': res['spalanie_na_100km'],
                    'predkosc_realna': res['predkosc_srednia_kmh']
                })
        return warianty

    def _wybierz_najlepsza_droge(self, warianty, kryterium):
        if not warianty:
            return None
        if kryterium == 'dystans':
            return min(warianty, key=lambda x: x['dystans_km'])
        elif kryterium == 'czas':
            return min(warianty, key=lambda x: x['czas_minuty'])
        else:  # 'spalanie'
            return min(warianty, key=lambda x: x['spalanie_litry'])

    def symuluj_flote(self, start, cel, lista_kierowcow, waga_startowa_kg, waga_lokalnie_kg):
        raport_floty = {}

        # Renault Master L2H2: masa własna pusta bez ładunku
        WAGA_NA_PUSTO_KG = 2431.0

        opcje_tam = self._pobierz_wszystkie_warianty(start, cel, waga_startowa_kg)
        opcje_lokalne = self._pobierz_wszystkie_warianty(cel, cel, waga_lokalnie_kg)
        opcje_powrot = self._pobierz_wszystkie_warianty(cel, start, WAGA_NA_PUSTO_KG)

        for kierowca in lista_kierowcow:
            id_kierowcy = kierowca['id']
            kryterium = kierowca['kryterium']

            droga_tam = self._wybierz_najlepsza_droge(opcje_tam, kryterium)
            droga_lokalna = self._wybierz_najlepsza_droge(opcje_lokalne, kryterium)
            droga_powrot = self._wybierz_najlepsza_droge(opcje_powrot, kryterium)

            if droga_tam and droga_powrot and droga_lokalna:
                calkowity_dystans = droga_tam['dystans_km'] + droga_lokalna['dystans_km'] + droga_powrot['dystans_km']
                calkowity_czas = droga_tam['czas_minuty'] + droga_lokalna['czas_minuty'] + droga_powrot['czas_minuty']
                calkowite_spalanie = droga_tam['spalanie_litry'] + droga_lokalna['spalanie_litry'] + droga_powrot[
                    'spalanie_litry']
                srednie_spalanie_100 = (calkowite_spalanie / calkowity_dystans) * 100

                raport_floty[id_kierowcy] = {
                    'kryterium': kryterium,
                    'tam': droga_tam,
                    'rozładunek_lokalny': droga_lokalna,
                    'powrot': droga_powrot,
                    'podsumowanie': {
                        'waga_trasy_tam_kg': waga_startowa_kg,
                        'waga_lokalna_z_algorytmu_kg': waga_lokalnie_kg,
                        'waga_powrotna_kg': WAGA_NA_PUSTO_KG,
                        'laczny_dystans_km': round(calkowity_dystans, 2),
                        'laczny_czas_min': round(calkowity_czas, 2),
                        'laczne_spalanie_litry': round(calkowite_spalanie, 3),
                        'srednie_spalanie_100km': round(srednie_spalanie_100, 2)
                    }
                }
        return raport_floty


# --- TWOJA BAZA DANYCH GRAFU ---
points = [
    {"id": "ZG", "name": "Zielona Góra", "lat": 51.9354800, "lon": 15.5064300},
    {"id": "NB", "name": "Nowogród Bobrzański", "lat": 51.798346, "lon": 15.236140},
    {"id": "ZR", "name": "Żary", "lat": 51.636, "lon": 15.138},
    {"id": "ZA", "name": "Żagań", "lat": 51.616591, "lon": 15.317660},
    {"id": "SZP", "name": "Szprotawa", "lat": 51.567, "lon": 15.538},
    {"id": "KOZ", "name": "Kożuchów", "lat": 51.745, "lon": 15.595},
    {"id": "NS", "name": "Nowa Sól", "lat": 51.8011, "lon": 15.7075}
]

edges = [
    # ZG
    {"from": "ZG", "to": "ZR", "km": 44.9, "droga": "DK27", "predkoscMax": 90, "natezenieRuchu": 3, "jakoscDrogi": 4},
    {"from": "ZG", "to": "ZR", "km": 48.7, "droga": "DK32 + DK27", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 4},
    {"from": "ZG", "to": "ZA", "km": 46.2, "droga": "DK27 + DW295", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 3},
    {"from": "ZG", "to": "ZA", "km": 58.2, "droga": "S3 + DW296", "predkoscMax": 120, "natezenieRuchu": 4,
     "jakoscDrogi": 4},
    {"from": "ZG", "to": "SZP", "km": 53.6, "droga": "S3 + DW297", "predkoscMax": 120, "natezenieRuchu": 4,
     "jakoscDrogi": 4},
    {"from": "ZG", "to": "SZP", "km": 58.1, "droga": "S3", "predkoscMax": 120, "natezenieRuchu": 4, "jakoscDrogi": 5},
    {"from": "ZG", "to": "SZP", "km": 51.6, "droga": "DW283 + DW297", "predkoscMax": 90, "natezenieRuchu": 2,
     "jakoscDrogi": 3},
    {"from": "ZG", "to": "KOZ", "km": 32.0, "droga": "S3 + DW297", "predkoscMax": 120, "natezenieRuchu": 4,
     "jakoscDrogi": 4},
    {"from": "ZG", "to": "KOZ", "km": 36.1, "droga": "S3", "predkoscMax": 120, "natezenieRuchu": 4, "jakoscDrogi": 5},
    {"from": "ZG", "to": "KOZ", "km": 28.2, "droga": "DW283", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},
    {"from": "ZG", "to": "NB", "km": 25.5, "droga": "DW282 + DK27", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 3},
    {"from": "ZG", "to": "NS", "km": 26.6, "droga": "S3", "predkoscMax": 120, "natezenieRuchu": 5, "jakoscDrogi": 5},
    {"from": "ZG", "to": "NS", "km": 23.2, "droga": "S3 + Zielonogórska", "predkoscMax": 120, "natezenieRuchu": 5,
     "jakoscDrogi": 4},

    # NB
    {"from": "NB", "to": "SZP", "km": 40.1, "droga": "DW295 + DK12", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 3},
    {"from": "NB", "to": "ZR", "km": 19.9, "droga": "DK27", "predkoscMax": 90, "natezenieRuchu": 3, "jakoscDrogi": 4},
    {"from": "NB", "to": "ZR", "km": 21.6, "droga": "DK27 + Obwodnica", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 4},
    {"from": "NB", "to": "ZA", "km": 23.1, "droga": "DW295", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},
    {"from": "NB", "to": "ZA", "km": 33.1, "droga": "DK27 + DK12", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 4},
    {"from": "NB", "to": "KOZ", "km": 31.4, "droga": "DW290", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},
    {"from": "NB", "to": "NS", "km": 39.9, "droga": "DW290", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},
    {"from": "NB", "to": "NS", "km": 54.4, "droga": "DK27 + S3", "predkoscMax": 120, "natezenieRuchu": 4,
     "jakoscDrogi": 4},

    # ZR
    {"from": "ZR", "to": "ZA", "km": 15.1, "droga": "DK12", "predkoscMax": 90, "natezenieRuchu": 4, "jakoscDrogi": 4},
    {"from": "ZR", "to": "ZA", "km": 18.3, "droga": "Obwodnica + DK12", "predkoscMax": 90, "natezenieRuchu": 4,
     "jakoscDrogi": 4},
    {"from": "ZR", "to": "SZP", "km": 32.2, "droga": "DK12", "predkoscMax": 90, "natezenieRuchu": 3, "jakoscDrogi": 4},
    {"from": "ZR", "to": "KOZ", "km": 40.7, "droga": "DK12 + DW296", "predkoscMax": 90, "natezenieRuchu": 3,
     "jakoscDrogi": 3},
    {"from": "ZR", "to": "NS", "km": 52.4, "droga": "DW296", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},

    # ZA
    {"from": "ZA", "to": "SZP", "km": 17.6, "droga": "DK12", "predkoscMax": 90, "natezenieRuchu": 3, "jakoscDrogi": 4},
    {"from": "ZA", "to": "KOZ", "km": 26.1, "droga": "DW296", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},
    {"from": "ZA", "to": "NS", "km": 37.9, "droga": "DW296", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},

    # SZP
    {"from": "SZP", "to": "KOZ", "km": 22.6, "droga": "DW297", "predkoscMax": 90, "natezenieRuchu": 2,
     "jakoscDrogi": 3},
    {"from": "SZP", "to": "NS", "km": 34.3, "droga": "DW297", "predkoscMax": 90, "natezenieRuchu": 2, "jakoscDrogi": 3},

    # KOZ
    {"from": "KOZ", "to": "NS", "km": 11.7, "droga": "DW297", "predkoscMax": 90, "natezenieRuchu": 3, "jakoscDrogi": 3},

    # Pętle lokalne
    {"from": "ZG", "to": "ZG", "km": 18.0, "droga": "Lokalne - Zielona Góra", "predkoscMax": 50, "natezenieRuchu": 4,
     "jakoscDrogi": 4},
    {"from": "NB", "to": "NB", "km": 8.0, "droga": "Lokalne - Nowogród Bobrzański", "predkoscMax": 50,
     "natezenieRuchu": 2, "jakoscDrogi": 3},
    {"from": "ZR", "to": "ZR", "km": 13.0, "droga": "Lokalne - Żary", "predkoscMax": 50, "natezenieRuchu": 3,
     "jakoscDrogi": 4},
    {"from": "ZA", "to": "ZA", "km": 11.0, "droga": "Lokalne - Żagań", "predkoscMax": 50, "natezenieRuchu": 3,
     "jakoscDrogi": 4},
    {"from": "SZP", "to": "SZP", "km": 9.0, "droga": "Lokalne - Szprotawa", "predkoscMax": 50, "natezenieRuchu": 2,
     "jakoscDrogi": 3},
    {"from": "KOZ", "to": "KOZ", "km": 7.0, "droga": "Lokalne - Kożuchów", "predkoscMax": 50, "natezenieRuchu": 2,
     "jakoscDrogi": 3},
    {"from": "NS", "to": "NS", "km": 14.0, "droga": "Lokalne - Nowa Sól", "predkoscMax": 50, "natezenieRuchu": 4,
     "jakoscDrogi": 4}
]

# --- URUCHOMIENIE SYMULACJI ---
menedzer = MenedzerTrasLogistycznych(points, edges)

kierowcy = [
    {"id": "Kierowca_Jan", "kryterium": "spalanie"},
    {"id": "Kierowca_Adam", "kryterium": "czas"}
]

# Symulowane dane wejściowe (w przyszłości pobierane dynamicznie):
waga_z_bazy_kg = 3500.0  # Całkowita masa na trasę dojazdową
waga_wyliczona_z_algorytmu_paczkowego = 2450.0  # Średnia masa wyznaczona przez zewnętrzny moduł dla ruchu lokalnego

wyniki = menedzer.symuluj_flote(
    start='ZG',
    cel='ZR',
    lista_kierowcow=kierowcy,
    waga_startowa_kg=waga_z_bazy_kg,
    waga_lokalnie_kg=waga_wyliczona_z_algorytmu_paczkowego
)

# Raport koncowy
for k_id, dane in wyniki.items():
    print(f"=== KIEROWCA: {k_id} ({dane['kryterium'].upper()}) ===")
    print(
        f" -> Odcinek dojazdowy (waga {dane['podsumowanie']['waga_trasy_tam_kg']} kg): {dane['tam']['droga']} | {dane['tam']['spalanie_litry']} L")
    print(
        f" -> Rozwóz lokalny (waga z alg. paczek {dane['podsumowanie']['waga_lokalna_z_algorytmu_kg']} kg): {dane['rozładunek_lokalny']['droga']} | {dane['rozładunek_lokalny']['spalanie_litry']} L")
    print(
        f" -> Odcinek powrotny (waga {dane['podsumowanie']['waga_powrotna_kg']} kg): {dane['powrot']['droga']} | {dane['powrot']['spalanie_litry']} L")
    p = dane['podsumowanie']
    print(
        f" -> ŁĄCZNIE: {p['laczny_dystans_km']} km | Zużycie: {p['laczne_spalanie_litry']} L | Średnie: {p['sredmie_spalanie_100km'] if 'sredmie_spalanie_100km' in p else p['srednie_spalanie_100km']} l/100km\n")

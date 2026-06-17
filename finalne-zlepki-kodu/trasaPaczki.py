import csv
import os
import math
import random
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict

# =====================================================================
# 1. PARAMETRY WEJŚCIOWE I KONFIGURACJA POJAZDU
# =====================================================================
LIMIT_WAGI_KG = 1069.0
LIMIT_OBJETOSCI_CM3 = 8_100_000.0  # 75% z 10.8 m^3
WAGA_PUSTEGO_VAN_KG = 2431.0
CZAS_ROZLADUNKU_PACZKI_SEC = 15

# NOWE PARAMETRY EFEKTYWNOŚCIOWE:
MAKS_CZAS_ZMIANY_MIN = 480  # 8 godzin zmiany
CZAS_ZALADUNKU_BAZA_MIN = 20  # Kolejne załadunki w ciągu dnia

ID_TO_NAME = {
    "Zielona Góra": "Zielona Góra",
    "Nowogród Bobrzański": "Nowogród Bobrzański",
    "Żary": "Żary",
    "Żagań": "Żagań",
    "Szprotawa": "Szprotawa",
    "Kożuchów": "Kożuchów",
    "Nowa Sól": "Nowa Sól"
}

# =====================================================================
# 2. BAZA INFRASTRUKTURY DROGOWEJ
# =====================================================================
edges = [
    # Zielona Góra -> Żary
    {"from": "Zielona Góra", "to": "Żary", "km": 44.90, "droga": "DK27", "predkoscSrednia": 65, "natezenieRuchu": 0.70,
     "jakoscDrogi": 4},
    {"from": "Zielona Góra", "to": "Żary", "km": 48.70, "droga": "DK32 + DK27", "predkoscSrednia": 65,
     "natezenieRuchu": 0.70, "jakoscDrogi": 4},
    # Zielona Góra -> Żagań
    {"from": "Zielona Góra", "to": "Żagań", "km": 46.20, "droga": "DK27 + DW295", "predkoscSrednia": 65,
     "natezenieRuchu": 0.70, "jakoscDrogi": 3},
    {"from": "Zielona Góra", "to": "Żagań", "km": 58.20, "droga": "S3 + DW296", "predkoscSrednia": 87,
     "natezenieRuchu": 0.80, "jakoscDrogi": 4},
    # Zielona Góra -> Szprotawa
    {"from": "Zielona Góra", "to": "Szprotawa", "km": 53.60, "droga": "S3 + DW297", "predkoscSrednia": 87,
     "natezenieRuchu": 0.80, "jakoscDrogi": 4},
    {"from": "Zielona Góra", "to": "Szprotawa", "km": 58.10, "droga": "S3", "predkoscSrednia": 87,
     "natezenieRuchu": 0.80, "jakoscDrogi": 5},
    {"from": "Zielona Góra", "to": "Szprotawa", "km": 51.60, "droga": "DW283 + DW297", "predkoscSrednia": 65,
     "natezenieRuchu": 0.60, "jakoscDrogi": 3},
    # Zielona Góra -> Kożuchów
    {"from": "Zielona Góra", "to": "Kożuchów", "km": 32.00, "droga": "S3 + DW297", "predkoscSrednia": 87,
     "natezenieRuchu": 0.80, "jakoscDrogi": 4},
    {"from": "Zielona Góra", "to": "Kożuchów", "km": 36.10, "droga": "S3", "predkoscSrednia": 87,
     "natezenieRuchu": 0.80, "jakoscDrogi": 5},
    {"from": "Zielona Góra", "to": "Kożuchów", "km": 28.20, "droga": "DW283", "predkoscSrednia": 65,
     "natezenieRuchu": 0.60, "jakoscDrogi": 3},
    # Zielona Góra -> Nowogród Bobrzański
    {"from": "Zielona Góra", "to": "Nowogród Bobrzański", "km": 25.50, "droga": "DW282 + DK27", "predkoscSrednia": 65,
     "natezenieRuchu": 0.70, "jakoscDrogi": 3},
    # Zielona Góra -> Nowa Sól
    {"from": "Zielona Góra", "to": "Nowa Sól", "km": 26.60, "droga": "S3", "predkoscSrednia": 87,
     "natezenieRuchu": 0.90, "jakoscDrogi": 5},
    {"from": "Zielona Góra", "to": "Nowa Sól", "km": 23.20, "droga": "S3 + Zielonogórska", "predkoscSrednia": 87,
     "natezenieRuchu": 0.90, "jakoscDrogi": 4},

    # Cykle wewnętrzne
    {"from": "Zielona Góra", "to": "Zielona Góra", "km": 18.00, "droga": "Rozwóz miejski - Zielona Góra",
     "predkoscSrednia": 36, "natezenieRuchu": 0.65, "jakoscDrogi": 4},
    {"from": "Nowogród Bobrzański", "to": "Nowogród Bobrzański", "km": 8.00,
     "droga": "Rozwóz miejski - Nowogród Bobrzański", "predkoscSrednia": 36, "natezenieRuchu": 0.50, "jakoscDrogi": 3},
    {"from": "Żary", "to": "Żary", "km": 13.00, "droga": "Rozwóz miejski - Żary", "predkoscSrednia": 36,
     "natezenieRuchu": 0.55, "jakoscDrogi": 4},
    {"from": "Żagań", "to": "Żagań", "km": 11.00, "droga": "Rozwóz miejski - Żagań", "predkoscSrednia": 36,
     "natezenieRuchu": 0.55, "jakoscDrogi": 4},
    {"from": "Szprotawa", "to": "Szprotawa", "km": 9.00, "droga": "Rozwóz miejski - Szprotawa", "predkoscSrednia": 36,
     "natezenieRuchu": 0.50, "jakoscDrogi": 3},
    {"from": "Kożuchów", "to": "Kożuchów", "km": 7.00, "droga": "Rozwóz miejski - Kożuchów", "predkoscSrednia": 36,
     "natezenieRuchu": 0.50, "jakoscDrogi": 3},
    {"from": "Nowa Sól", "to": "Nowa Sól", "km": 14.00, "droga": "Rozwóz miejski - Nowa Sól", "predkoscSrednia": 36,
     "natezenieRuchu": 0.65, "jakoscDrogi": 4}
]

for edge in edges:
    eff_speed = edge["predkoscSrednia"] * edge["natezenieRuchu"]
    edge["czas"] = round(edge["km"] / eff_speed * 60, 1)


# =====================================================================
# 3. FIZYKA SPALANIA
# =====================================================================
def oblicz_spalanie_fizyczne(edge, waga_pojazdu_kg):
    effective_speed_mps = (edge["predkoscSrednia"] * edge["natezenieRuchu"]) / 3.6
    czas_sekundy = (edge["km"] / (edge["predkoscSrednia"] * edge["natezenieRuchu"])) * 3600
    G, FR, RHO, CD, A = 9.81, 0.015, 1.2, 0.33, 3.65
    f_toczenia = waga_pojazdu_kg * G * FR
    f_powietrza = 0.5 * RHO * CD * A * (effective_speed_mps ** 2)
    moc = (f_toczenia + f_powietrza) * effective_speed_mps
    energia_mj = (moc * czas_sekundy) / 1_000_000.0
    spalanie_litry = energia_mj / (0.31 * 36.9)
    spalanie_litry *= (1.0 + (5 - edge["jakoscDrogi"]) * 0.05)
    return round(spalanie_litry, 3)


# =====================================================================
# 4. PARSER PLIKU CSV Z PACZKAMI
# =====================================================================
def wczytaj_najnowszy_plik_csv():
    root = tk.Tk()
    root.withdraw()
    sciezka = filedialog.askopenfilename(
        title="Wybierz plik CSV z paczkami",
        filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
    )
    if sciezka:
        print(f"[V] Pomyślnie podpięto zewnętrzną bazę danych: {sciezka}\n")
        return sciezka
    else:
        print("[!] Anulowano wybór pliku CSV.")
        return None


def pakuj_busy(sciezka_csv):
    dane_pogrupowane = defaultdict(lambda: defaultdict(list))
    with open(sciezka_csv, mode='r', encoding='utf-8') as plik:
        reader = csv.DictReader(plik)
        for wiersz in reader:
            dane_pogrupowane[wiersz['data_dostawy']][wiersz['miasto_docelowe']].append(wiersz)

    raport_tygodniowy = {}
    for data, miasta in dane_pogrupowane.items():
        raport_tygodniowy[data] = {}
        for miasto, paczki in miasta.items():
            paczki.sort(key=lambda p: p['id_paczkomatu'])
            busy = []
            aktualny_bus = {'waga': 0.0, 'objetosc': 0.0, 'id_paczkomatow': set(), 'liczba_paczek': 0}
            licznik_paczek = 0

            for paczka in paczki:
                waga = float(paczka['waga_kg'])
                objetosc = float(paczka['wysokosc_cm']) * float(paczka['szerokosc_cm']) * float(paczka['dlugosc_cm'])

                if (aktualny_bus['waga'] + waga <= LIMIT_WAGI_KG) and (
                        aktualny_bus['objetosc'] + objetosc <= LIMIT_OBJETOSCI_CM3):
                    aktualny_bus['waga'] += waga
                    aktualny_bus['objetosc'] += objetosc
                    aktualny_bus['id_paczkomatow'].add(paczka['id_paczkomatu'])
                    licznik_paczek += 1
                else:
                    aktualny_bus['liczba_paczek'] = licznik_paczek
                    busy.append(aktualny_bus)
                    aktualny_bus = {'waga': waga, 'objetosc': objetosc, 'id_paczkomatow': {paczka['id_paczkomatu']},
                                    'liczba_paczek': 1}
                    licznik_paczek = 1

            if licznik_paczek > 0:
                aktualny_bus['liczba_paczek'] = licznik_paczek
                busy.append(aktualny_bus)
            raport_tygodniowy[data][miasto] = busy
    return raport_tygodniowy


# =====================================================================
# 5. KALKULATOR POJEDYNCZEJ TRASY (Z KONTROLĄ KOLEJNOŚCI WYJAZDU)
# =====================================================================
def oblicz_parametry_trasy(cel_miasto, dane_busa, kryterium, czy_pierwsza_trasa):
    trasa_miejska = next((e for e in edges if e['from'] == cel_miasto and e['to'] == cel_miasto), None)
    waga_zaladowanego = WAGA_PUSTEGO_VAN_KG + dane_busa['waga']
    czas_rozladunku_min = round((dane_busa['liczba_paczek'] * CZAS_ROZLADUNKU_PACZKI_SEC) / 60.0, 2)

    # Koszt czasowy załadunku: 0 minut rano, 20 minut na każdy kolejny kurs
    czas_zaladunku = 0 if czy_pierwsza_trasa else CZAS_ZALADUNKU_BAZA_MIN

    if cel_miasto == "Zielona Góra":
        paliwo_miasto = oblicz_spalanie_fizyczne(trasa_miejska, waga_zaladowanego)
        czas_miejski = trasa_miejska['czas'] + czas_rozladunku_min + czas_zaladunku + round(random.uniform(-1, 1), 2)
        return {"droga": "Ulice Zielonej Góry", "dystans": trasa_miejska['km'], "czas": round(czas_miejski, 2),
                "paliwo": round(paliwo_miasto, 2), "zaladunek_min": czas_zaladunku}

    opcje_dojazdu = [e for e in edges if e['from'] == "Zielona Góra" and e['to'] == cel_miasto]
    wybrana_krajowka = min(opcje_dojazdu, key=lambda x: x['czas']) if kryterium == 'czas' else min(opcje_dojazdu,
                                                                                                   key=lambda x: x[
                                                                                                       'km'])

    paliwo_tam = oblicz_spalanie_fizyczne(wybrana_krajowka, waga_zaladowanego)
    czas_tam = wybrana_krajowka['czas'] + random.uniform(-1, 1)

    paliwo_miasto = oblicz_spalanie_fizyczne(trasa_miejska, waga_zaladowanego)
    czas_miasto = trasa_miejska['czas'] + czas_rozladunku_min + random.uniform(-1, 1)

    paliwo_powrot = oblicz_spalanie_fizyczne(wybrana_krajowka, WAGA_PUSTEGO_VAN_KG)
    czas_powrot = wybrana_krajowka['czas'] + random.uniform(-1, 1)

    dystans_total = (wybrana_krajowka['km'] * 2) + trasa_miejska['km']
    paliwo_total = paliwo_tam + paliwo_miasto + paliwo_powrot
    czas_total = czas_tam + czas_miasto + czas_powrot + czas_zaladunku

    return {"droga": wybrana_krajowka['droga'], "dystans": round(dystans_total, 2), "czas": round(czas_total, 2),
            "paliwo": round(paliwo_total, 2), "zaladunek_min": czas_zaladunku}


# =====================================================================
# 6. NOWY LOGICZNY SILNIK MULTI-TRIP (ŁĄCZENIE TRAS DLA JEDNEGO ETATU)
# =====================================================================
def optymalizuj_przydzial_kierowcow(lista_busow, cel_miasto, kryterium):
    # Kopia listy busów (paczek spakowanych w pule) do obsłużenia
    pule_do_obsługi = lista_busow.copy()
    baza_kierowcow = []

    while pule_do_obsługi:
        # Tworzymy nowego kierowcę, bo poprzedni skończyli zmiany lub to początek dnia
        kierowca_id = len(baza_kierowcow) + 1
        dane_kierowcy = {
            "id": kierowca_id,
            "czas_pracy_suma": 0.0,
            "dystans_suma": 0.0,
            "paliwo_suma": 0.0,
            "obsugiwane_trasy": []
        }

        while pule_do_obsługi:
            nastepny_bus = pule_do_obsługi[0]
            czy_pierwszy = len(dane_kierowcy["obsugiwane_trasy"]) == 0

            # Próba kalkulacji symulacji trasy dla tego busa
            wynik_trasy = oblicz_parametry_trasy(cel_miasto, nastepny_bus, kryterium, czy_pierwsza_trasa=czy_pierwszy)

            # Sprawdzamy czy zmieści się w 8 godzinach zmiany
            if dane_kierowcy["czas_pracy_suma"] + wynik_trasy["czas"] <= MAKS_CZAS_ZMIANY_MIN:
                # Kierowca bierze tę robotę!
                dane_kierowcy["czas_pracy_suma"] += wynik_trasy["czas"]
                dane_kierowcy["dystans_suma"] += wynik_trasy["dystans"]
                dane_kierowcy["paliwo_suma"] += wynik_trasy["paliwo"]
                dane_kierowcy["obsugiwane_trasy"].append({
                    "bus_dane": nastepny_bus,
                    "trasa_szczegoly": wynik_trasy
                })
                # Usuwamy zapakowany ładunek z kolejki do obsłużenia
                pule_do_obsługi.pop(0)
            else:
                # Ta trasa wykracza poza 8h tego pracownika – zamykamy jego dzień pracy
                break

        baza_kierowcow.append(dane_kierowcy)

    return baza_kierowcow


# =====================================================================
# 7. INTERFEJS TERMINALA Z WYLICZENIAMI EFEKTYWNOŚCIOWYMI
# =====================================================================
def uruchom_interfejs(raport):
    while True:
        print("\n" + "=" * 60)
        print("    SYSTEM MAKSYMALIZACJI EFEKTYWNOŚCI KURIERÓW (MULTI-TRIP)")
        print("=" * 60)

        daty = sorted(list(raport.keys()))
        print(" [KROK 1] Wybierz datę dostawy z pliku:")
        for idx, data in enumerate(daty, 1):
            print(f"  [{idx}] Data: {data}")
        print("  [X] Zakończ program")
        print("-" * 60)

        wybor_daty = input("Wpisz numer: ").strip()
        if wybor_daty.upper() == 'X':
            break

        if not wybor_daty.isdigit() or int(wybor_daty) < 1 or int(wybor_daty) > len(daty):
            print("[!] Błąd wyboru daty.")
            continue

        data_wybrana = daty[int(wybor_daty) - 1]

        miasta_dnia = sorted(list(raport[data_wybrana].keys()))
        print(f"\n [KROK 2] Kierunki w dniu {data_wybrana}:")
        for idx, miasto in enumerate(miasta_dnia, 1):
            print(f"  [{idx}] {miasto:<22} | Łączna pula busów towaru: {len(raport[data_wybrana][miasto])}")
        print("-" * 60)

        wybor_miasta = input("Wybierz numer celu: ").strip()
        if not wybor_miasta.isdigit() or int(wybor_miasta) < 1 or int(wybor_miasta) > len(miasta_dnia):
            print("[!] Błąd wyboru miasta.")
            continue

        miasto_wybrane = miasta_dnia[int(wybor_miasta) - 1]

        kryterium = 'czas'
        if miasto_wybrane != "Zielona Góra":
            print("\n [KROK 3] Wybierz kryterium trasy:")
            print("  [1] Najkrótszy CZAS dojazdu")
            print("  [2] Najkrótszy DYSTANS")
            wybor_kryterium = input("Wybór [1/2]: ").strip()
            if wybor_kryterium == '2':
                kryterium = 'dystans'

        lista_busow = raport[data_wybrana][miasto_wybrane]

        # URUCHOMIENIE SILNIKA OPTYMALIZACYJNEGO MULTI-TRIP
        wyniki_kierowcow = optymalizuj_przydzial_kierowcow(lista_busow, miasto_wybrane, kryterium)

        print("\n" + "═" * 60)
        print(f" OPERACYJNY RAPORT OPTYMALIZACJI ZATRUDNIENIA - INTERWAŁ: {data_wybrana}")
        print(f" REJON DOSTAWY: {miasto_wybrane.upper()}")
        print("═" * 60)

        for k in wyniki_kierowcow:
            print(f" 👤 KIEROWCA NR {k['id']}:")
            print(
                f"   ➔ Łączny czas pracy na zmianie: {k['czas_pracy_suma']:.1f} min ({round(k['czas_pracy_suma'] / 60, 2)}h / 8.0h)")
            print(f"   ➔ Wykonane pętle (trasy)     : {len(k['obsugiwane_trasy'])}")
            print(f"   ➔ Sumaryczny dystans dzienny : {k['dystans_suma']:.2f} km")
            print(f"   ➔ Zużyte paliwo (ON)         : {k['paliwo_suma']:.2f} L")

            # Wylistowanie szczegółów tras danego kierowcy
            for t_idx, trasa in enumerate(k['obsugiwane_trasy'], 1):
                b_dane = trasa["bus_dane"]
                t_szczegoly = trasa["trasa_szczegoly"]
                status_zaladunku = "Poranny (Towar w aucie, 0 min)" if t_szczegoly[
                                                                           'zaladunek_min'] == 0 else f"Powrotny (+{t_szczegoly['zaladunek_min']} min załadunek)"

                print(
                    f"     [Wyjazd {t_idx}]: Paczek: {b_dane['liczba_paczek']} szt. | Masa: {b_dane['waga']:.1f}kg | Czas pętli: {t_szczegoly['czas']} min ({status_zaladunku})")
            print("-" * 60)

        print("\n" + "📊 PORÓWNANIE WSKAŹNIKÓW EFEKTYWNOŚCIOWYCH (KPI):")
        print(f" ➔ Liczba busów z towarem z pliku CSV       : {len(lista_busow)}")
        print(f" ➔ WYMAGANA LICZBA KIEROWCÓW PO OPTYMALIZACJI: {len(wyniki_kierowcow)}")
        oszczedzeni_ludzie = len(lista_busow) - len(wyniki_kierowcow)
        print(
            f" ➔ Zredukowana liczba etatów/samochodów     : [ {oszczedzeni_ludzie} ] o tyle zmniejszyłeś zatrudnienie!")
        print("═" * 60)

        input("\nNaciśnij [ENTER], aby wrócić do menu...")


if __name__ == "__main__":
    plik_danych = wczytaj_najnowszy_plik_csv()
    if plik_danych:
        baza_zaladunkowa = pakuj_busy(plik_danych)
        uruchom_interfejs(baza_zaladunkowa)
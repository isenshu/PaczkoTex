import csv
import random
import uuid
import os
from datetime import datetime

# --- TWOJA LISTA PACZKOMATÓW ---
PACZKOMATY_ZGO = [
    {"kod": "ZGO02L", "ulica": "ul. Konstytucji 3 Maja 23"},
    {"kod": "ZGO19M", "ulica": "ul.Dworcowa 27"},
    {"kod": "ZGO09M", "ulica": "ul. Staszica 5"},
    {"kod": "ZGO36M", "ulica": "ul. Łużycka 18"},
    {"kod": "ZGO03N", "ulica": "ul. Wyszyńskiego 22A"},
    {"kod": "ZGO01APP", "ulica": "ul. Zawadzkiego 'Zośki' 14"},
    {"kod": "ZGO08A", "ulica": "ul. Kożuchowska 10"},
    {"kod": "ZGO77M", "ulica": "ul. Harcerska 9"},
    {"kod": "ZGO04M", "ulica": "ul. Urszuli 1"},
    {"kod": "ZGO11N", "ulica": "ul. Truskawkowa 1B"},
    {"kod": "ZGO14M", "ulica": "ul. Głogowska 85"},
    {"kod": "ZGO67M", "ulica": "ul. osiedle Kaszubskie 3"},
    {"kod": "ZGO07A", "ulica": "ul. Pionierów Lubuskich 72"},
    {"kod": "ZGO15M", "ulica": "ul. Nowy Kisielin - Odrzańska 51a"},
    {"kod": "ZGO52M", "ulica": "ul. Jędrzychowska 46"},
    {"kod": "ZGO13N", "ulica": "ul. Kożuchowska 30"},
    {"kod": "ZGO24M", "ulica": "ul. Turystyczna 1 A"},
    {"kod": "ZGO82M", "ulica": "ul. Geologów 2"},
    {"kod": "ZGO07BAPP", "ulica": "ul. Batorego 118 C"},
    {"kod": "ZGO07M", "ulica": "ul. Aleja Zjednoczenia 118"},
    {"kod": "ZGO04N", "ulica": "ul. Stefana Batorego 81"},
    {"kod": "ZGO41M", "ulica": "ul. Lwowska 2"},
    {"kod": "ZGO40M", "ulica": "ul. Lisia 63"},
    {"kod": "ZGO04L", "ulica": "ul. Wojska Polskiego 106"},
    {"kod": "ZGO01H", "ulica": "ul. Agrestowa 5A/11"},
    {"kod": "ZGO66M", "ulica": "ul. Konicza 34"}
]

# --- KONFIGURACJA ---
WYBRANA_DATA_STR = "2026-05-01"
BAZOWA_LICZBA_PACZEK = 300

GABARYTY = {
    'A': {'wymiary': '8x38x64', 'max_waga': 25, 'prawdopodobienstwo': 0.50, 'zakres_wagi_realnej': (0.1, 5.0)},
    'B': {'wymiary': '19x38x64', 'max_waga': 25, 'prawdopodobienstwo': 0.35, 'zakres_wagi_realnej': (1.0, 10.0)},
    'C': {'wymiary': '41x38x64', 'max_waga': 25, 'prawdopodobienstwo': 0.15, 'zakres_wagi_realnej': (5.0, 25.0)}
}

def generuj_paczke():
    typy = list(GABARYTY.keys())
    wagi = [GABARYTY[t]['prawdopodobienstwo'] for t in typy]
    gabaryt = random.choices(typy, weights=wagi, k=1)[0]
    
    min_waga, max_waga = GABARYTY[gabaryt]['zakres_wagi_realnej']
    waga = round(random.uniform(min_waga, max_waga), 2)
    
    # --- NOWE: Losowanie paczkomatu docelowego ---
    paczkomat = random.choice(PACZKOMATY_ZGO)
    
    return {
        'id_paczki': f"ZG-{uuid.uuid4().hex[:8].upper()}",
        'kod_paczkomatu': paczkomat['kod'],      # Dodane
        # 'adres_paczkomatu': paczkomat['ulica'],  # Dodane
        'gabaryt': gabaryt,
        'wymiary_max_cm': GABARYTY[gabaryt]['wymiary'],
        'waga_kg': waga
    }

def generuj_dzien_pracy(data, baza_paczek):
    dzien_tyg = data.weekday()
    mnoznik = 1.0
    if dzien_tyg == 0: mnoznik = 1.15 
    elif dzien_tyg == 4: mnoznik = 0.90 
    elif dzien_tyg >= 5: return [] 
        
    wariancja = random.uniform(0.9, 1.1)
    liczba_paczek = int(baza_paczek * mnoznik * wariancja)
    
    return [generuj_paczke() for _ in range(liczba_paczek)]

def zapisz_do_csv(paczki, data_obj):
    if not paczki:
        return 0

    folder_skryptu = os.path.dirname(os.path.abspath(__file__))
    nazwa_pliku = f"paczki_{data_obj.strftime('%Y%m%d')}.csv"
    pelna_sciezka = os.path.join(folder_skryptu, nazwa_pliku)
    
    klucze = paczki[0].keys()
    with open(pelna_sciezka, 'w', newline='', encoding='utf-8') as plik_csv:
        writer = csv.DictWriter(plik_csv, fieldnames=klucze)
        writer.writeheader()
        writer.writerows(paczki)
        
    print(f"\n[OK] Zapisano plik: {pelna_sciezka}")
    return len(paczki)

if __name__ == "__main__":
    try:
        data_celu = datetime.strptime(WYBRANA_DATA_STR, "%Y-%m-%d")
    except ValueError:
        print("Błąd: Niepoprawny format daty! Użyj RRRR-MM-DD.")
        exit()

    print(f"Rozpoczynam generowanie danych dla: {WYBRANA_DATA_STR}...")
    paczki_dzis = generuj_dzien_pracy(data_celu, BAZOWA_LICZBA_PACZEK)
    
    if paczki_dzis:
        ile = zapisz_do_csv(paczki_dzis, data_celu)
        
        a_count = sum(1 for p in paczki_dzis if p['gabaryt'] == 'A')
        b_count = sum(1 for p in paczki_dzis if p['gabaryt'] == 'B')
        c_count = sum(1 for p in paczki_dzis if p['gabaryt'] == 'C')
        laczna_waga = sum(p['waga_kg'] for p in paczki_dzis)
        
        print("\n--- PODSUMOWANIE DNIA ---")
        print(f"Data:           {WYBRANA_DATA_STR} ({data_celu.strftime('%A')})")
        print(f"Suma paczek:    {ile} szt.")
        print(f" - Gabaryt A:   {a_count} szt.")
        print(f" - Gabaryt B:   {b_count} szt.")
        print(f" - Gabaryt C:   {c_count} szt.")
        print(f"Łączna waga:    {laczna_waga:.2f} kg")
        print(f"Średnio paczek na automat: {ile/len(PACZKOMATY_ZGO):.1f}")
        print("-------------------------")
    else:
        print(f"\nDzień {WYBRANA_DATA_STR} to weekend. Nie wygenerowano żadnych paczek.")
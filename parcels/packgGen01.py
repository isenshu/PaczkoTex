import csv
import random
import uuid
import os
from datetime import datetime

# --- KONFIGURACJA ---
# Tutaj zmień datę, dla której chcesz wygenerować paczki (format RRRR-MM-DD)
WYBRANA_DATA_STR = "2026-05-1"  # <--- Zmień to na dowolny dzień roboczy
BAZOWA_LICZBA_PACZEK = 300

# Konfiguracja gabarytów InPost
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
    
    return {
        'id_paczki': f"ZG-{uuid.uuid4().hex[:8].upper()}",
        'gabaryt': gabaryt,
        'wymiary_max_cm': GABARYTY[gabaryt]['wymiary'],
        'waga_kg': waga
    }

def generuj_dzien_pracy(data, baza_paczek):
    dzien_tyg = data.weekday()
    
    # Logika natężenia ruchu
    mnoznik = 1.0
    if dzien_tyg == 0: mnoznik = 1.15 # Poniedziałek
    elif dzien_tyg == 4: mnoznik = 0.90 # Piątek
    elif dzien_tyg >= 5: return [] # Weekend
        
    wariancja = random.uniform(0.9, 1.1)
    liczba_paczek = int(baza_paczek * mnoznik * wariancja)
    
    return [generuj_paczke() for _ in range(liczba_paczek)]

def zapisz_do_csv(paczki, data_obj):
    if not paczki:
        return 0

    # 1. Określenie folderu, w którym znajduje się ten skrypt
    folder_skryptu = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Budowa nazwy pliku i pełnej ścieżki
    nazwa_pliku = f"paczki_{data_obj.strftime('%Y%m%d')}.csv"
    pelna_sciezka = os.path.join(folder_skryptu, nazwa_pliku)
    
    klucze = paczki[0].keys()
    with open(pelna_sciezka, 'w', newline='', encoding='utf-8') as plik_csv:
        writer = csv.DictWriter(plik_csv, fieldnames=klucze)
        writer.writeheader()
        writer.writerows(paczki)
        
    print(f"\n[OK] Zapisano plik: {pelna_sciezka}")
    return len(paczki)

# --- URUCHOMIENIE ---
if __name__ == "__main__":
    # Konwersja tekstu na obiekt daty
    try:
        data_celu = datetime.strptime(WYBRANA_DATA_STR, "%Y-%m-%d")
    except ValueError:
        print("Błąd: Niepoprawny format daty! Użyj RRRR-MM-DD.")
        exit()

    print(f"Rozpoczynam generowanie danych dla: {WYBRANA_DATA_STR}...")
    paczki_dzis = generuj_dzien_pracy(data_celu, BAZOWA_LICZBA_PACZEK)
    
    if paczki_dzis:
        ile = zapisz_do_csv(paczki_dzis, data_celu)
        
        # Obliczanie szczegółowych statystyk dla terminala
        a_count = sum(1 for p in paczki_dzis if p['gabaryt'] == 'A')
        b_count = sum(1 for p in paczki_dzis if p['gabaryt'] == 'B')
        c_count = sum(1 for p in paczki_dzis if p['gabaryt'] == 'C')
        laczna_waga = sum(p['waga_kg'] for p in paczki_dzis)
        
        # Wyświetlanie podsumowania
        print("\n--- PODSUMOWANIE DNIA ---")
        print(f"Data:           {WYBRANA_DATA_STR} ({data_celu.strftime('%A')})")
        print(f"Suma paczek:    {ile} szt.")
        print(f" - Gabaryt A:   {a_count} szt.")
        print(f" - Gabaryt B:   {b_count} szt.")
        print(f" - Gabaryt C:   {c_count} szt.")
        print(f"Łączna waga:    {laczna_waga:.2f} kg")
        print("-------------------------")
    else:
        print(f"\nDzień {WYBRANA_DATA_STR} to weekend. Nie wygenerowano żadnych paczek.")
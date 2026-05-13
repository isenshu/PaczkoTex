import csv
import random
import uuid
import os
from datetime import datetime, timedelta

# --- KONFIGURACJA ---
# Podaj DOWOLNĄ datę. Skrypt sam znajdzie poniedziałek w tym tygodniu
WYBRANA_DATA_STR = "2026-05-06"  

# Słownik miast
MIASTA = {
    'Zielona Góra': {'populacja': 140000, 'paczkomaty_w_projekcie': 40, 'pokrycie_km': 3.5},
    'Nowogród Bobrzański': {'populacja': 5000, 'paczkomaty_w_projekcie': 5, 'pokrycie_km': 3.0},
    'Żary': {'populacja': 36000, 'paczkomaty_w_projekcie': 15, 'pokrycie_km': 2.5},
    'Żagań': {'populacja': 25000, 'paczkomaty_w_projekcie': 10, 'pokrycie_km': 4.0},
    'Szprotawa': {'populacja': 11000, 'paczkomaty_w_projekcie': 4, 'pokrycie_km': 2.5},
    'Kożuchów': {'populacja': 9000, 'paczkomaty_w_projekcie': 2, 'pokrycie_km': 3.0},
    'Nowa Sól': {'populacja': 37000, 'paczkomaty_w_projekcie': 20, 'pokrycie_km': 1.0}
}

# Obliczenia globalne dla regionu
LISTA_MIAST = list(MIASTA.keys())
WAGI_MIAST = [MIASTA[m]['populacja'] for m in LISTA_MIAST]
CALKOWITA_POPULACJA = sum(WAGI_MIAST)

# Konfiguracja gabarytów (waga 1-25 kg)
GABARYTY = {
    'A': {'wymiary': '8x38x64', 'prawdopodobienstwo': 0.50},
    'B': {'wymiary': '19x38x64', 'prawdopodobienstwo': 0.35},
    'C': {'wymiary': '41x38x64', 'prawdopodobienstwo': 0.15}
}

def znajdz_poniedzialek(data_obj):
    # Metoda weekday() zwraca: 0=Pon, 1=Wt, ..., 6=Niedz
    # Wystarczy odjąć tyle dni, ile wynosi numer dnia tygodnia
    dni_do_odjecia = data_obj.weekday()
    poniedzialek = data_obj - timedelta(days=dni_do_odjecia)
    return poniedzialek

def oblicz_dzienny_popyt(data_obj):
    dzien_tyg = data_obj.weekday()
    
    # 0=Pon, 1=Wt, 2=Śr, 3=Czw, 4=Pt
    wspolczynniki_bazowe = {
        0: 0.055, # Pon: 5.5%
        1: 0.060, # Wt:  6.0% (Szczyt)
        2: 0.050, # Śr:  5.0%
        3: 0.045, # Czw: 4.5%
        4: 0.040  # Pt:  4.0% (Dołek)
    }
    
    if dzien_tyg >= 5: 
        return 0, 0.0 # Weekend
        
    wspolczynnik_bazowy = wspolczynniki_bazowe[dzien_tyg]
    wariancja = random.uniform(-0.002, 0.002)
    ostateczny_wspolczynnik = wspolczynnik_bazowy + wariancja
    
    liczba_paczek = int(CALKOWITA_POPULACJA * ostateczny_wspolczynnik)
    return liczba_paczek, ostateczny_wspolczynnik

def generuj_paczke(data_dostawy_str):
    typy = list(GABARYTY.keys())
    wagi_gabarytow = [GABARYTY[t]['prawdopodobienstwo'] for t in typy]
    gabaryt = random.choices(typy, weights=wagi_gabarytow, k=1)[0]
    
    waga = random.randint(1, 25)
    miasto = random.choices(LISTA_MIAST, weights=WAGI_MIAST, k=1)[0]
    
    return {
        'id_paczki': f"ZG-{uuid.uuid4().hex[:8].upper()}",
        'data_dostawy': data_dostawy_str,  # <--- Nowa kolumna ułatwiająca analizę!
        'gabaryt': gabaryt,
        'wymiary_max_cm': GABARYTY[gabaryt]['wymiary'],
        'waga_kg': waga,
        'miasto_docelowe': miasto
    }

def zapisz_do_csv(wszystkie_paczki, poniedzialek, piatek):
    if not wszystkie_paczki: 
        return 0

    folder_skryptu = os.path.dirname(os.path.abspath(__file__))
    # Nazywamy plik zakresem dat, np. paczki_tydzien_20260504_20260508.csv
    nazwa_pliku = f"paczki_tydzien_{poniedzialek.strftime('%Y%m%d')}_{piatek.strftime('%Y%m%d')}.csv"
    pelna_sciezka = os.path.join(folder_skryptu, nazwa_pliku)
    
    klucze = wszystkie_paczki[0].keys()
    with open(pelna_sciezka, 'w', newline='', encoding='utf-8') as plik_csv:
        writer = csv.DictWriter(plik_csv, fieldnames=klucze)
        writer.writeheader()
        writer.writerows(wszystkie_paczki)
        
    print(f"\n[OK] Zapisano plik: {pelna_sciezka}")
    return nazwa_pliku

# --- URUCHOMIENIE ---
if __name__ == "__main__":
    try:
        data_celu = datetime.strptime(WYBRANA_DATA_STR, "%Y-%m-%d")
    except ValueError:
        print("Błąd: Niepoprawny format daty! Użyj RRRR-MM-DD.")
        exit()

    poniedzialek = znajdz_poniedzialek(data_celu)
    piatek = poniedzialek + timedelta(days=4)

    print(f"Baza: Podano datę {WYBRANA_DATA_STR}.")
    print(f"Wyznaczono tydzień pracy: od {poniedzialek.strftime('%Y-%m-%d')} (Poniedziałek) do {piatek.strftime('%Y-%m-%d')} (Piątek)\n")
    
    paczki_caly_tydzien = []
    
    print("--- GENEROWANIE DANYCH ---")
    
    # Generujemy dane dla 5 dni (od poniedziałku do piątku)
    for i in range(5):
        obecny_dzien = poniedzialek + timedelta(days=i)
        obecny_dzien_str = obecny_dzien.strftime('%Y-%m-%d')
        
        liczba_paczek, uzyskany_procent = oblicz_dzienny_popyt(obecny_dzien)
        
        # Generowanie paczek dla tego konkretnego dnia
        paczki_dnia = [generuj_paczke(obecny_dzien_str) for _ in range(liczba_paczek)]
        paczki_caly_tydzien.extend(paczki_dnia) # Doklejamy paczki do tygodniowej listy
        
        # Szybki wydruk info dla danego dnia
        nazwa_dnia = obecny_dzien.strftime('%A')
        print(f"{obecny_dzien_str} ({nazwa_dnia:<12}): Wygenerowano {liczba_paczek:<5} paczek (wsp. p = {uzyskany_procent*100:.2f}%)")
    
    # Zapisz całość do jednego pliku
    zapisz_do_csv(paczki_caly_tydzien, poniedzialek, piatek)
    
    # Podsumowanie całego tygodnia
    calkowita_waga = sum(p['waga_kg'] for p in paczki_caly_tydzien)
    
    print("\n--- PODSUMOWANIE TYGODNIA ---")
    print(f"Całkowita liczba paczek: {len(paczki_caly_tydzien)} szt.")
    print(f"Całkowity tonaż:         {calkowita_waga / 1000:.2f} ton ({calkowita_waga} kg)")
    print(f"Średnia waga paczki:     {calkowita_waga / len(paczki_caly_tydzien):.2f} kg")
    print("-----------------------------")
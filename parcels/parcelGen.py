import csv
import random
import os
from datetime import datetime, timedelta

# --- KONFIGURACJA ---
WYBRANA_DATA_STR = "2026-05-06"  

MIASTA = {
    'Zielona Góra': {'populacja': 140000, 'paczkomaty': 40, 'prefix': 'ZG'},
    'Nowogród Bobrzański': {'populacja': 5000, 'paczkomaty': 5, 'prefix': 'NB'},
    'Żary': {'populacja': 36000, 'paczkomaty': 15, 'prefix': 'ZAR'},
    'Żagań': {'populacja': 25000, 'paczkomaty': 10, 'prefix': 'ZGN'},
    'Szprotawa': {'populacja': 11000, 'paczkomaty': 4, 'prefix': 'SZP'},
    'Kożuchów': {'populacja': 9000, 'paczkomaty': 2, 'prefix': 'KOZ'},
    'Nowa Sól': {'populacja': 37000, 'paczkomaty': 20, 'prefix': 'NS'}
}

LISTA_MIAST = list(MIASTA.keys())
WAGI_MIAST = [MIASTA[m]['populacja'] for m in LISTA_MIAST]
CALKOWITA_POPULACJA = sum(WAGI_MIAST)

# Zaktualizowane gabaryty: wprowadzono minimalną i maksymalną WYSOKOŚĆ
GABARYTY_INFO = {
    'A': {'min_wys': 1,  'max_wys': 8,  'max_szer': 38, 'max_dl': 64, 'prawdopodobienstwo': 0.50},
    'B': {'min_wys': 9,  'max_wys': 19, 'max_szer': 38, 'max_dl': 64, 'prawdopodobienstwo': 0.35},
    'C': {'min_wys': 20, 'max_wys': 41, 'max_szer': 38, 'max_dl': 64, 'prawdopodobienstwo': 0.15}
}
TYPY_GABARYTOW = list(GABARYTY_INFO.keys())
WAGI_GABARYTOW = [GABARYTY_INFO[t]['prawdopodobienstwo'] for t in TYPY_GABARYTOW]

def znajdz_poniedzialek(data_obj):
    return data_obj - timedelta(days=data_obj.weekday())

def oblicz_dzienny_popyt(data_obj):
    dzien_tyg = data_obj.weekday()
    if dzien_tyg >= 5: return 0, 0.0 # Weekend
        
    wspolczynniki = {0: 0.055, 1: 0.060, 2: 0.050, 3: 0.045, 4: 0.040}
    wsp_bazowy = wspolczynniki[dzien_tyg]
    ostateczny = wsp_bazowy + random.uniform(-0.002, 0.002)
    
    return int(CALKOWITA_POPULACJA * ostateczny), ostateczny

def generuj_paczki_na_dzien(data_dostawy_str, liczba_paczek):
    if liczba_paczek <= 0: return []
    
    wylosowane_gabaryty = random.choices(TYPY_GABARYTOW, weights=WAGI_GABARYTOW, k=liczba_paczek)
    wylosowane_miasta = random.choices(LISTA_MIAST, weights=WAGI_MIAST, k=liczba_paczek)
    
    paczki_dnia = []
    
    for i in range(liczba_paczek):
        gabaryt = wylosowane_gabaryty[i]
        miasto = wylosowane_miasta[i]
        dane_miasta = MIASTA[miasto]
        pref = dane_miasta['prefix']
        
        id_paczki = f"{pref}-{random.randint(0, 0xFFFFFFFF):08X}"
        nr_paczkomatu = random.randint(1, dane_miasta['paczkomaty'])
        
        g_info = GABARYTY_INFO[gabaryt]
        
        paczki_dnia.append({
            'id_paczki': id_paczki,
            'data_dostawy': data_dostawy_str,
            'gabaryt': gabaryt,
            # Tutaj jest kluczowa zmiana: losujemy od dolnego do górnego limitu
            'wysokosc_cm': random.randint(g_info['min_wys'], g_info['max_wys']),
            'szerokosc_cm': random.randint(1, g_info['max_szer']),
            'dlugosc_cm': random.randint(1, g_info['max_dl']),
            'waga_kg': random.randint(1, 25),
            'miasto_docelowe': miasto,
            'id_paczkomatu': f"{pref}-{nr_paczkomatu:02d}"
        })
        
    return paczki_dnia

def zapisz_do_csv(wszystkie_paczki, poniedzialek, piatek):
    if not wszystkie_paczki: return 0

    folder = os.path.dirname(os.path.abspath(__file__))
    
    # TUTAJ JEST KRÓTSZA NAZWA (np. paczki_tydzien_04.05-08.05.2026.csv):
    nazwa_pliku = f"paczki_tydzien_{poniedzialek.strftime('%d.%m')}-{piatek.strftime('%d.%m.%Y')}.csv"
    
    pelna_sciezka = os.path.join(folder, nazwa_pliku)
    
    with open(pelna_sciezka, 'w', newline='', encoding='utf-8') as plik_csv:
        writer = csv.DictWriter(plik_csv, fieldnames=wszystkie_paczki[0].keys())
        writer.writeheader()
        writer.writerows(wszystkie_paczki)
        
    print(f"\n[OK] Zapisano plik: {pelna_sciezka}")
    return nazwa_pliku

# --- URUCHOMIENIE ---
if __name__ == "__main__":
    try:
        data_celu = datetime.strptime(WYBRANA_DATA_STR, "%Y-%m-%d")
    except ValueError:
        print("Błąd daty!")
        exit()

    poniedzialek = znajdz_poniedzialek(data_celu)
    piatek = poniedzialek + timedelta(days=4)

    print("--- START GENEROWANIA (TRYB SZYBKI Z POPRAWIONĄ LOGIKĄ WYMIARÓW) ---")
    paczki_caly_tydzien = []
    
    for i in range(5):
        obecny_dzien = poniedzialek + timedelta(days=i)
        obecny_dzien_str = obecny_dzien.strftime('%Y-%m-%d')
        
        liczba_paczek, uzyskany_procent = oblicz_dzienny_popyt(obecny_dzien)
        paczki_dnia = generuj_paczki_na_dzien(obecny_dzien_str, liczba_paczek)
        paczki_caly_tydzien.extend(paczki_dnia)
        
        print(f"{obecny_dzien_str} ({obecny_dzien.strftime('%A')[:3]}): {liczba_paczek} paczek")
    
    zapisz_do_csv(paczki_caly_tydzien, poniedzialek, piatek)
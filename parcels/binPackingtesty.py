import csv
import os
import glob
from collections import defaultdict

# --- KONFIGURACJA ---
LIMIT_WAGI_KG = 1069.0
LIMIT_OBJETOSCI_CM3 = 8_100_000.0  # 75% z 10.8 m^3

def wczytaj_najnowszy_plik_csv():
    folder = os.path.dirname(os.path.abspath(__file__))
    pliki = glob.glob(os.path.join(folder, "paczki_tydzien_*.csv"))
    
    if not pliki:
        print("Błąd: Nie znaleziono pliku z paczkami.")
        return None
        
    najnowszy = max(pliki, key=os.path.getctime)
    print(f"Wczytano plik danych: {os.path.basename(najnowszy)}\n")
    return najnowszy

def pakuj_busy_skonsolidowane(sciezka_csv):
    # Grupujemy dane WYŁĄCZNIE po dacie: dane_pogrupowane[data_dostawy] = [paczka1, paczka2, ...]
    dane_pogrupowane = defaultdict(list)
    
    with open(sciezka_csv, mode='r', encoding='utf-8') as plik:
        reader = csv.DictWriter # Używamy DictReader do odczytu słowników
        reader = csv.DictReader(plik)
        for wiersz in reader:
            dane_pogrupowane[wiersz['data_dostawy']].append(wiersz)
    
    raport_tygodniowy = {}
    
    for data, paczki in dane_pogrupowane.items():
        # KLUCZOWA OPTYMALIZACJA: Sortujemy paczki najpierw po mieście docelowym, 
        # a wewnątrz miasta po ID paczkomatu. Dzięki temu bus ładuje najpierw całą Zieloną Górę,
        # a wolną przestrzeń doładowuje kolejnym miastem (np. Nowogrodem), nie mieszając paczek chaotycznie.
        paczki.sort(key=lambda p: (p['miasto_docelowe'], p['id_paczkomatu']))
        
        busy = []
        # Rozszerzamy strukturę busa o listę obsługiwanych miast (jako set, aby unikać duplikatów)
        aktualny_bus = {
            'waga': 0.0, 
            'objetosc': 0.0, 
            'miasta': set(), 
            'id_paczkomatow': set(),
            'liczba_paczek': 0
        }
        
        for paczka in paczki:
            waga = float(paczka['waga_kg'])
            objetosc = float(paczka['wysokosc_cm']) * float(paczka['szerokosc_cm']) * float(paczka['dlugosc_cm'])
            
            # Sprawdzenie limitów technicznych pojazdu
            if (aktualny_bus['waga'] + waga <= LIMIT_WAGI_KG) and (aktualny_bus['objetosc'] + objetosc <= LIMIT_OBJETOSCI_CM3):
                # Dodajemy paczkę do aktualnego busa (niezależnie od miasta)
                aktualny_bus['waga'] += waga
                aktualny_bus['objetosc'] += objetosc
                aktualny_bus['miasta'].add(paczka['miasto_docelowe'])
                aktualny_bus['id_paczkomatow'].add(paczka['id_paczkomatu'])
                aktualny_bus['liczba_paczek'] += 1
            else:
                # Jeśli się nie mieści, zamykamy ten pojazd i wysyłamy go w trasę
                busy.append(aktualny_bus)
                
                # Otwieramy kolejny pojazd dla tej i następnych paczek
                aktualny_bus = {
                    'waga': waga, 
                    'objetosc': objetosc, 
                    'miasta': {paczka['miasto_docelowe']}, 
                    'id_paczkomatow': {paczka['id_paczkomatu']},
                    'liczba_paczek': 1
                }
        
        # Zapisujemy ostatni pojazd z końca pętli
        if aktualny_bus['liczba_paczek'] > 0:
            busy.append(aktualny_bus)
            
        raport_tygodniowy[data] = busy
        
    return raport_tygodniowy

def wyswietl_raport_skonsolidowany(raport):
    for data, busy in sorted(raport.items()):
        print(f"=== DATA: {data} ===")
        print(f"Łączna liczba wymaganych busów na ten dzień: {len(busy)}")
        
        for i, bus in enumerate(busy, 1):
            proc_wagi = (bus['waga'] / LIMIT_WAGI_KG) * 100
            proc_obj = (bus['objetosc'] / LIMIT_OBJETOSCI_CM3) * 100
            list_miast = ", ".join(sorted(bus['miasta']))
            
            print(f"  Bus {i}: {bus['liczba_paczek']:>3} paczek | "
                  f"Waga: {proc_wagi:>5.1f}% ({bus['waga']:>7.2f} kg) | "
                  f"Obj: {proc_obj:>5.1f}% ({bus['objetosc']/1000000:>5.2f} m³) | "
                  f"Trasa obejmuje miasta: [{list_miast}] (Paczkomaty: {len(bus['id_paczkomatow'])})")
        print("-" * 60)

if __name__ == "__main__":
    najnowszy_plik = wczytaj_najnowszy_plik_csv()
    
    if najnowszy_plik:
        wyniki_załadunku = pakuj_busy_skonsolidowane(najnowszy_plik)
        wyswietl_raport_skonsolidowany(wyniki_załadunku)
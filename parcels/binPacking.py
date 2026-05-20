import csv
import os
import glob
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog

# --- KONFIGURACJA ---
LIMIT_WAGI_KG = 1069.0
LIMIT_OBJETOSCI_CM3 = 8_100_000.0  # 75% z 10.8 m^3



def wczytaj_najnowszy_plik_csv():
    # Inicjalizacja ukrytego okna głównego
    root = tk.Tk()
    root.withdraw()
    
    # Wywołanie okienka wyboru pliku
    sciezka = filedialog.askopenfilename(
        title="Wybierz plik CSV z paczkami",
        filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
    )
    
    if sciezka:
        print(f"Wczytano plik danych: {sciezka}\n")
        return sciezka
    else:
        print("Anulowano wybór pliku.")
        return None

def pakuj_busy(sciezka_csv):
    # defaultdict automatycznie tworzy zagnieżdżone słowniki i listy, jeśli klucz nie istnieje
    # Struktura: dane[data_dostawy][miasto_docelowe] = [paczka1, paczka2, ...]
    dane_pogrupowane = defaultdict(lambda: defaultdict(list))
    
    with open(sciezka_csv, mode='r', encoding='utf-8') as plik:
        reader = csv.DictReader(plik)
        for wiersz in reader:
            dane_pogrupowane[wiersz['data_dostawy']][wiersz['miasto_docelowe']].append(wiersz)
    
    raport_tygodniowy = {}
    
    for data, miasta in dane_pogrupowane.items():
        raport_tygodniowy[data] = {}
        
        for miasto, paczki in miasta.items():
            # Sortowanie paczek po paczkomacie. Dzięki temu kurier ma w busie
            # zgrupowane paczki do jednej maszyny, co ułatwi późniejsze trasowanie.
            paczki.sort(key=lambda p: p['id_paczkomatu'])
            
            busy = []
            aktualny_bus = {'waga': 0.0, 'objetosc': 0.0, 'id_paczkomatow': set()}
            licznik_paczek = 0
            
            for paczka in paczki:
                waga = float(paczka['waga_kg'])
                # Wyliczenie objętości w cm3 na bieżąco
                objetosc = float(paczka['wysokosc_cm']) * float(paczka['szerokosc_cm']) * float(paczka['dlugosc_cm'])
                
                # Sprawdzenie dwóch warunków brzegowych
                if (aktualny_bus['waga'] + waga <= LIMIT_WAGI_KG) and (aktualny_bus['objetosc'] + objetosc <= LIMIT_OBJETOSCI_CM3):
                    # Paczka się mieści
                    aktualny_bus['waga'] += waga
                    aktualny_bus['objetosc'] += objetosc
                    aktualny_bus['id_paczkomatow'].add(paczka['id_paczkomatu'])
                    licznik_paczek += 1
                else:
                    # Bus pełny - zapisujemy jego stan
                    aktualny_bus['liczba_paczek'] = licznik_paczek
                    busy.append(aktualny_bus)
                    
                    # Otwieramy nowego busa i wrzucamy do niego obecną paczkę
                    aktualny_bus = {
                        'waga': waga, 
                        'objetosc': objetosc, 
                        'id_paczkomatow': {paczka['id_paczkomatu']}
                    }
                    licznik_paczek = 1
            
            # Zapisanie ostatniego otwartego busa, jeśli ma jakieś paczki
            if licznik_paczek > 0:
                aktualny_bus['liczba_paczek'] = licznik_paczek
                busy.append(aktualny_bus)
                
            raport_tygodniowy[data][miasto] = busy
            
    return raport_tygodniowy

def wyswietl_podsumowanie(raport):
    for data, miasta in sorted(raport.items()):
        print(f"=== DATA: {data} ===")
        for miasto, busy in sorted(miasta.items()):
            print(f"  {miasto}: Wymagane busy -> {len(busy)}")
            
            for i, bus in enumerate(busy, 1):
                proc_wagi = (bus['waga'] / LIMIT_WAGI_KG) * 100
                proc_obj = (bus['objetosc'] / LIMIT_OBJETOSCI_CM3) * 100
                liczba_maszyn = len(bus['id_paczkomatow'])
                
                print(f"    Bus {i}: {bus['liczba_paczek']:>3} szt. | "
                      f"Waga: {proc_wagi:>5.1f}% ({bus['waga']:>7.2f} kg) | "
                      f"Obj: {proc_obj:>5.1f}% ({bus['objetosc']/1000000:>5.2f} m³) | "
                      f"Paczkomaty: {liczba_maszyn}")
        print("-" * 50)

if __name__ == "__main__":
    najnowszy_plik = wczytaj_najnowszy_plik_csv()
    
    if najnowszy_plik:
        wyniki_załadunku = pakuj_busy(najnowszy_plik)
        wyswietl_podsumowanie(wyniki_załadunku)
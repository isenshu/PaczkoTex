import pandas as pd

df = pd.read_csv("C:/Users/bsiek/Desktop/szkoua/Semestr_4/metodyObliczeniowe/projekt/PaczkoTex/parcels/paczki_tydzien_04.05-08.05.2026.csv")

df['objetosc_cm3'] = df['wysokosc_cm'] * df['szerokosc_cm'] * df['dlugosc_cm']


print("=== STATYSTYKI WSPÓLNE (CAŁY ŁADUNEK) ===")
print(f"Całkowita ilość paczek: {len(df)} szt.")

srednia_waga = df['waga_kg'].mean()
print(f"Średnia waga paczki: {srednia_waga:.2f} kg")

srednia_wys = df['wysokosc_cm'].mean()
srednia_szer = df['szerokosc_cm'].mean()
srednia_dl = df['dlugosc_cm'].mean()
print(f"Średnie wymiary (Wys x Szer x Dł): {srednia_wys:.1f} cm x {srednia_szer:.1f} cm x {srednia_dl:.1f} cm")

srednia_objetosc_cm3 = df['objetosc_cm3'].mean()
srednia_objetosc_m3 = srednia_objetosc_cm3 / 1000000
print(f"Średnia objętość paczki: {srednia_objetosc_cm3:.0f} cm³ (czyli ok. {srednia_objetosc_m3:.4f} m³)\n")



gabaryty = ['A', 'B', 'C']

for gabaryt in gabaryty:
    print(f"=== STATYSTYKI DLA GABARYTU: {gabaryt} ===")
    
    # Wyciągamy z tabeli tylko paczki danego gabarytu
    df_gabaryt = df[df['gabaryt'] == gabaryt]
    
    if df_gabaryt.empty:
        print("Brak paczek tego gabarytu w pliku.\n")
        continue
        
    s_waga = df_gabaryt['waga_kg'].mean()
    s_wys = df_gabaryt['wysokosc_cm'].mean()
    s_szer = df_gabaryt['szerokosc_cm'].mean()
    s_dl = df_gabaryt['dlugosc_cm'].mean()
    
    s_obj_cm3 = df_gabaryt['objetosc_cm3'].mean()
    s_obj_m3 = s_obj_cm3 / 1000000
    
    print(f"Ilość paczek: {len(df_gabaryt)} szt.")
    print(f"Średnia waga: {s_waga:.2f} kg")
    print(f"Średnie wymiary (Wys x Szer x Dł): {s_wys:.1f} cm x {s_szer:.1f} cm x {s_dl:.1f} cm")
    print(f"Średnia objętość: {s_obj_cm3:.0f} cm³ (czyli ok. {s_obj_m3:.4f} m³)\n")
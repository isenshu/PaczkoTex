# Dokumentacja: Generator Paczek (Projekt PaczkoTex)
**Plik:** `parcelGen.py`

## Co dokładnie robi obecna wersja kodu?

Obecny skrypt to wysoce zoptymalizowany generator wsadowy (batch generator), który symuluje popyt na usługi kurierskie w regionie Zielonej Góry i okolicznych miast. Na podstawie wpisanej daty, automatycznie generuje bazę przesyłek na cały tydzień roboczy (od poniedziałku do piątku).

**Kluczowe funkcjonalności:**
*   **Modelowanie Popytu (Top-Down):** Generator nie opiera się na "sztywnych" liczbach, lecz wylicza ilość paczek na podstawie populacji regionu (ok. 263 000 osób). Zakłada, że dziennie obsługujemy średnio 5% populacji.
*   **Realistyczny rozkład tygodniowy:** Implementuje logikę e-commerce, gdzie wtorki są dniami szczytowymi (6% populacji), a piątki najsłabszymi (4% populacji).
*   **Zoptymalizowane wymiary InPost:** Generuje paczki w 3 gabarytach (A, B, C). Kod uwzględnia nie tylko maksymalne, ale i minimalne wymiary dla wysokości (np. paczka B musi mieć minimum 9 cm wysokości, by nie wpaść do skrytki A). Waga każdej paczki jest losowana z przedziału od 1 do 25 kg.
*   **Trasowanie pod Paczkomaty:** Każda paczka otrzymuje unikalny identyfikator przesyłki (np. `ZG-A1B2C3D4`) oraz jest przypisywana do konkretnego miasta i **konkretnego paczkomatu** (np. `ZG-05` dla 5. maszyny w Zielonej Górze). Ułatwia to późniejsze grupowanie danych.
*   **Wysoka wydajność:** Dzięki zastosowaniu pre-alokacji i losowania na listach, skrypt generuje około 70 000 paczek w ułamek sekundy.
*   **Pojedynczy plik wyjściowy:** Cały tydzień pracy zapisywany jest do jednego, łatwego w obróbce pliku CSV z czytelną datą w nazwie (np. `paczki_tydzien_04.05-08.05.2026.csv`), co jest idealne dla biblioteki Pandas.

---

## Co trzeba jeszcze zrobić (Kolejne kroki dla zespołu)

Dane mamy już wygenerowane, teraz projekt musi przejść w fazę układania tras i przydzielania kurierów. Oto wyzwania, które przed Wami stoją:

*   **[Rozwiązanie problemu ładowności (Bin Packing Problem)]**
    *   Wiedząc, że bus kurierski ma limit 1000 kg (1 tona), zespół musi napisać skrypt, który sumuje wagę paczek dla konkretnych paczkomatów w dany dzień.
    *   *Decyzja do podjęcia:* Co robimy, gdy waga przesyłek dla paczkomatu (np. we wtorek) przekroczy 1000 kg? Czy algorytm dopuszcza wysłanie dwóch kurierów do jednej maszyny, czy "wirtualnie" przymykamy oko na przeładowanie busa?
*   **[Algorytm przypisywania kurierów]**
    *   Stworzenie puli kurierów (np. 15 kierowców).
    *   Algorytm, który czyta wygenerowany plik CSV, grupuje paczki po kluczu `id_paczkomatu` i rozdziela je na "paki" poszczególnych busów, pilnując limitu wagi.
*   **[Macierz Odległości i Czasów (Distance Matrix)]**
    *   Stworzenie w kodzie (np. w formie słownika lub wczytywanej z zewnętrznego pliku) prostej macierzy odległości pomiędzy miastami z projektu (np. czas przejazdu Zielona Góra <-> Nowa Sól).
    *   Bez tego algorytm może wysłać kuriera w nieopłacalną trasę, skacząc między najdalszymi punktami (np. Żagań -> Nowogród Bobrzański -> Szprotawa).
*   **[Kalkulacja czasu obsługi punktu (Drop-off time)]**
    *   Wykorzystanie parametru `pokrycie_km` (który zostawiliśmy w słowniku `MIASTA`) do obliczenia, ile czasu kurier spędza na dojazd i wypakowanie paczek pod konkretną maszyną.
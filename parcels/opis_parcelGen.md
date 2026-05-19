# Dokumentacja: Generator Paczek (Projekt PaczkoTex)
**Plik:** `parcelGen.py`

## Co dokładnie robi obecna wersja kodu?

Obecny skrypt to zaawansowany generator wsadowy (batch generator), który symuluje popyt na usługi kurierskie w regionie Zielonej Góry i okolicznych miast. Na podstawie wpisanej daty, automatycznie generuje bazę przesyłek na cały tydzień roboczy (od poniedziałku do piątku), zapisując wszystko do jednego pliku CSV.

**Kluczowe funkcjonalności:**
*   **Modelowanie Popytu (Top-Down):** Generator bazuje na populacji regionu (ok. 258 000 osób) do wyliczenia liczby paczek. Zakłada, że dziennie obsługujemy od 2% do 3% populacji, co daje łącznie ok. 32 000 paczek tygodniowo.
*   **Realistyczny rozkład tygodniowy:** Implementuje logikę e-commerce, gdzie wtorki są dniami szczytowymi (ok. 3.0% populacji), a piątki najsłabszymi (ok. 2.0% populacji).
*   **Zaawansowane generowanie paczek:**
    *   **Wymiary:** Zamiast sztywnych wymiarów, każda paczka ma losowane trzy osobne wartości: `wysokosc_cm`, `szerokosc_cm` i `dlugosc_cm`, mieszczące się w dopuszczalnych normach dla gabarytów A, B i C. Uwzględniono minimalną wysokość, aby paczki pasowały do odpowiednich skrytek.
    *   **Waga (Rozkład Gamma):** Waga nie jest już losowana jednostajnie. Skrypt wykorzystuje **rozkład prawdopodobieństwa Gamma**, aby realistycznie modelować wagę paczek. Każdy gabaryt (A, B, C) ma własny, odrębny rozkład – małe paczki są statystycznie lżejsze, a duże cięższe. Waga jest liczbą całkowitą z przedziału 1-25 kg.
*   **Strukturalne ID i trasowanie:**
    *   Każda paczka otrzymuje unikalny, strukturalny identyfikator (np. `ZG-050600001`), który zawiera prefix miasta, datę i numer porządkowy.
    *   Każda paczka jest przypisywana do konkretnego miasta i **konkretnego paczkomatu** (np. `ZG-05`), co jest kluczowe dla dalszych etapów projektu.
*   **Wysoka wydajność:** Dzięki zastosowaniu wektoryzacji (pre-alokacja list z miastami i gabarytami za pomocą `random.choices`), skrypt generuje dane dla całego dnia w jednej, szybkiej operacji, a nie paczka po paczce.
*   **Pojedynczy, szczegółowy plik wyjściowy:** Cały tydzień pracy zapisywany jest do jednego pliku CSV (np. `paczki_tydzien_04.05-08.05.2026.csv`). Plik zawiera szczegółowe kolumny (`id_paczki`, `data_dostawy`, `gabaryt`, `wysokosc_cm`, `szerokosc_cm`, `dlugosc_cm`, `waga_kg`, `miasto_docelowe`, `id_paczkomatu`), gotowe do analizy w bibliotece Pandas.

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

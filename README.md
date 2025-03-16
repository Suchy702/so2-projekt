# Problem ucztujących filozofów
Celem projektu było przedstawienie problemu ucztujących filozofów, jako ćwiczenie z synchronizacji wątków (jeden proces - jeden filozof). Aby uniknąć zakleszczenia zastosowano metodę asymetrycznego podnoszenia widelców.

## Narzędzia
Progam został wykonany w języku C++ z użyciem biblioteki threads oraz ncurses (do czytelnego wyświetlania informacji w terminalu).

## Wymagania
- System Linux
- kompilator C++ (g++)
- Cmake
- ncurses

Instalacja zależności
```
sudo apt-get install -y g++ cmake libncurses5-dev libncursesw5-dev
```

## Uruchomienie
Aby uruchomić program musimy nadać uprawnienia wykonania dla pliku `run.sh`
```
chmod +x run.sh
```
Uruchamiamy skrypt z odpowiednimi argumentami
```
./run.sh <liczba_filozofów> <min_czas> <max_czas>
```
- `liczba_filozofów`– Liczba filozofów (i widelców) w symulacji.
- `min_czas` – Minimalny losowy czas (w milisekundach), który filozof spędza na myśleniu/jedzeniu.
- `max_czas` – Maksymalny losowy czas (w milisekundach), który filozof spędza na myśleniu/jedzeniu.

Przykładowe uruchomienie
```
./run.sh 5 1000 3000
```

Aby zakończyć program należy nacisnąć `CTRL + C`

![image](https://github.com/user-attachments/assets/ad7e7d4b-b71c-4d6e-b155-f7f55c8637d8)

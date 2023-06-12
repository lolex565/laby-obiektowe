# Projekt na zajęcia laboratoryjne z Programowania obiektowego

## Specyfika

Projekt tworzony jest w języku [Python](https://www.python.org/) (w wersji 3.11.2) z wykorzystaniem biblioteki [Matplotlib](https://matplotlib.org/) do tworzenia wykresów populacji po zakończeniu symulacji.

## Członkowie zespołu

- Bedryło Miłosz - lider
- Kręgiel Artur

## Opis projektu
Jako temat projektu została wybrana symulacja agentowa ekosystemu.
W projekcie zostanie zaimplementowany ekosystem, w którym będzie żyło 5 gatunków zwierząt: wilki, orły, myszy, jelenie i bobry.
Zwierzęta będą posiadały cechy takie jak: prędkość, siła, zdolność do rozmnażania, zdolność do polowania.
Zwierzęta będą się poruszać po mapie, na której będą znajdowały się pola z jedzeniem, wodą, drzewami.
Zwierzęta będą mogły polować na inne zwierzęta.
Zwierzęta będą mogły się rozmnażać.
Zwierzęta będą mogły umierać z głodu, starości, zabicia przez inne zwierzęta.
Zwierzęta będą mogły się poruszać po mapie.
Zwierzęta będą mogły jeść.
Zwierzęta będą mogły pić.

## Aktualnie zaimplementowane funkcjonalności
- stworzenie mapy (grid 2D)
- stworzenie zwierząt
- stworzenie drzew, wody, jedzenia
- stworzenie funkcji rysującej mapę
- stworzenie funkcji aktualizującej mapę

## Sposób uruchomienia

Najpierw należy sklonować repozytorium:

```
git clone https://github.com/lolex565/laby-obiektowe.git
```

A następnie zainstalować niezbędne biblioteki:

```
pip install -r requirements.txt
```

Aby uruchomić program należy wpisać w terminalu będąc w katalogu projektu:

- dodać uprawnienia do uruchamiania skryptów `bash`:

```
chmod +x *.sh
```

- uruchomić skrypt `run.sh`:

```
./run.sh
```
Program testowany był jedynie na systemie Linux i macos, które mają wbudowaną powłokę bash, jednak do uruchomienia programu w systemie windows najprościej będzie użyć narzędzia [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

Wtedy należy wykonać te same kroki co w przypadku systemu Linux.

Alternatywnym sposobem uruchomienia programu jest uruchomienie skryptu `main.py` bezpośrednio z wiersza poleceń systemu windows(jednak trzeba upewnić się co do istnienia folderu logs, graphs i csv):

```
python3 main.py
```
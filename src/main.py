import platform, os, time

from ecosystem_simulation import Board, BoardSize
from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.objects.animals.predators import *
from ecosystem_simulation.utils import *


if __name__ == "__main__":
    height = min(int(input("Podaj wysokość planszy: ")), 50)
    width = min(int(input("Podaj szerokość planszy: ")), 50)

    predators_num = min(int(input("Podaj liczbę drapieżników: ")), 500)
    preys_num = min(int(input("Podaj liczbę ofiar: ")), 600)
    beavers_num = min(int(input("Podaj liczbę bobrów: ")), 400)
    max_pop = min(int(input("Podaj maksymalną liczbę zwierząt na planszy(zalecany 600 maksymalnie): ")), 3000)

    items_num = min(int(input("Podaj liczbę obiektów nieożywionych: ")), 1000)
    time.sleep(min((float(input("podaj minimalny czas między turami w ms: ")) / 1000), 0.01))
    max_turns = min(int(input("Podaj maksymalną liczbę tur (domyślnie maksymalnie 10 tysięcy tur): ")), 10000)

    print("Przygotowywanie symulacji...")

    # tworzymy planszę
    print("Tworzenie planszy...")
    board = Board(BoardSize(width, height), max_pop, max_turns)

    # dodajemy zwierzęta

    # dodajemy drapieżniki
    print("Dodawanie drapieżników...")
    for _ in range(predators_num):
        board.add_predator()

    # dodajemy ofiary
    print("Dodawanie ofiar...")
    for _ in range(preys_num):
        board.add_prey()

    # dodajemy bobry
    print("Dodawanie bobrów...")
    for _ in range(beavers_num):
        board.add_beaver()

    # dodajemy obiekty nieożywione
    print("Dodawanie obiektów nieożywionych...")
    for _ in range(items_num):
        board.add_random_item()

    # komenda czyszcząca ekran
    # cls dla Windows, clear dla Linux/Unix
    clear_screen_cmd = "cls" if platform.system() == "Windows" else "clear"

    print("Rozpoczynanie symulacji...")
    os.system(clear_screen_cmd)
    print(board)
    try:
        while not (end := board.check_end_conditions()):
            board.update()
            os.system(clear_screen_cmd)
            print(board)
            print("-" * board.get_size()[0])
            print("Tura = ", board.get_round())
            print("Populacja = ", board.get_population())
            print("Żywe drapieżniki = ", board.get_predators())
            print("Żywe ofiary = ", board.get_preys())
            print("Żywe bobry = ", board.get_beavers())
        else:
            print(f"Przyczyna zakończenia symulacji: {end}")
    except KeyboardInterrupt:
        print("Przerwano symulację")

    choice_csv = input("Czy chcesz zapisać wyniki do pliku csv? [t/n]: ")
    if choice_csv.lower() == "t":
        time_of_creation = time.strftime("%Y-%m-%d_%H-%M-%S")
        create_csv_file(f'wyniki_{time_of_creation}.csv', board.get_pop_data())
        print(f'Plik csv został zapisany jako csv/wyniki_{time_of_creation}.csv')
        choice_graph = input("Czy chcesz utworzyć wykresy z wyników? [t/n]: ")
        if choice_graph.lower() == "t":
            create_graphs(f'wyniki_{time_of_creation}')
            print(f'Wykresy zostały zapisane w folderze graphs/wyniki_{time_of_creation}')

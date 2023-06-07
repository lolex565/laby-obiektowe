import pickle, platform, os, time

from ecosystem_simulation import Board, BoardSize
from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.objects.animals.predators import *


if __name__ == "__main__":
    height = min(int(input("Podaj wysokość planszy: ")), 20)
    width = min(int(input("Podaj szerokość planszy: ")), 40)

    predators_num = min(int(input("Podaj liczbę drapieżników: ")), 500)
    preys_num = min(int(input("Podaj liczbę ofiar: ")), 600)
    beavers_num = min(int(input("Podaj liczbę bobrów: ")), 400)

    items_num = min(int(input("Podaj liczbę obiektów nieożywionych: ")), 1000)

    print("Przygotowywanie symulacji...")

    # tworzymy planszę
    print("Tworzenie planszy...")
    board = Board(BoardSize(width, height))

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
            time.sleep(0.1)
        else:
            print(f"Przyczyna zakończenia symulacji: {end}")
    except KeyboardInterrupt:
        print("Przerwano symulację")

import pickle, platform, os, time

from ecosystem_simulation import Board, BoardSize
from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.objects.animals.predators import *


if __name__ == "__main__":
    board = Board(BoardSize(20, 20))

    # dodajemy zwierzęta
    for _ in range(50):
        board.add_random_animal()

    # dodajemy obiekty nieożywione
    for _ in range(40):
        board.add_random_item()

    print(board)

    # komenda czyszcząca ekran
    # cls dla Windows, clear dla Linux/Unix
    clear_screen_cmd = "cls" if platform.system() == "Windows" else "clear"

    print(board)
    try:
        while not (end := board.check_end_conditions()):
            os.system(clear_screen_cmd)
            board.update()
            print(board)
            print("-" * board.get_size()[0])
            print("Tura = ", board.get_round())
            print("Populacja = ", board.get_population())
            print("Żywe drapieżniki = ", board.get_predators())
            print("Żywe ofiary = ", board.get_preys())
            time.sleep(0.4)
        else:
            print(f"Przyczyna zakończenia symulacji: {end}")
    except KeyboardInterrupt:
        print("Przerwano symulację")

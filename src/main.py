import pickle, platform, os, time, logging

from ecosystem_simulation import Board, BoardSize
from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.objects.animals.predators import *


if __name__ == "__main__":
    print("Compiles!")

    predator = Wolf(0, 0, 5.6, 20, 3, 100, 100, GENDER_MALE, 10, 50, 20)
    prey = Mouse(0, 0, 0.1, 10, 1, 100, 100, GENDER_FEMALE, 10, 1, 10)
    print(predator.get_hit_points())
    print(prey.get_hit_points())
    predator.attack(prey)
    print(prey.get_hit_points())
    prey.defend(predator)
    print(predator.get_durability())
    print(predator.get_hit_points())

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
    while not (end := board.check_end_conditions()):
        os.system(clear_screen_cmd)
        board.update()
        print(board)
        print("-" * board.get_size()[0])
        print("Populacja = ", board.get_population())
        print("Żywe drapieżniki = ", board.get_predators())
        print("Żywe ofiary = ", board.get_preys())
        time.sleep(0.4)
    else:
        print(f"Przyczyna zakończenia symulacji: {end}")
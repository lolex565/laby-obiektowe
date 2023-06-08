from random import randint, choice, uniform
import math, logging, time

from .objects import Object
from .objects.items import *
from .objects.animals import *
from .objects.animals.beaver import Beaver
from .objects.animals.predators import *
from .objects.animals.preys import *
from .utils import *


class BoardSize:
    """Klasa reprezentująca rozmiar planszy"""

    def __init__(self, width: int, height: int) -> None:
        """Konstruktor klasy BoardSize

        :param width: szerokość planszy
        :param height: wysokość planszy
        """
        self.__width = width
        self.__height = height

    def get_size(self) -> tuple:
        """Zwraca rozmiar planszy
        
        :return: krotka (szerokość, wysokość)
        """
        return (self.__width, self.__height)
    
    def get_area(self) -> int:
        """Zwraca powierzchnię planszy
        
        :return: powierzchnia planszy
        """
        return self.__width * self.__height

    

class Board:
    """Klasa reprezentująca planszę"""
    
    __total_object_count = 0  # całkowita liczba obiektów
    __population = 0          # liczba żywych obiektów
    __predators = 0           # liczba drapieżników
    __preys = 0               # liczba ofiar
    __beavers = 0             # liczba bobrów
    __grid = []               # siatka planszy
    __objects = set()         # zbiór wszystkich obiektów
    __round = 0               # tura
    __size = None             # rozmiar planszy
    __max_pop = 1000          # maksymalna liczba zwierząt na planszy
    __pop_data = []           # dane o populacji w czasie

    # możliwe zwierzęta
    __possible_animals = {
        "Mouse": Mouse,
        "Deer": Deer,
        "Wolf": Wolf,
        "Eagle": Eagle,
        "Beaver": Beaver
    }

    # możliwe przedmioty
    __possible_items = {
        "Tree": Tree,
        "Rock": Rock,
        "Plant": Plant,
        "Water": Water
    }

    def __init__(self, size: BoardSize, max_pop: int) -> None:
        """Konstruktor klasy Board

        :param size: rozmiar planszy
        """
        self.__size = size
        self.__grid = [[None for _ in range(self.__size.get_size()[0])] for _ in range(self.__size.get_size()[1])]
        self.__max_pop = max_pop
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='logs/simulation_%s.log' % time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), filemode='a')

    def __str__(self) -> str:
        """Zwraca planszę w postaci stringa"""
        grid_str = [[str(cell) if cell is not None else name_to_emoji("Dirt") for cell in row] for row in self.get_grid()]
        lengths = [max(map(len, col)) for col in zip(*grid_str)]
        format = ''.join('{{:{}}}'.format(x) for x in lengths)
        table = [format.format(*row) for row in grid_str]
        return '\n'.join(table)
    
    def __repr__(self) -> str:
        """Zwraca planszę w postaci stringa"""
        return self.__str__()

    def get_size(self) -> tuple:
        """Zwraca rozmiar planszy"""
        return self.__size.get_size()
    
    def get_area(self) -> int:
        """Zwraca powierzchnię planszy"""
        return self.__size.get_area()

    def get_max_pop(self) -> int:
        """Zwraca maksymalną liczbę zwierząt na planszy"""
        return self.__max_pop
    
    def get_total_object_count(self) -> int:
        """Zwraca liczbę wszystkich obiektów"""
        return self.__total_object_count
    
    def get_population(self) -> int:
        """Zwraca liczbę wszystkich zwierząt"""
        return self.__population
    
    def get_predators(self) -> int:
        """Zwraca liczbę drapieżników"""
        return self.__predators
    
    def get_preys(self) -> int:
        """Zwraca liczbę ofiar"""
        return self.__preys

    def get_beavers(self) -> int:
        """Zwraca liczbę bobrów"""
        return self.__beavers
    
    def __set_grid(self) -> None:
        """Ustawia planszę"""
        self.__grid = [[None for _ in range(self.__size.get_size()[0])] for _ in range(self.__size.get_size()[1])]
        for obj in self.__objects:
            self.__grid[obj.get_position()[1]][obj.get_position()[0]] = obj
    
    def get_grid(self) -> list:
        """Zwraca planszę"""
        self.__set_grid()
        return self.__grid
    
    def get_objects(self) -> set:
        """Zwraca zbiór wszystkich obiektów"""
        return self.__objects
    
    def get_round(self) -> int:
        """Zwraca numer rundy"""
        return self.__round

    def get_pop_data(self) -> list:
        """Zwraca dane o populacji w czasie"""
        return self.__pop_data

    def append_pop_data(self) -> None:
        """Dodaje dane o populacji w czasie"""
        self.__pop_data.append([self.get_round(), self.get_population(), self.get_predators(), self.get_preys(), self.get_beavers()])
    
    def add_random_object(self) -> None:
        """Dodaje losowy obiekt"""
        category = choice("animal", "item")
        if category == "animal":
            self.add_random_animal()
        else:
            self.add_random_item()

    def __generate_random_position(self) -> tuple:
        """Generuje losowe współrzędne"""
        x, y = randint(0, self.__size.get_size()[0] -1), randint(0, self.__size.get_size()[1] - 1)
        return (x, y)

    def add_random_animal(self, species=None) -> None:
        """Dodaje losowe zwierzę"""
        if species not in self.__possible_animals:
            raise Exception(species)
            species = choice(list(self.__possible_animals.keys()))
        
        x, y = self.__generate_random_position()

        animal = eval(species)(
            x=x,
            y=y,
            weight=uniform(0.1, 20),
            speed=randint(1, 5) if issubclass(eval(species), Prey) else randint(6, 10),
            age=0,
            thirst=100,
            satiety=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
            anger=randint(1, 10),
            hit_points=100
        )

        self.__objects.add(animal)

        if issubclass(animal.__class__, Predator):
            self.__predators += 1
        if issubclass(animal.__class__, Prey):
            self.__preys += 1
        if issubclass(animal.__class__, Beaver):
            self.__beavers += 1
        self.__population += 1
        self.__total_object_count += 1

    def add_random_item(self) -> None:
        """Dodaje losowy przedmiot"""

        category = choice(list(self.__possible_items.keys()))

        x, y = self.__generate_random_position()
        
        item = eval(category)(
            x=x,
            y=y,
            weight=uniform(0.1, 150),
            energy=randint(1, 10),
            durability=randint(1, 50),
        )

        self.__objects.add(item)
        self.__total_object_count += 1

    def add_predator(self) -> None:
        """Dodaje drapieżnika"""
        species = choice(["Wolf", "Eagle"])
        self.add_random_animal(species=species)

    def add_prey(self) -> None:
        """Dodaje ofiarę"""
        species = choice(["Deer", "Mouse"])
        self.add_random_animal(species=species)

    def add_beaver(self) -> None:
        """Dodaje bobra"""
        self.add_random_animal(species="Beaver")
    
    def populate(self, animal: Animal) -> None:
        """Dodaje zwierzę do planszy na podstawie innego zwierzęcia
        
        :param animal: zwierzę, na podstawie którego zostanie dodane nowe zwierzę
        """
        baby = eval(type(animal).__name__)(
            x=animal.get_position()[0],
            y=animal.get_position()[1],
            weight=uniform(0.1, 20),
            speed=randint(1, 5 * (self.__size.get_area()) % 100 + 1),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
            anger=randint(1, 10),
        )

        self.__objects.add(baby)
        self.__population += 1
        self.__total_object_count += 1
        if issubclass(baby.__class__, Predator):
            self.__predators += 1
        if issubclass(baby.__class__, Prey):
            self.__preys += 1
        if issubclass(baby.__class__, Beaver):
            self.__beavers += 1

    def remove(self, obj) -> None:
        """Usuwa obiekt z planszy
        
        :param obj: obiekt do usunięcia
        """
        self.__objects.remove(obj)

        if issubclass(obj.__class__, Predator):
            self.__predators -= 1
            self.__predators = max(self.__predators, 0)
            self.__population -= 1
        if issubclass(obj.__class__, Prey):
            if not obj.is_dead():
                self.__preys -= 1
                self.__preys = max(self.__preys, 0)
                self.__population -= 1
        if isinstance(obj, Beaver):
            self.__population -= 1
            self.__beavers -= 1
        self.__total_object_count -= 1
        self.__population = max(self.__population, 0)
        del obj

    def __scan_area_nearby(self, x: int, y: int, view_range: int) -> list:
        """Skanuje okolicę w zadanym zasięgu w poszukiwaniu obiektów
        
        :param x: współrzędna x
        :param y: współrzędna y
        :param view_range: zasięg widzenia
        :return: lista obiektów w zasięgu widzenia
        """
        objects_nearby = list(filter(lambda o: self.__calculate_range(x, y, *o.get_position()) <= view_range, self.__objects))
        return objects_nearby
    
    def __calculate_range(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Oblicza dystans między dwoma punktami
        
        :param x1: współrzędna x pierwszego punktu
        :param y1: współrzędna y pierwszego punktu
        :param x2: współrzędna x drugiego punktu
        :param y2: współrzędna y drugiego punktu
        :return: dystans między punktami
        """
        return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    
    def __correct_position(self, x: int, y: int) -> tuple:
        """Poprawia współrzędne obiektu, jeśli wyjdą poza planszę
        
        :param x: współrzędna x
        :param y: współrzędna y
        """
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        x = self.__size.get_size()[0] - 1 if x >= self.__size.get_size()[0] else x
        y = self.__size.get_size()[1] - 1 if y >= self.__size.get_size()[1] else y
        return (x, y)
    
    def __move_towards_object(self, src: Animal, dst: Object) -> tuple:
        """Przesuwa obiekt w kierunku innego obiektu
        
        :param src: obiekt, który ma się przesunąć
        :param dst: obiekt, w kierunku którego ma się przesunąć
        """
        distance = self.__calculate_range(*src.get_position(), *dst.get_position())
        if src.get_speed() >= distance:
            x, y = dst.get_position()
        else:
            x, y = move_towards_point(*src.get_position(), *dst.get_position(), src.get_speed())
            x, y = self.__correct_position(x, y)
        return (x, y)
    
    def update(self) -> None:
        """Aktualizuje stan planszy"""
        self.__round += 1  # zwiększamy licznik rund
        self.__set_grid()  # ustawiamy siatkę


        # aktualizujemy stan obiektów
        for obj in list(self.__objects):
            if obj not in self.__objects:
                # jeśli obiekt został usunięty, pomijamy go
                continue

            if issubclass(obj.__class__, Animal):
                # jeśli obiekt jest zwierzęciem, aktualizujemy jego stan

                if issubclass(obj.__class__, Predator):
                    if obj.get_age() >= randint(50, 100):
                        self.remove(obj)
                        logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has died of old age: {obj.get_age()} ]')
                        continue
                elif issubclass(obj.__class__, Prey):
                    if obj.get_age() >= randint(40, 100):
                        self.remove(obj)
                        logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has died of old age: {obj.get_age()} ]')
                        continue
                elif issubclass(obj.__class__, Beaver):
                    if obj.get_age() >= randint(15, 20):
                        logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has died of old age: {obj.get_age()} ]')
                        continue

                x, y = obj.get_position()
                if obj.get_hit_points() <= 0:
                    # jeśli zwierzę nie ma już punktów życia, usuwamy go
                    if not issubclass(obj.__class__, Prey):
                        self.remove(obj)
                        logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has been removed ]')
                    else:
                        obj.die()
                        self.__preys -= 1
                        self.__preys = max(self.__preys, 0)
                        self.__population -= 1
                        logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has died ]')
                    continue

                # rozglądamy się w poszukiwaniu obiektów w zasięgu widzenia
                objects_nearby = self.__scan_area_nearby(*obj.get_position(), obj.get_view_range())

                # sprawdzamy, jakie obiekty są w zasięgu widzenia
                for object_nearby in objects_nearby:
                    if object_nearby not in self.__objects:
                        # jeśli obiekt nie istnieje, pomijamy go
                        continue
                    if objects_nearby is obj:
                        # jeśli obiekt jest sam ze sobą, pomijamy go
                        continue
                    elif issubclass(obj.__class__, Prey) and issubclass(object_nearby.__class__, Predator):
                        # jeśli obiekt jest ofiarą, a obiekt w zasięgu widzenia jest drapieżnikiem, uciekamy
                        if object_nearby.get_hit_points() <= 0:
                            # jeśli drapieżnik nie ma już punktów życia, pomijamy go
                            self.remove(object_nearby)
                            logging.info(f'[ Round {self.get_round()}: {type(object_nearby).__name__}{object_nearby.get_position()} has been removed ]')
                            continue
                        if obj.get_position() == object_nearby.get_position():
                            # jeśli ofiara i drapieżnik są w tym samym miejscu, atakujemy
                            obj.defend(object_nearby)
                            logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} defends against {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        else:
                            # uciekamy
                            x, y = obj.run(object_nearby)
                            x, y = self.__correct_position(x, y)
                            logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} runs away from {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        break
                    elif issubclass(obj.__class__, Predator) and issubclass(object_nearby.__class__, Prey) and obj.get_satiety() < 70:
                        # jeśli obiekt jest drapieżnikiem, a obiekt w zasięgu widzenia jest ofiarą, atakujemy
                        if obj.get_position() == object_nearby.get_position():
                            if object_nearby.get_hit_points() <= 0:
                                # jeśli ofiara nie ma już punktów życia, zjadamy ją
                                obj.eat(object_nearby)
                                self.remove(object_nearby)
                                logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has eaten {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                            else:
                                # jeśli ofiara ma jeszcze punkty życia, atakujemy
                                obj.attack(object_nearby)
                                logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has attacked {type(object_nearby).__name__}{object_nearby.get_position()} ]')

                                if object_nearby.get_hit_points() <= 0:
                                    # jeśli ofiara nie ma już punktów życia, zjadamy ją
                                    obj.eat(object_nearby)
                                    self.remove(object_nearby)
                                    logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has eaten {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        else:
                            # polujemy na ofiarę
                            x, y = obj.hunt(object_nearby)
                            x, y = self.__move_towards_object(obj, object_nearby)
                            logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} hunts {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        break
                    elif isinstance(obj, Beaver) and isinstance(object_nearby, Tree) and obj.get_satiety() < 50:
                        # jeśli obiekt jest bobrem, a obiekt w zasięgu widzenia jest drzewem, jemy je
                        if obj.get_position() == object_nearby.get_position():
                            obj.eat(object_nearby)
                            self.remove(object_nearby)
                            logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has eaten {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        else:
                            # poruszamy się w kierunku drzewa
                            x, y = self.__move_towards_object(obj, object_nearby)
                        break
                    elif issubclass(obj.__class__, Prey) and isinstance(object_nearby, Plant) and obj.get_satiety() < 70:
                        # jeśli obiekt jest ofiarą, a obiekt w zasięgu widzenia jest rośliną, jemy ją
                        if obj.get_position() == object_nearby.get_position():
                            obj.eat(object_nearby)
                            self.remove(object_nearby)
                            logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has eaten {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        else:
                            # poruszamy się w kierunku rośliny
                            x, y = self.__move_towards_object(obj, object_nearby)
                        break
                    elif isinstance(object_nearby, Water):
                        # jeśli obiekt jest wodą, pijemy ją
                        if obj.get_thirst() >= 70:
                            # jeśli zwierzę jest nawodnione, pomijamy ją
                            continue
                        if obj.get_position() == object_nearby.get_position():
                            # jeśli zwierzę jest w tym samym miejscu, pijemy
                            obj.drink(object_nearby)
                            self.remove(object_nearby)
                            logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has drunk {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                        else:
                            # poruszamy się w kierunku wody
                            x, y = self.__move_towards_object(obj, object_nearby)
                        break
                    # jeśli obiekt jest tego samego typu oraz maksymalna populacja na to pozwala, próbujemy się rozmnożyć
                    elif obj.can_reproduce_with(object_nearby):
                        if isinstance(obj, Predator) and self.get_predators() >= 0.6 * self.get_population():
                            break
                        if isinstance(obj, Prey) and self.get_preys() >= 0.6 * self.get_population():
                            break
                        if isinstance(obj, Beaver) and self.get_beavers() >= 0.6 * self.get_population():
                            break
                        if self.get_population() >= self.get_max_pop():
                            break
                        if obj.get_position() == object_nearby.get_position():
                            if obj.can_have_child() and object_nearby.can_have_child():
                                if obj.can_have_triplets() or object_nearby.can_have_triplets():
                                    self.populate(obj)
                                    self.populate(obj)
                                    self.populate(obj)
                                    logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has reproduced with {type(object_nearby).__name__}{object_nearby.get_position()} and had triplets ]')
                                elif obj.can_have_twins() or object_nearby.can_have_twins():
                                    self.populate(obj)
                                    self.populate(obj)
                                    logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has reproduced with {type(object_nearby).__name__}{object_nearby.get_position()} and had twins ]')
                                else:
                                    self.populate(obj)
                                    logging.info(f'[ Round {self.get_round()}: {type(obj).__name__}{obj.get_position()} has reproduced with {type(object_nearby).__name__}{object_nearby.get_position()} ]')
                            x, y = move_away_from_point(*obj.get_position(), *object_nearby.get_position(), int(obj.get_speed()))
                            x, y = self.__correct_position(x, y)
                        else:
                            # poruszamy się w kierunku partnera
                            x, y = self.__move_towards_object(obj, object_nearby)
                        break
                else:
                    # jeśli nie znaleziono żadnego obiektu w zasięgu widzenia, losowo poruszamy się po mapie
                    x, y = randint(1, self.__size.get_size()[0] - 1), randint(1, self.__size.get_size()[1] - 1)
                    x, y = move_towards_point(*obj.get_position(), x, y, int(obj.get_speed()))
                    x, y = self.__correct_position(x, y)

                # zwiększamy wiek zwierzęcia i poruszamy się
                obj.set_age(obj.get_age() + 1)
                obj.move(x, y)
        
        # jeśli liczba obiektów nieożywionych jest mniejsza niż 70% powierzchni mapy, dodajemy losowe obiekty
        if self.__total_object_count - self.__population < 70 * self.get_area() // 100:
            self.add_random_item()

        # ustawiamy siatkę
        self.__set_grid()


    def check_end_conditions(self) -> bool:
        """Sprawdza warunki końcowe.
        Symulacja kończy się, gdy:
        - liczba ofiar jest równa 0
        - liczba drapieżników jest równa 0
        - cała populacja jest równa 0
        """

        self.append_pop_data()

        if self.__population <= 0:
            logging.info(f'[ Round {self.get_round()}: Simulation has ended - All animals have died ]')
            return "Wszystkie zwierzęta umarły"
        if self.__predators <= 0:
            logging.info(f'[ Round {self.get_round()}: Simulation has ended - All predators have died ]')
            return "Wszystkie drapieżniki umarły"
        if self.__preys <= 0:
            logging.info(f'[ Round {self.get_round()}: Simulation has ended - All preys have died ]')
            return "Wszystkie ofiary umarły"
        return False

from copy import deepcopy
from random import randint, choice, uniform
import math

from ecosystem_simulation.objects.items import *
from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.beaver import Beaver
from ecosystem_simulation.objects.animals.predators import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.utils import *


"""
TODO:

    - [ ] dodać komentarze
    - [ ] dodać testy
    - [ ] dodać dokumentację
    - [ ] zamienić nazwy obiektów w siatce na odpowiednie emoji (np. 🐺)
    - [ ] dodać możliwość zapisu i wczytywania stanu symulacji (pickle)
    - [ ] dodać generowanie logów do pliku (logging)
    - [ ] dodać metody dodawania osobno drapieżników, ofiar i bobrów

"""


class BoardSize:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height

    def get_size(self) -> tuple:
        """Zwraca rozmiar planszy"""
        return (self.__width, self.__height)
    
    def get_area(self) -> int:
        """Zwraca powierzchnię planszy"""
        return self.__width * self.__height
    

class Board:
    
    __total_object_count = 0
    __population = 0
    __predators = 0
    __preys = 0
    __grid = []
    __objects = set()
    __round = 0
    __size = None

    __possible_animals = {
        "Mouse": Mouse,
        "Deer": Deer,
        "Wolf": Wolf,
        "Eagle": Eagle,
        "Beaver": Beaver
    }

    __possible_items = {
        "Tree": Tree,
        # "Rock": Rock,
        "Plant": Plant,
        "Water": Water
    }

    def __init__(self, size: BoardSize) -> None:
        self.__size = size
        self.__grid = [[None for _ in range(self.__size.get_size()[0])] for _ in range(self.__size.get_size()[1])]

    def __str__(self) -> str:
        grid_str = [[str(cell) if cell is not None else name_to_emoji("Dirt") for cell in row] for row in self.get_grid()]
        lengths = [max(map(len, col)) for col in zip(*grid_str)]
        format = ''.join('{{:{}}}'.format(x) for x in lengths)
        table = [format.format(*row) for row in grid_str]
        return '\n'.join(table)
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_size(self) -> tuple:
        """Zwraca rozmiar planszy"""
        return self.__size.get_size()
    
    def get_area(self) -> int:
        """Zwraca powierzchnię planszy"""
        return self.__size.get_area()
    
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
    
    def __set_grid(self) -> None:
        """Ustawia planszę"""
        self.__grid = [[None for _ in range(self.__size.get_size()[0])] for _ in range(self.__size.get_size()[1])]
        for obj in self.__objects:
            self.__grid[obj.get_position()[1]][obj.get_position()[0]] = obj
    
    def get_grid(self) -> list:
        """Zwraca planszę"""
        self.__set_grid()
        return deepcopy(self.__grid)
    
    def get_objects(self) -> set:
        """Zwraca zbiór wszystkich obiektów"""
        return deepcopy(self.__objects)
    
    def get_round(self) -> int:
        """Zwraca numer rundy"""
        return self.__round
    
    def add_random_object(self) -> None:
        """Dodaje losowy obiekt"""
        category = choice("animal", "item")
        if category == "animal":
            self.add_random_animal()
        else:
            self.add_random_item()

    def __generate_random_position(self) -> tuple:
        """Generuje losowe współrzędne"""
        retry = 0
        while True and retry < 10:
            x, y = randint(0, self.__size.get_size()[0] -1), randint(0, self.__size.get_size()[1] - 1)
            if self.get_grid()[y][x] is None:
                return (x, y)
            retry += 1
        else:
            return (-1, -1)

    def add_random_animal(self) -> None:
        """Dodaje losowe zwierzę"""
        species = choice(list(self.__possible_animals.keys()))
        
        x, y = self.__generate_random_position()
        if x == -1 or y == -1:
            return # TODO: raise exception

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
        self.__population += 1
        self.__total_object_count += 1

    def add_random_item(self) -> None:
        """Dodaje losowy przedmiot"""
        category = choice(list(self.__possible_items.keys()))

        x, y = self.__generate_random_position()
        if x == -1 or y == -1:
            return # TODO: raise exception
        
        item = eval(category)(
            x=x,
            y=y,
            weight=uniform(0.1, 150),
            energy=randint(1, 10),
            durability=randint(1, 50),
        )

        self.__objects.add(item)
        self.__total_object_count += 1
    
    def populate(self, animal: Animal) -> None:
        """Dodaje zwierzę do planszy"""
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
        self.__grid[baby.get_position()[1]][baby.get_position()[0]] = baby
        self.__population += 1
        self.__total_object_count += 1
        if issubclass(baby.__class__, Predator):
            self.__predators += 1
        if issubclass(baby.__class__, Prey):
            self.__preys += 1

    def remove(self, obj) -> None:
        """Usuwa zwierzę z planszy"""
        # if obj in self.__objects:
        # print(f"Usuwanie {obj} z planszy [{obj in self.__objects}]")
        self.__objects.remove(obj)
        # print(f"Usunięto {obj} z planszy [{obj in self.__objects}]")

        if issubclass(obj.__class__, Predator):
            self.__predators -= 1
            self.__population -= 1
        if issubclass(obj.__class__, Prey):
            self.__preys -= 1
            self.__population -= 1
        if isinstance(obj, Beaver):
            self.__population -= 1
        self.__total_object_count -= 1
        del obj

    def __scan_area_nearby(self, x: int, y: int, view_range: int) -> list:
        """Skanuje okolicę"""
        objests_nearby = []
        self.__set_grid()
        for i in range(x - view_range, x + view_range + 1):
            for j in range(y - view_range, y + view_range + 1):
                    try:
                        if i == x and j == y:
                            continue
                        if self.__grid[j][i] is not None:
                            objests_nearby.append(self.__grid[j][i])
                    except IndexError:
                        # indeks może wykorczyć poza zakres co spowoduje
                        # wyrzucenie wyjątku. Jeśli wyjątek wystąpi,
                        # wyłapujemy go i ignorujemy
                        pass
        return objests_nearby
    
    def __calculate_range(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Oblicza dystans"""
        return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    
    def __correct_position(self, x: int, y: int) -> tuple:
        """Poprawia współrzędne"""
        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        x = self.__size.get_size()[0] - 1 if x >= self.__size.get_size()[0] else x
        y = self.__size.get_size()[1] - 1 if y >= self.__size.get_size()[1] else y
        return (x, y)
    
    def __move_towards_object(self, src: Animal, dst: Object) -> tuple:
        """Przesuwa obiekt w kierunku innego obiektu"""
        distance = self.__calculate_range(*src.get_position(), *dst.get_position())
        if src.get_speed() >= distance:
            x, y = dst.get_position()
        else:
            x, y = move_towards_point(*src.get_position(), *dst.get_position(), src.get_speed())
            x, y = self.__correct_position(x, y)
        # print(f"{str(src)}{src.get_position()}: Move towards {str(dst)}{dst.get_position()}")
        return (x, y)
    
    def update(self) -> None:
        """Aktualizuje stan planszy"""
        self.__round += 1
        self.__set_grid()
        for obj in list(self.__objects):
            if obj not in self.__objects:
                continue
            if issubclass(obj.__class__, Animal):
                x, y = obj.get_position()
                if obj.get_hit_points() <= 0:
                    if not issubclass(obj.__class__, Prey):
                        self.remove(obj)
                    continue
                objects_nearby = sorted(self.__scan_area_nearby(*obj.get_position(), obj.get_view_range()), key=lambda o: self.__calculate_range(*obj.get_position(), *o.get_position()))
                for object_nearby in objects_nearby:
                    if object_nearby not in self.__objects:
                        continue
                    if objects_nearby is obj:
                        continue
                    if issubclass(obj.__class__, Prey) and issubclass(object_nearby.__class__, Predator):
                        # print(f"{str(obj)}: Run")
                        if object_nearby.get_hit_points() <= 0:
                            self.remove(object_nearby)
                            continue
                        if obj.get_position() == object_nearby.get_position():
                            obj.defend(object_nearby)
                            # print(f"{str(obj)}: Defend")
                        else:
                            x, y = obj.run(object_nearby)
                            x, y = self.__correct_position(x, y)
                            # obj.move(x, y)
                            # print(f"{str(obj)}: Run")
                        break
                    elif issubclass(obj.__class__, Predator) and issubclass(object_nearby.__class__, Prey):
                        # print(f"{str(obj)}: Attack")
                        if obj.get_position() == object_nearby.get_position():
                            if object_nearby.get_hit_points() <= 0:
                                obj.eat(object_nearby)
                                self.remove(object_nearby)
                                # print(f"{str(obj)}: Eat")
                            else:
                                obj.attack(object_nearby)
                                # print(f"{str(obj)}{obj.get_position()}[hp={obj.get_hit_points()}]: Attack {str(object_nearby)}{object_nearby.get_position()}[hp={object_nearby.get_hit_points()}]")
                        else:
                            x, y = obj.hunt(object_nearby)
                            
                            x, y = self.__move_towards_object(obj, object_nearby)
                        break
                    elif isinstance(obj, Beaver) and isinstance(object_nearby, Tree):
                        # print(f"{str(obj)}: Eat")
                        if obj.get_position() == object_nearby.get_position():
                            obj.eat(object_nearby)
                            self.remove(object_nearby)
                            # print(f"{str(obj)}: Eat")
                        else:
                            x, y = self.__move_towards_object(obj, object_nearby)
                            # obj.move(x, y)
                        break
                    elif issubclass(obj.__class__, Prey) and isinstance(object_nearby, Plant):
                        # print(f"{str(obj)}: Eat")
                        if obj.get_position() == object_nearby.get_position():
                            obj.eat(object_nearby)
                            self.remove(object_nearby)
                            # print(f"{str(obj)}: Eat")
                        else:
                            x, y = self.__move_towards_object(obj, object_nearby)
                            # obj.move(x, y)
                        break
                    elif isinstance(object_nearby, Water):
                        # print(f"{str(obj)}: Drink")
                        if obj.get_thirst() >= 90:
                            continue
                        if obj.get_position() == object_nearby.get_position():
                            obj.drink(object_nearby)
                            # self.remove(object_nearby)
                        else:
                            x, y = self.__move_towards_object(obj, object_nearby)
                            # obj.move(x, y)
                        break
                    elif obj.__class__ == object_nearby.__class__:
                        # print(f"{str(obj)}: Reproduce")
                        if obj.can_reproduce_with(object_nearby):
                            if obj.get_position() == object_nearby.get_position():
                                self.populate(obj)
                            else:
                                
                                x, y = self.__move_towards_object(obj, object_nearby)
                                # obj.move(x, y)
                            break
                else:
                    x, y = randint(1, self.__size.get_size()[0] - 1), randint(1, self.__size.get_size()[1] - 1)
                    x, y = move_towards_point(*obj.get_position(), x, y, obj.get_speed())
                    x, y = self.__correct_position(x, y)
                    # obj.move(x, y)
                    # print(f"{str(obj)}: Random move")
                obj.set_age(obj.get_age() + 1)
                obj.move(x, y)
        if self.__total_object_count - self.__population < 5 * self.get_area() // 100:
            self.add_random_item()
        self.__set_grid()


    def check_end_conditions(self) -> bool:
        """Sprawdza warunki końcowe"""
        if self.__population == 0:
            # raise Exception("Population number is: ", self.__population)
            # print("Population number is: ", self.__population)
            return f"Population number is: {self.__population}"
        if self.__predators == 0:
            # raise Exception("Predators number is: ", self.__predators)
            # print("Predators number is: ", self.__predators)
            return f"Predators number is: {self.__predators}"
        if self.__preys == 0:
            # raise Exception("Preys number is: ", self.__preys)
            # print("Preys number is: ", self.__preys)
            return f"Preys number is: {self.__preys}"
        return False

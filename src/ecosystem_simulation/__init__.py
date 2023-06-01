from copy import deepcopy
from random import randint, choice, uniform
import pickle, platform, os, math, time, logging

"""
TODO:

    - [ ] zaimplementować metody planszy odpowiedzialne za właściwe działanie symulacji
    - [ ] podzielić plik na mniejsze i ustrukturyzować
    - [ ] dodać komentarze
    - [ ] dodać testy
    - [ ] dodać dokumentację
    - [ ] zamienić nazwy obiektów w siatce na emoji
    - [ ] dodać możliwość zapisu i wczytywania stanu symulacji (pickle)
    - [ ] dodać generowanie logów do pliku (logging)
    - [ ] dodać metody dodawania osobno drapieżników, ofiar i bobrów

"""

def move_towards_point(x: int, y: int, x2: int, y2: int, distance: int) -> tuple:
        """Przesuwa się w kierunku punktu"""
        if x2 == x and y2 == y:
            return (x, y)
        if x2 == x:
            if y2 > y:
                return (x, y + distance)
            else:
                return (x, y - distance)
        if y2 == y:
            if x2 > x:
                return (x + distance, y)
            else:
                return (x - distance, y)
        if x2 > x:
            if y2 > y:
                return (x + distance, y + distance)
            else:
                return (x + distance, y - distance)
        else:
            if y2 > y:
                return (x - distance, y + distance)
            else:
                return (x - distance, y - distance)
            
def move_away_from_point(x: int, y: int, x2: int, y2: int, distance: int) -> tuple:
    """Przesuwa się zdala od punktu"""
    if x2 == x and y2 == y:
        return (x, y)
    if x2 == x:
        if y2 > y:
            return (x, y - distance)
        else:
            return (x, y + distance)
    if y2 == y:
        if x2 > x:
            return (x - distance, y)
        else:
            return (x + distance, y)
    if x2 > x:
        if y2 > y:
            return (x - distance, y - distance)
        else:
            return (x - distance, y + distance)
    else:
        if y2 > y:
            return (x + distance, y - distance)
        else:
            return (x + distance, y + distance)

####### OBJECTS #######

class Object:
    __hashcode = None

    def __init__(self, x: int, y: int, weight: float) -> None:
        self.__x = x
        self.__y = y
        self.__weight = weight
        self.__hashcode = id(self)

    def get_position(self) -> tuple:
        """Zwraca współrzędne obiektu"""
        return self.__x, self.__y
    
    def set_position(self, x: int, y: int) -> None:
        """Ustawia współrzędne obiektu"""
        self.__x = x
        self.__y = y
    
    def get_weight(self) -> tuple:
        """Zwraca wagę obiektu"""
        return self.__weight
    
    def __str__(self) -> str:
        return str(type(self).__name__)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_hit_points(self):
        pass

    def __hash__(self) -> int:
        return self.__hashcode
    

####### ITEMS #######


class Item(Object):
    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        super().__init__(x, y, weight)
        self.__energy = energy
        self.__durability = durability

    def get_energy(self) -> int:
        """Zwraca ilość energii, jaką dostarcza jedzenie"""
        return self.__energy
    
    def get_durability(self) -> int:
        """Zwraca trwałość przedmiotu"""
        return self.__durability
    

class Plant(Item):
    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        super().__init__(x, y, weight, energy, durability)


class Water(Item):
    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        super().__init__(x, y, weight, energy, durability)


class Tree(Item):
    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        super().__init__(x, y, weight, energy, durability)


# class Rock(Item):
#     def __init__(self, x: int, y: int, weight: float, energy: int,
#                  durability: int) -> None:
#         super().__init__(x, y, weight, energy, durability)


####### ANIMALS #######
 

GENDER_MALE = True
GENDER_FEMALE = False


class Animal(Object):
    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                strenght: int, hit_points: int = 100) -> None:
        super().__init__(x, y, weight)
        self.__speed = speed
        self.__age = age
        self.__thirst = thirst
        self.__satiety = satiety
        self.__gender = gender
        self.__view_range = view_range
        self.__hit_points = hit_points
        self.__strenght = strenght

    def get_speed(self) -> float:
        """Zwraca prędkość zwierzęcia"""
        return self.__speed
    
    def get_age(self) -> int:
        """Zwraca wiek zwierzęcia"""
        return self.__age
    
    def set_age(self, age: int) -> None:
        """Ustawia wiek zwierzęcia"""
        self.__age = age
    
    def get_satiety(self) -> int:
        """Zwraca poziom sytości zwierzęcia"""
        return self.__satiety
    
    def set_satiety(self, satiety: int) -> None:
        """Ustawia poziom sytości zwierzęcia"""
        self.__satiety = satiety

    def get_thirst(self) -> int:
        """Zwraca poziom pragnienia zwierzęcia"""
        return self.__thirst
    
    def get_gender(self) -> int:
        """Zwraca płeć zwierzęcia"""
        return self.__gender
    
    def get_view_range(self) -> int:
        """Zwraca zasięg widzenia zwierzęcia"""
        return self.__view_range
    
    def get_hit_points(self) -> int:    
        """Zwraca punkty życia zwierzęcia"""
        return self.__hit_points
    
    def get_strenght(self) -> int:
        """Zwraca siłę zwierzęcia"""
        return self.__strenght
    
    def move(self, x: int, y: int) -> None:
        """Przesuwa zwierzę na podane współrzędne"""
        energy_lost = int((abs(self.get_position()[0] - x) + abs(self.get_position()[1] - y)) % 10)
        if self.__satiety == 0 or self.__thirst == 0:
            self.__hit_points -= energy_lost
            self.__hit_points = int(max(self.__hit_points, 0))
        else:
            self.__satiety -= energy_lost
            self.__thirst -= energy_lost
            self.__satiety = max(self.__satiety, 0)
            self.__thirst = max(self.__thirst, 0)
        self.set_position(x, y)

    def eat(self, food: Plant) -> None:
        """Zwiększa poziom sytości zwierzęcia o wagę jedzenia"""
        self.set_satiety((food.get_weight() * food.get_energy()) % 100)

    def drink(self, water: Water) -> None:
        """Zwiększa poziom sytości zwierzęcia o wagę wody"""
        self.__thirst += water.get_weight() % 100

    def can_reproduce_with(self, partner) -> bool:
        """Zwraca True, jeśli zwierzęta mogą się rozmnażać"""
        if type(self).__name__ == type(partner).__name__:
            if self.get_gender() != self.get_gender():
                if self.get_age() >= 5 and partner.get_age() >= 5:
                    if self.get_hit_points() >= 0 and partner.get_hit_points() >= 0:
                        return True
        return False

    def get_durability(self) -> int:
        """Zwraca trwałość atrybutu ataku lub obrony zwierzęcia"""
        return 0

    def set_durability(self, damage_points: int) -> int:
        """Zadaje zwierzęciu obrażenia"""
        return damage_points

    def set_damage(self, points: int) -> None:
        """Zadaje zwierzęciu obrażenia"""
        points = int(self.set_durability(points))
        self.__hit_points -= points
        self.__hit_points = int(max(self.__hit_points, 0))

    def make_sound(self) -> int:
        """Zwraca głośność wydawanego przez zwierzę dźwięku"""
        return 0


class Beaver(Animal):
    __teeth_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, hit_points: int = 100, **kwargs) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, hit_points)
        
    def eat(self, tree: Tree) -> None:
        """Zjada drzewo"""
        self.set_satiety((tree.get_weight() * tree.get_energy()) % 100)
        self.__teeth_durability -= tree.get_durability() // 100

    def get_teeth_durability(self) -> int:
        """Zwraca trwałość zębów"""
        return self.__teeth_durability
    
    def set_durability(self, damage_points: int) -> int:
        """Zadaje zwierzęciu obrażenia"""
        points = damage_points - self.__teeth_durability
        self.__teeth_durability -= damage_points
        self.__teeth_durability = max(self.__teeth_durability, 0)
        return max(points, 0)
    
    def get_durability(self) -> int:
        """Zwraca trwałość atrybutu ataku lub obrony zwierzęcia"""
        return self.get_teeth_durability()
    

class Predator(Animal):

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, anger: int, hit_points: int = 100) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, hit_points)
        self.__anger = anger

    def get_anger(self) -> int:
        """Zwraca poziom złości"""
        return self.__anger
    
    def hunt(self, prey: Animal) -> tuple:
        """Atakuje ofiarę"""
        self.__anger += prey.make_sound()
        x, y = move_towards_point(*self.get_position(), *prey.get_position(), self.get_speed())
        return x, y

    def attack(self, prey: Animal) -> None:
        """Zadaje obrażenia"""
        prey.set_damage(int(self.get_strenght() + self.get_weight() + self.get_anger()))

    def make_sound(self) -> int:
        return int(self.get_anger() + self.get_weight() + self.get_strenght())
    
    def eat(self, prey: Animal) -> None:
        """Zjada ofiarę"""
        satiety = self.get_satiety()
        satiety += int(prey.get_weight())
        self.set_satiety(max(satiety, 100))
        self.__anger -= int(prey.get_weight()) % 100


class Prey(Animal):
    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, fear: int, hit_points: int = 100) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, hit_points)
        self.__fear = fear

    def get_fear(self) -> int:
        """Zwraca poziom strachu"""
        return self.__fear
    
    def run(self, predator) -> None:
        """Ucieka przed drapieżnikiem"""
        self.__fear += predator.make_sound()
        x, y = move_away_from_point(*self.get_position(), *predator.get_position(), self.get_speed())
        return x, y

    def defend(self, predator) -> None:
        """Obronić się przed drapieżnikiem"""
        predator.set_damage(int(self.get_strenght() + self.get_weight() + self.get_fear()))

    def make_sound(self) -> int:
        return self.get_fear() + self.get_weight() + self.get_strenght()


class Wolf(Predator):
    __claws_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, anger: int, hit_points: int = 100, **kwargs) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, anger, hit_points)
        
    def roar(self) -> int:
        """Wydać dźwięk"""
        return 20

    def get_claws_durability(self) -> int:
        """Zwraca trwałość pazurów"""
        return self.__claws_durability
    
    def get_durability(self) -> int:
        return self.get_claws_durability()
    
    def set_durability(self, damage_points: int) -> int:
        """Zadaje zwierzęciu obrażenia"""
        points = damage_points - self.__claws_durability
        self.__claws_durability -= damage_points
        self.__claws_durability = max(self.__claws_durability, 0)
        return max(points, 0)
    
    def make_sound(self) -> int:
        return super().make_sound() + self.roar()
    
class Eagle(Predator):
    __beak_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, anger: int, hit_points: int = 100, **kwargs) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght, anger)
        
    def screech(self) -> int:
        """Wydać dźwięk"""
        return 10

    def get_beak_durability(self) -> int:
        """Zwraca trwałość dzioba"""
        return self.__beak_durability
    
    def get_durability(self) -> int:
        return self.get_beak_durability()
    
    def set_durability(self, damage_points: int) -> int:
        """Zadaje zwierzęciu obrażenia"""
        points = damage_points - self.__beak_durability
        self.__beak_durability -= damage_points
        self.__beak_durability = max(self.__beak_durability, 0)
        return max(points, 0)
    
    def make_sound(self) -> int:
        return super().make_sound() + self.screech()
    
class Mouse(Prey):

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, fear: int, hit_points: int = 100, **kwargs) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, fear, hit_points)
        
    def squeak(self) -> int:
        """Wydać dźwięk"""
        return 1

    def get_durability(self) -> int:
        return 0
    
    def set_durability(self, damage_points: int) -> int:
        return damage_points
    
    def make_sound(self) -> int:
        return super().make_sound() + self.squeak()


class Deer(Prey):
    __antlers_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, fear: int, hit_points: int = 100, **kwargs) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, fear, hit_points)
        
    def yell(self) -> int:
        """Wydać dźwięk"""
        return 10

    def get_antlers_durability(self) -> int:
        """Zwraca trwałość poroża"""
        return self.__antlers_durability
    
    def get_durability(self) -> int:
        return self.get_antlers_durability()
    
    def set_durability(self, damage_points: int) -> int:
        """Zadaje zwierzęciu obrażenia"""
        points = damage_points - self.__antlers_durability
        self.__antlers_durability -= damage_points
        self.__antlers_durability = max(self.__antlers_durability, 0)
        return max(points, 0)
    
    def make_sound(self) -> int:
        return super().make_sound() + self.yell()
    

###### BOARD ######


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
        grid_str = [[str(cell) if cell is not None else " " for cell in row] for row in self.get_grid()]
        lengths = [max(map(len, col)) for col in zip(*grid_str)]
        format = '\t'.join('{{:{}}}'.format(x) for x in lengths)
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
        print(f"Usuwanie {obj} z planszy [{obj in self.__objects}]")
        self.__objects.remove(obj)
        print(f"Usunięto {obj} z planszy [{obj in self.__objects}]")

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
            print("Population number is: ", self.__population)
            return True
        if self.__predators == 0:
            # raise Exception("Predators number is: ", self.__predators)
            print("Predators number is: ", self.__predators)
            return True
        if self.__preys == 0:
            # raise Exception("Preys number is: ", self.__preys)
            print("Preys number is: ", self.__preys)
            return True
        return False


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

    for _ in range(50):
        board.add_random_animal()

    for _ in range(40):
        board.add_random_item()

    print(board)

    clear_screen_cmd = "cls" if platform.system() == "Windows" else "clear"

    while not board.check_end_conditions():
        os.system(clear_screen_cmd)
        print(board)
        board.update()
        objects = list(sorted((f"{o}{o.get_position()}[hp={o.get_hit_points()}]" for o in board.get_objects())))
        print(objects)
        print("Population = ", board.get_population())
        print("Predators = ", board.get_predators())
        print("Preys = ", board.get_preys())
        # input(f"End = {board.check_end_conditions()}")
        time.sleep(0.4)
    
    # board.update()
    # print(board)
    print(board.get_objects())

    s = set()
    s.add(predator)
    l = list(s)
    print(predator in s)
    print(predator in l)

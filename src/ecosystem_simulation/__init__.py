####### OBJECTS #######

class Object:
    def __init__(self, x: int, y: int, weight: float) -> None:
        self.__x = x
        self.__y = y
        self.__weight = weight

    def get_coordinates(self) -> tuple:
        """Zwraca współrzędne obiektu"""
        return self.__x, self.__y
    
    def get_weight(self) -> tuple:
        """Zwraca wagę obiektu"""
        return self.__weight
    

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


class Rock(Item):
    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        super().__init__(x, y, weight, energy, durability)


####### ANIMALS #######
 

GENDER_MALE = True
GENDER_FEMALE = False


class Animal(Object):
    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int) -> None:
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
        energy_lost = (abs(self.__x - x) + abs(self.__y - y)) * (self.__weight + self.__speed)
        if self.__satiety == 0 or self.__thirst == 0:
            self.__hit_points -= energy_lost
            self.__hit_points = max(self.__hit_points, 0)
        else:
            self.__satiety -= energy_lost
            self.__thirst -= energy_lost
            self.__satiety = max(self.__satiety, 0)
            self.__thirst = max(self.__thirst, 0)
        self.__x = x
        self.__y = y

    def eat(self, food: Plant) -> None:
        """Zwiększa poziom sytości zwierzęcia o wagę jedzenia"""
        self.__satiety += (food.get_weight() * food.get_energy()) % 100

    def drink(self, water: Water) -> None:
        """Zwiększa poziom sytości zwierzęcia o wagę wody"""
        self.__thirst += water.get_weight() % 100

    def reproduce(self, partner: Animal) -> Animal:
        """Tworzy nowe zwierzę na podstawie dwóch rodziców"""
        pass


class Beaver(Animal):
    __teeth_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght)
        
    def eat(tree: Tree) -> None:
        """Zjada drzewo"""
        self.__satiety += (tree.get_weight() * tree.get_energy()) % 100
        self.__teeth_durability -= tree.get_durability() / 100

    def get_teeth_durability(self) -> int:
        """Zwraca trwałość zębów"""
        return self.__teeth_durability
    

class Predator(Animal):

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int, anger: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght)
        self.__anger = anger

    def get_anger(self) -> int:
        """Zwraca poziom złości"""
        return self.__anger
    
    def hunt(self, prey: Prey) -> None:
        """Atakuje ofiarę"""
        pass


class Prey(Animal):
    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int, fear: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght)
        self.__fear = fear

    def get_fear(self) -> int:
        """Zwraca poziom strachu"""
        return self.__fear
    
    def run(self, predator: Predator) -> None:
        """Ucieka przed drapieżnikiem"""
        pass

    def defend(self, predator: Predator) -> None:
        """Obronić się przed drapieżnikiem"""
        pass


class Wolf(Predator):
    __claws_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int, anger: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght, anger)
        
    def roar(self) -> int:
        """Wydać dźwięk"""
        pass

    def get_claws_durability(self) -> int:
        """Zwraca trwałość pazurów"""
        return self.__claws_durability
    
class Eagle(Predator):
    __beak_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int, anger: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght, anger)
        
    def screech(self) -> int:
        """Wydać dźwięk"""
        pass

    def get_beak_durability(self) -> int:
        """Zwraca trwałość dzioba"""
        return self.__beak_durability
    
class Mouse(Prey):

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int, fear: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght, fear)
        
    def squeak(self) -> int:
        """Wydać dźwięk"""
        pass


class Deer(Prey):
    __antlers_durability = 100

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 hit_points: int, strenght: int, fear: int) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght, fear)
        
    def yell(self) -> int:
        """Wydać dźwięk"""
        pass

    def get_antlers_durability(self) -> int:
        """Zwraca trwałość poroża"""
        return self.__antlers_durability
    

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
    __grid = []
    __objects = set()
    __round = 0

    def __init__(self, size: BoardSize) -> None:
        self.__size = size
        self.__grid = [[None for _ in range(self.__size.get_size()[0])] for _ in range(self.__size.get_size()[1])]

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
    
    def get_grid(self) -> list:
        """Zwraca planszę"""
        return self.__grid
    
    def get_objects(self) -> set:
        """Zwraca zbiór wszystkich obiektów"""
        return self.__objects.copy()
    
    def get_round(self) -> int:
        """Zwraca numer rundy"""
        return self.__round
    
    def populate(self, animal: Animal) -> None:
        """Dodaje zwierzę do planszy"""
        pass

    def remove(self, animal: Animal) -> None:
        """Usuwa zwierzę z planszy"""
        pass

    def update(self) -> None:
        """Aktualizuje stan planszy"""
        pass

    def check_end_conditions(self) -> bool:
        """Sprawdza warunki końcowe"""
        pass

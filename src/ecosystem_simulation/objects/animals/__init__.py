import sys

sys.path.append('..')

from ecosystem_simulation.objects import Object
from ecosystem_simulation.objects.items import Plant, Water


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
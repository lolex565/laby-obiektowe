import sys

sys.path.append('..')

from . import Animal
from ecosystem_simulation.utils import move_towards_point
from ecosystem_simulation import *


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
        prey.set_damage(int(self.get_strenght() * self.get_anger() + self.get_weight()))

    def make_sound(self) -> int:
        return int(self.get_anger() + self.get_weight() + self.get_strenght())
    
    def eat(self, prey: Animal) -> None:
        """Zjada ofiarę"""
        satiety = self.get_satiety()
        satiety += int(prey.get_weight())
        self.set_satiety(max(satiety, 100))
        self.__anger -= int(prey.get_weight()) % 100


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

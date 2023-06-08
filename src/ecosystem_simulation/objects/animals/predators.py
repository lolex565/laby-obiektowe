import sys

sys.path.append('../..')

from . import Animal
from ecosystem_simulation.utils import move_towards_point
from ecosystem_simulation import *


class Predator(Animal):
    """Klasa bazowa dla drapieżników"""

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, anger: int, hit_points: int = 100) -> None:
        """Konstruktor klasy Predator
        
        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param speed: prędkość
        :param age: wiek
        :param thirst: poziom pragnienia
        :param satiety: poziom sytości
        :param gender: płeć
        :param view_range: zasięg widzenia
        :param strenght: siła
        :param anger: złość
        :param hit_points: punkty życia
        """
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, hit_points)
        self.__anger = anger

    def get_anger(self) -> int:
        """Zwraca poziom złości"""
        return self.__anger
    
    def hunt(self, prey: Animal) -> tuple:
        """Atakuje ofiarę
        
        :param prey: ofiara
        """
        self.__anger += prey.make_sound()
        x, y = move_towards_point(*self.get_position(), *prey.get_position(), self.get_speed())
        return x, y

    def attack(self, prey: Animal) -> None:
        """Zadaje obrażenia
        
        :param prey: ofiara
        """
        prey.set_damage(int(self.get_strenght() * self.get_anger() + self.get_weight()))

    def make_sound(self) -> int:
        """Wydanie dźwięku"""
        return int(self.get_anger() + self.get_weight() + self.get_strenght())
    
    def eat(self, prey: Animal) -> None:
        """Zjedzenie ofiary
        
        :param prey: ofiara
        """
        satiety = self.get_satiety()
        satiety += int(prey.get_weight())
        self.set_satiety(max(satiety, 100))
        self.__anger -= int(prey.get_weight()) % 100

    def can_have_child(self) -> bool:
        """Sprawdza, czy zwierzę może mieć potomka"""
        if self.get_age() < 5:
            return False
        if self.get_satiety() < 30:
            return False
        if self.get_thirst() < 30:
            return False
        return True


class Wolf(Predator):
    """Klasa reprezentująca wilka"""

    __claws_durability = 100  # wytrzymałość pazurów

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, anger: int, hit_points: int = 100, **kwargs) -> None:
        """Konstruktor klasy Wolf

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param speed: prędkość
        :param age: wiek
        :param thirst: poziom pragnienia
        :param satiety: poziom sytości
        :param gender: płeć
        :param view_range: zasięg widzenia
        :param strenght: siła
        :param anger: złość
        :param hit_points: punkty życia
        """
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, anger, hit_points)
        
    def roar(self) -> int:
        """Wydanie ryku"""
        return 20

    def get_claws_durability(self) -> int:
        """Zwraca wytrzymałość pazurów"""
        return self.__claws_durability
    
    def get_durability(self) -> int:
        """Zwraca wytrzymałość pazurów"""
        return self.get_claws_durability()
    
    def set_durability(self, damage_points: int) -> int:
        """Zwraca ilość punktów obrażeń, które nie zostały zablokowane przez pazury
        
        :param damage_points: punkty obrażeń
        """
        points = damage_points - self.__claws_durability
        self.__claws_durability -= damage_points
        self.__claws_durability = max(self.__claws_durability, 0)
        return max(points, 0)
    
    def make_sound(self) -> int:
        """Wydanie dźwięku"""
        return super().make_sound() + self.roar()

   
class Eagle(Predator):
    """Klasa reprezentująca orła"""

    __beak_durability = 100  # wytrzymałość dzioba

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, anger: int, hit_points: int = 100, **kwargs) -> None:
        """Konstruktor klasy Eagle

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param speed: prędkość
        :param age: wiek
        :param thirst: poziom pragnienia
        :param satiety: poziom sytości
        :param gender: płeć
        :param view_range: zasięg widzenia
        :param strenght: siła
        :param anger: złość
        :param hit_points: punkty życia
        """
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         hit_points, strenght, anger)
        
    def screech(self) -> int:
        """Wydanie pisku"""
        return 10

    def get_beak_durability(self) -> int:
        """Zwraca wytrzymałość dzioba"""
        return self.__beak_durability
    
    def get_durability(self) -> int:
        """Zwraca wytrzymałość dzioba"""
        return self.get_beak_durability()
    
    def set_durability(self, damage_points: int) -> int:
        """Zwraca ilość punktów obrażeń, które nie zostały zablokowane przez dziób
        
        :param damage_points: punkty obrażeń
        """
        points = damage_points - self.__beak_durability
        self.__beak_durability -= damage_points
        self.__beak_durability = max(self.__beak_durability, 0)
        return max(points, 0)
    
    def make_sound(self) -> int:
        """Wydanie dźwięku"""
        return super().make_sound() + self.screech()

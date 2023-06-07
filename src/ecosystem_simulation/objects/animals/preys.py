import sys

sys.path.append('../..')

from . import Animal
from ecosystem_simulation.utils import move_away_from_point


class Prey(Animal):
    """Klasa bazowa dla wszystkich zwierząt roślinożernych"""

    __is_dead = False  # czy zwierzę zostało zjedzone


    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, fear: int, hit_points: int = 100) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, hit_points)
        """Konstruktor klasy Prey
        
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
        :param fear: poziom strachu
        :param hit_points: punkty życia
        """
        self.__fear = fear

    def get_fear(self) -> int:
        """Zwraca poziom strachu"""
        return self.__fear
    
    def run(self, predator: Animal) -> None:
        """Ucieka przed drapieżnikiem
        
        :param predator: drapieżnik
        """
        self.__fear += predator.make_sound()
        x, y = move_away_from_point(*self.get_position(), *predator.get_position(), self.get_speed())
        return x, y

    def defend(self, predator: Animal) -> None:
        """Obrona przed drapieżnikiem.
        Zadaje obrażenia drapieżnikowi
        
        :param predator: drapieżnik
        """
        predator.set_damage(int(self.get_strenght() + self.get_weight() + self.get_fear()))

    def make_sound(self) -> int:
        """Wydanie dźwięku"""
        return self.get_fear() + self.get_weight() + self.get_strenght()
    
    def is_dead(self) -> bool:
        """Sprawdza, czy zwierzę zostało zjedzone"""
        return self.__is_dead
    
    def die(self) -> None:
        """Zabija zwierzę"""
        self.__is_eaten = True

    
class Mouse(Prey):
    """Klasa reprezentująca mysz"""

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, fear: int, hit_points: int = 100, **kwargs) -> None:
        """Konstruktor klasy Mouse
        
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
                         strenght, fear, hit_points)
        
    def squeak(self) -> int:
        """Wydanie pisku"""
        return 1

    def get_durability(self) -> int:
        """Zwraca wytrzymałość. Mysz nie ma wytrzymałości"""
        return 0
    
    def set_durability(self, damage_points: int) -> int:
        """Zwraca ilość punktów obrażeń, które nie zostały zablokowane przez wytrzymałość - wszystkie, bo mysz nie ma wytrzymałości"""
        return damage_points
    
    def make_sound(self) -> int:
        """Wydanie dźwięku"""
        return super().make_sound() + self.squeak()


class Deer(Prey):
    """Klasa reprezentująca jelenia"""

    __antlers_durability = 100  # wytrzymałość poroża

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                 strenght: int, fear: int, hit_points: int = 100, **kwargs) -> None:
        super().__init__(x, y, weight, speed, age, thirst, satiety, gender, view_range,
                         strenght, fear, hit_points)
        
    def yell(self) -> int:
        """Wydać dźwięk"""
        return 10

    def get_antlers_durability(self) -> int:
        """Zwraca wytrzymałość poroża"""
        return self.__antlers_durability
    
    def get_durability(self) -> int:
        return self.get_antlers_durability()
    
    def set_durability(self, damage_points: int) -> int:
        """Zwraca ilość punktów obrażeń, które nie zostały zablokowane przez poroże
        """
        points = damage_points - self.__antlers_durability
        self.__antlers_durability -= damage_points
        self.__antlers_durability = max(self.__antlers_durability, 0)
        return max(points, 0)
    
    def make_sound(self) -> int:
        """Wydanie dźwięku"""
        return super().make_sound() + self.yell()

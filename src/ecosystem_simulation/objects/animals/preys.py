import sys

sys.path.append('..')

from . import Animal
from ecosystem_simulation.utils import move_away_from_point


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
    
    def run(self, predator: Animal) -> None:
        """Ucieka przed drapieżnikiem"""
        self.__fear += predator.make_sound()
        x, y = move_away_from_point(*self.get_position(), *predator.get_position(), self.get_speed())
        return x, y

    def defend(self, predator: Animal) -> None:
        """Obronić się przed drapieżnikiem"""
        predator.set_damage(int(self.get_strenght() + self.get_weight() + self.get_fear()))

    def make_sound(self) -> int:
        return self.get_fear() + self.get_weight() + self.get_strenght()

    
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

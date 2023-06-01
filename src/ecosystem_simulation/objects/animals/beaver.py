import sys

sys.path.append('..')

from . import Animal
from ecosystem_simulation.objects.items import Tree


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
import sys

sys.path.append('..')

from ecosystem_simulation.objects import Object


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

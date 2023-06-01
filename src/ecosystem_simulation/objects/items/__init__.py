import sys

sys.path.append('..')

from ecosystem_simulation.objects import Object


class Item(Object):
    """Klasa reprezentująca przedmioty (obiekty nieożywione)"""

    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        """Konstruktor klasy Item

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param energy: energia
        :param durability: trwałość
        """
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
    """Klasa reprezentująca rośliny"""

    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        """Konstruktor klasy Plant

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param energy: energia
        :param durability: trwałość
        """
        super().__init__(x, y, weight, energy, durability)


class Water(Item):
    """Klasa reprezentująca wodę"""

    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        """Konstruktor klasy Water

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param energy: energia
        :param durability: trwałość
        """
        super().__init__(x, y, weight, energy, durability)


class Tree(Item):
    """Klasa reprezentująca drzewa"""

    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        """Konstruktor klasy Tree

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param energy: energia
        :param durability: trwałość
        """
        super().__init__(x, y, weight, energy, durability)


class Rock(Item):
    """Klasa reprezentująca kamienie"""

    def __init__(self, x: int, y: int, weight: float, energy: int,
                 durability: int) -> None:
        """Konstruktor klasy Rock

        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga
        :param energy: energia
        :param durability: trwałość
        """
        super().__init__(x, y, weight, energy, durability)

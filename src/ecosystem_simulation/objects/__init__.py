import sys

sys.path.append("..")

from ecosystem_simulation.utils import name_to_emoji


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
        return name_to_emoji(str(type(self).__name__))
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def get_hit_points(self):
        pass

    def __hash__(self) -> int:
        return self.__hashcode

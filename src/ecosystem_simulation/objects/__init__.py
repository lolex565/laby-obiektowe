import sys

sys.path.append("..")

from ecosystem_simulation.utils import name_to_emoji


class Object:
    """Klasa bazowa dla wszystkich obiektów w symulacji"""

    __hashcode = None  # hashcode obiektu

    def __init__(self, x: int, y: int, weight: float) -> None:
        """Inicjalizuje obiekt
        
        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga obiektu
        """
        self.__x = x
        self.__y = y
        self.__weight = weight
        self.__hashcode = id(self)

    def get_position(self) -> tuple:
        """Zwraca współrzędne obiektu"""
        return self.__x, self.__y
    
    def set_position(self, x: int, y: int) -> None:
        """Ustawia współrzędne obiektu
        
        :param x: współrzędna x
        :param y: współrzędna y
        """
        self.__x = x
        self.__y = y
    
    def get_weight(self) -> float:
        """Zwraca wagę obiektu
        
        :return: waga obiektu
        """
        return self.__weight
    
    def __str__(self) -> str:
        """Zwraca reprezentację obiektu w postaci emoji"""
        return name_to_emoji(str(type(self).__name__))
    
    def __repr__(self) -> str:
        """Zwraca reprezentację obiektu w postaci emoji"""
        return self.__str__()

    def __hash__(self) -> int:
        """Zwraca hashcode obiektu"""
        return self.__hashcode

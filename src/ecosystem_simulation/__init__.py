class Object:
    def __init__(self, x, y, weight) -> None:
        self.__x = x
        self.__y = y
        self.__weight = weight

    def get_coordinates(self) -> tuple:
        """Zwraca współrzędne obiektu"""
        return self.__x, self.__y
    
    def get_weight(self) -> tuple:
        """Zwraca wagę obiektu"""
        return self.__weight

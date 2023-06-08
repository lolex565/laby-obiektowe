import sys
from random import randint

sys.path.append('../..')

from ecosystem_simulation.objects import Object
from ecosystem_simulation.objects.items import Plant, Water


GENDER_MALE = True      # płeć męska
GENDER_FEMALE = False   # płeć żeńska


class Animal(Object):
    """Klasa bazowa dla wszystkich zwierząt w symulacji"""

    __reproduced = 0  # ile razy zwierzę się rozmnożyło

    def __init__(self, x: int, y: int, weight: float, speed: int,
                 age: int, thirst: int, satiety: int, gender: bool, view_range: int,
                strenght: int, hit_points: int = 100) -> None:
        """Inicjalizuje zwierzę
        
        :param x: współrzędna x
        :param y: współrzędna y
        :param weight: waga zwierzęcia
        :param speed: prędkość zwierzęcia
        :param age: wiek zwierzęcia
        :param thirst: poziom pragnienia zwierzęcia
        :param satiety: poziom sytości zwierzęcia
        :param gender: płeć zwierzęcia
        :param view_range: zasięg widzenia zwierzęcia
        :param strenght: siła zwierzęcia
        :param hit_points: punkty życia zwierzęcia
        """
        super().__init__(x, y, weight)
        self.__speed = speed
        self.__age = age
        self.__thirst = thirst
        self.__satiety = satiety
        self.__gender = gender
        self.__view_range = view_range
        self.__hit_points = hit_points
        self.__strenght = strenght

    def get_speed(self) -> float:
        """Zwraca prędkość zwierzęcia"""
        return self.__speed
    
    def get_age(self) -> int:
        """Zwraca wiek zwierzęcia"""
        return self.__age

    def can_have_child(self) -> bool:
        """Sprawdza, czy zwierzę może mieć potomka"""
        if self.get_age() < 5:
            return False
        if self.get_satiety() < 40:
            return False
        if self.get_thirst() < 40:
            return False
        if self.has_reproduced() > 3:
            return False
        return True
    
    def can_have_twins(self) -> bool:
        """Sprawdza, czy zwierzę może mieć bliźniaki"""
        if self.can_have_child():
            if self.get_satiety() > 80 and self.get_thirst() > 80:
                return True
        return False
    
    def can_have_triplets(self) -> bool:
        if self.can_have_twins() and randint(0, 300) == 1:
            return True
        return False
    
    def has_reproduced(self) -> int:
        """Sprawdza, czy zwierzę się już rozmnożyło"""
        return self.__reproduced

    def reproduce(self) -> None:
        """Zaznacza, że zwierze się rozmnożyło"""
        self.__reproduced += 1
    
    def set_age(self, age: int) -> None:
        """Ustawia wiek zwierzęcia
        
        :param age: wiek zwierzęcia
        """
        self.__age = age
    
    def get_satiety(self) -> int:
        """Zwraca poziom sytości zwierzęcia"""
        return self.__satiety
    
    def set_satiety(self, satiety: int) -> None:
        """Ustawia poziom sytości zwierzęcia
        
        :param satiety: poziom sytości zwierzęcia
        """
        self.__satiety = satiety

    def get_thirst(self) -> int:
        """Zwraca poziom pragnienia zwierzęcia"""
        return self.__thirst
    
    def get_gender(self) -> int:
        """Zwraca płeć zwierzęcia"""
        return self.__gender
    
    def get_view_range(self) -> int:
        """Zwraca zasięg widzenia zwierzęcia"""
        return self.__view_range
    
    def get_hit_points(self) -> int:    
        """Zwraca punkty życia zwierzęcia"""
        return self.__hit_points
    
    def get_strenght(self) -> int:
        """Zwraca siłę zwierzęcia"""
        return self.__strenght
    
    def move(self, x: int, y: int) -> None:
        """Przesuwa zwierzę na podane współrzędne
        
        :param x: współrzędna x
        :param y: współrzędna y
        """

        energy_lost = int((abs(self.get_position()[0] - x) + abs(self.get_position()[1] - y))) % 2
        if self.__satiety == 0 or self.__thirst == 0:
            self.__hit_points -= energy_lost
            self.__hit_points = int(max(self.__hit_points, 0))
        else:
            self.__satiety -= energy_lost
            self.__thirst -= energy_lost
            self.__satiety = max(self.__satiety, 0)
            self.__thirst = max(self.__thirst, 0)
        self.set_position(x, y)

    def eat(self, food: Plant) -> None:
        """Zjadanie rośliny przez zwierzę.
        Zwiększa poziom sytości zwierzęcia o wagę rośliny
        
        :param food: roślina
        """
        self.set_satiety((food.get_weight() * food.get_energy()) % 100)

    def drink(self, water: Water) -> None:
        """Picie wody przez zwierzę.
        Zwiększa poziom nawodnienia zwierzęcia o wagę wody
        
        :param water: woda
        """
        self.__thirst += water.get_weight() % 100

    def can_reproduce_with(self, partner) -> bool:
        """Zwraca True, jeśli zwierzęta mogą się rozmnażać
        
        :param partner: partner do rozmnażania
        """
        if type(self).__name__ == type(partner).__name__:
            if self.get_gender() != partner.get_gender():
                if self.get_hit_points() > 0 and partner.get_hit_points() > 0:
                    if self.get_age() >= 5 and partner.get_age() >= 5:
                        # if type(self).__name__ == "Predator":
                        #     if self.get_gender() == GENDER_MALE and not partner.has_reproduced():
                        #         return True
                        #     elif not self.has_reproduced():
                        #         return True
                        # elif not self.has_reproduced():
                        #     return True
                        if type(self).__name__ == "Predator":
                            return True
                        elif self.get_gender() == GENDER_MALE and partner.has_reproduced() <= 3:
                            return True
                        elif not self.has_reproduced() <= 3:
                            return True

        return False

    def get_durability(self) -> int:
        """Zwraca trwałość atrybutu ataku lub obrony zwierzęcia"""
        return 0

    def set_durability(self, damage_points: int) -> int:
        """Zadaje zwierzęciu obrażenia
        
        :param damage_points: punkty obrażeń
        """
        return damage_points

    def set_damage(self, points: int) -> None:
        """Zadaje zwierzęciu obrażenia
        
        :param points: punkty obrażeń
        """
        points = int(self.set_durability(points))
        self.__hit_points -= points
        self.__hit_points = int(max(self.__hit_points, 0))

    def make_sound(self) -> int:
        """Zwraca głośność wydawanego przez zwierzę dźwięku"""
        return 0
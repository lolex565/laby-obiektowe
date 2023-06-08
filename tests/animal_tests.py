import sys, random

sys.path.append("src/")

import unittest

from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.objects.animals.predators import *
from ecosystem_simulation.objects.animals.beaver import Beaver
from ecosystem_simulation.objects.items import *

class AnimalTester(unittest.TestCase):
    """Testy związanych ze zwierzętami"""

    def test_can_reproduce_with(self):
        male = Animal(0, 0, 0, 0, 6, 0, 0, GENDER_MALE, 0, 0)
        female = Animal(0, 0, 0, 0, 6, 0, 0, GENDER_FEMALE, 0, 0)

        self.assertTrue(male.can_reproduce_with(female), "Osobniki różnych płci powinny móc się rozmnażać")

        self.assertFalse(male.can_reproduce_with(male), "Osobniki tych samych płci nie powinny móc się rozmnażać")

    def test_predator_attacks_prey(self):
        predator = Predator(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            anger=randint(1, 10),
        )
        prey = Prey(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
        )

        hp_before_attack = prey.get_hit_points()
        predator.attack(prey)
        hp_after_attack = prey.get_hit_points()

        self.assertTrue(hp_after_attack < hp_before_attack, "Ofiara powinna otrzymać obrażenia")

    def test_predator_eats_prey(self):
        predator = Predator(
        x=0,
        y=0,
        weight=uniform(0.1, 20),
        speed=randint(1, 5),
        age=0,
        thirst=100,
        satiety=0,
        hit_points=100,
        gender=choice((GENDER_MALE, GENDER_FEMALE)),
        view_range=randint(1, 20),
        strenght=randint(1, 50),
        anger=randint(1, 10),
        )
        prey = Prey(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=0,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
        )

        predator.eat(prey)

        self.assertTrue(predator.get_satiety() > 0, "Zjedzenie ofiary powinno zwiększyć sytość drapieżnika")

    def test_animal_drinks_water(self):
        animal = Animal(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=0,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
        )

        water = Water(0, 0, random.uniform(0, 10), random.uniform(0, 10), 10)

        animal.drink(water)

        self.assertTrue(animal.get_thirst() > 0, "Po wypiciu wody zwierzę powinno być mniej spragnione")


    def test_prey_defends_against_predator(self):
        predator = Predator(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            anger=randint(1, 10),
        )
        prey = Prey(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
        )

        hp_before_attack = predator.get_hit_points()
        prey.defend(predator)
        hp_after_attack = predator.get_hit_points()

        self.assertTrue(hp_after_attack < hp_before_attack, "Drapieżnik powinien otrzymać obrażenia")

    def test_beaver_eats_tree(self):
        beaver = Beaver(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=0,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
        )

        tree = Tree(0, 0, random.uniform(0, 10), random.uniform(0, 10), 10)

        beaver.eat(tree)

        self.assertTrue(beaver.get_satiety() > 0, "Zjedzenie drzewa powinno zwiększyć sytość bobra")

    def test_prey_eats_plant(self):
        prey = Prey(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=0,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10)
        )

        plant = Plant(0, 0, random.uniform(0, 10), random.uniform(0, 10), 10)

        prey.eat(plant)

        self.assertTrue(prey.get_satiety() > 0, "Zjedzenie rośliny powinno zwiększyć sytość ofiary")

    def test_wolf_gives_damage_to_deer(self):
        wolf = Wolf(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            anger=randint(1, 10),
        )

        deer = Deer(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
        )

        wolf.attack(deer)

        self.assertTrue(deer.get_antlers_durability() < 100, "Poroże jelenia powinno zostać uszkodzone")

    def test_deer_gives_damage_to_eagle(self):
        eagle = Eagle(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            anger=randint(1, 10),
        )

        deer = Deer(
            x=0,
            y=0,
            weight=uniform(0.1, 20),
            speed=randint(1, 5),
            age=0,
            thirst=100,
            satiety=100,
            hit_points=100,
            gender=choice((GENDER_MALE, GENDER_FEMALE)),
            view_range=randint(1, 20),
            strenght=randint(1, 50),
            fear=randint(1, 10),
        )

        deer.defend(eagle)

        self.assertTrue(eagle.get_beak_durability() < 100, "Dziób orła powinien zostać uszkodzony")


if __name__ == '__main__':
    unittest.main()

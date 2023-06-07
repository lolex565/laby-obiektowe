import sys, random

sys.path.append("src/")

import unittest

from ecosystem_simulation.objects.animals import *
from ecosystem_simulation.objects.animals.preys import *
from ecosystem_simulation.objects.animals.predators import *
from ecosystem_simulation.objects.animals.beaver import Beaver

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


if __name__ == '__main__':
    unittest.main()

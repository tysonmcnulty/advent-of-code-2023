import unittest
from pathlib import Path

from src.day02 import load, Drawing, Game, Bag


class Day02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day02/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day02/input.txt")

    def test_load_example(self):
        self.assertEqual(
            self.example[0:2],
            [
                Game(
                    1,
                    [
                        Drawing(blue=3, red=4),
                        Drawing(red=1, green=2, blue=6),
                        Drawing(green=2),
                    ],
                ),
                Game(
                    2,
                    [
                        Drawing(blue=1, green=2),
                        Drawing(green=3, blue=4, red=1),
                        Drawing(green=1, blue=1),
                    ],
                ),
            ],
        )

    def test_game_is_possible_for_bag(self):
        bag = Bag(red=12, green=13, blue=14)
        self.assertEqual(
            [True, True, False, False, True],
            [game.is_possible(bag) for game in self.example],
        )
        self.assertEqual(
            8, sum(game.id for game in self.example if game.is_possible(bag))
        )

    def test_solution_1(self):
        bag = Bag(red=12, green=13, blue=14)
        self.assertEqual(
            2512, sum(game.id for game in self.input if game.is_possible(bag))
        )

    def test_smallest_possible_bag(self):
        self.assertEqual(
            [
                Bag(blue=6, green=2, red=4),
                Bag(blue=4, green=3, red=1),
                Bag(blue=6, green=13, red=20),
                Bag(blue=15, green=3, red=14),
                Bag(blue=2, green=3, red=6),
            ],
            [game.smallest_possible_bag for game in self.example],
        )

    def test_power(self):
        self.assertEqual(
            2286, sum(game.smallest_possible_bag.power for game in self.example)
        )

    def test_solution_2(self):
        self.assertEqual(
            67335, sum(game.smallest_possible_bag.power for game in self.input)
        )

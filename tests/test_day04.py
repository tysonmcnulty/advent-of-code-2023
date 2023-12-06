import unittest
from pathlib import Path

from src.day04 import load, ScratchCard


class Day04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day04/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day04/input.txt")

    def test_load_example(self):
        self.assertEqual(
            ScratchCard(
                id=1,
                winning_numbers=[41, 48, 83, 86, 17],
                picks=[83, 86, 6, 31, 17, 9, 48, 53],
            ),
            self.example[0],
        )
        self.assertEqual(6, len(self.example))

    def test_point_value(self):
        self.assertEqual(
            [8, 2, 2, 1, 0, 0], [card.point_value for card in self.example]
        )

    def test_solution_1(self):
        self.assertEqual(25010, sum(card.point_value for card in self.input))

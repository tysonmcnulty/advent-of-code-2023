import unittest
from collections import Counter
from pathlib import Path

from src.day04 import load, process, ScratchCard


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

    def test_cards_won(self):
        self.assertEqual([2, 3, 4, 5], self.example[0].cards_won)

    def test_process(self):
        card_counts = process(self.example)
        self.assertEqual(Counter({1: 1, 2: 2, 3: 4, 4: 8, 5: 14, 6: 1}), card_counts)
        self.assertEqual(30, sum(card_counts.values()))

    def test_solution_2(self):
        card_counts = process(self.input)
        self.assertEqual(9924412, sum(card_counts.values()))

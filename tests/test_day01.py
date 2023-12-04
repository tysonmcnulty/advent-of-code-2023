import unittest
from pathlib import Path

from src.day01 import load, Strategy, parse_digits


class Day01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day01/example.txt")
        cls.example_2 = load(
            Path(__file__).parent / "resources/day01/example2.txt",
            Strategy.DIGITS_OR_WORDS,
        )
        cls.input = load(Path(__file__).parent / "../src/day01/input.txt")
        cls.input_2 = load(
            Path(__file__).parent / "../src/day01/input.txt", Strategy.DIGITS_OR_WORDS
        )

    def test_load_example(self):
        self.assertEqual(self.example, [12, 38, 15, 77])
        self.assertEqual(sum(self.example), 142)

    def test_load_example2(self):
        self.assertEqual(self.example_2, [29, 83, 13, 24, 42, 14, 76])
        self.assertEqual(sum(self.example_2), 281)

    def test_parse_line(self):
        self.assertEqual(
            parse_digits("12threeight\n", Strategy.DIGITS_OR_WORDS), [1, 2, 3, 8]
        )

    def test_solution_1(self):
        self.assertEqual(sum(self.input), 55090)

    def test_solution_2(self):
        self.assertEqual(sum(self.input_2), 54871)

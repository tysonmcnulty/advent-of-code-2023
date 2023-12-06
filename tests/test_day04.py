import unittest
from pathlib import Path

from src.day04 import load


class Day04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day04/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day04/input.txt")

    def test_load_example(self):
        self.assertEqual([], self.example)

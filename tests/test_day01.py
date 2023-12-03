import unittest
from pathlib import Path

from src.day01 import load


class Day01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day01/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day01/input.txt")

    def test_load_example(self):
        self.assertEqual(self.example, [12, 38, 15, 77])

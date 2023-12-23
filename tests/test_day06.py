import unittest
from collections import Counter
from itertools import chain
from pathlib import Path

from src.day06 import load


class Day06Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day06/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day06/input.txt")

    def test_load_example(self):
        pass
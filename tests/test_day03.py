import unittest
from pathlib import Path

from src.day03 import load


class Day03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day03/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day03/input.txt")

    def test_load_example(self):
        self.assertEqual(
            self.example,
            [],
        )

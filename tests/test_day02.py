import unittest
from pathlib import Path

from src.day02 import load, Drawing, Game


class Day02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day02/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day02/input.txt")

    def test_load_example(self):
        self.assertEqual(
            self.example[0],
            Game(
                1,
                [
                    Drawing(blue=3, red=4),
                    Drawing(red=1, green=2, blue=6),
                    Drawing(green=2),
                ],
            ),
        )

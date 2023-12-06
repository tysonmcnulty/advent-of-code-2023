import unittest
from pathlib import Path

from src.day03 import load, Symbol, Coordinate, Number, Extent


class Day03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day03/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day03/input.txt")

    def test_load_example(self):
        self.assertEqual(
            self.example.symbols,
            set(
                [
                    Symbol(value="*", location=Coordinate(x=3, y=1)),
                    Symbol(value="#", location=Coordinate(x=6, y=3)),
                    Symbol(value="*", location=Coordinate(x=3, y=4)),
                    Symbol(value="+", location=Coordinate(x=5, y=5)),
                    Symbol(value="$", location=Coordinate(x=3, y=8)),
                    Symbol(value="*", location=Coordinate(x=5, y=8)),
                ]
            ),
        )
        self.assertEqual(
            self.example.numbers,
            set(
                [
                    Number(value="467", location=Coordinate(x=0, y=0)),
                    Number(value="114", location=Coordinate(x=5, y=0)),
                    Number(value="35", location=Coordinate(x=2, y=2)),
                    Number(value="633", location=Coordinate(x=6, y=2)),
                    Number(value="617", location=Coordinate(x=0, y=4)),
                    Number(value="58", location=Coordinate(x=7, y=5)),
                    Number(value="592", location=Coordinate(x=2, y=6)),
                    Number(value="755", location=Coordinate(x=6, y=7)),
                    Number(value="664", location=Coordinate(x=1, y=9)),
                    Number(value="598", location=Coordinate(x=5, y=9)),
                ]
            ),
        )

    def test_extent(self):
        number = Number(value="467", location=Coordinate(x=0, y=0))
        self.assertTrue(Coordinate(x=0, y=0) in number.extent)
        self.assertTrue(Coordinate(x=1, y=0) in number.extent)
        self.assertTrue(Coordinate(x=2, y=0) in number.extent)
        self.assertEqual(3, len(number.extent))

    def test_extent_iter(self):
        extent = Extent(
            top_left=Coordinate(x=0, y=0), bottom_right=Coordinate(x=2, y=1)
        )
        self.assertEqual(
            {
                Coordinate(x=0, y=0),
                Coordinate(x=1, y=0),
                Coordinate(x=2, y=0),
                Coordinate(x=0, y=1),
                Coordinate(x=1, y=1),
                Coordinate(x=2, y=1),
            },
            {c for c in extent},
        )

    def test_neighborhood(self):
        neighborhood = self.example.extent.neighborhood
        self.assertEqual(44, len(neighborhood))
        self.assertTrue(Coordinate(x=-1, y=-1) in neighborhood)
        self.assertEqual(Coordinate(x=-1, y=-1), neighborhood.outer.top_left)
        self.assertTrue(Coordinate(x=10, y=10) in neighborhood)
        self.assertEqual(Coordinate(x=10, y=10), neighborhood.outer.bottom_right)

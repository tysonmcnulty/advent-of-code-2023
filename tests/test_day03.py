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
            {
                Symbol(value="*", location=Coordinate(x=3, y=1)),
                Symbol(value="#", location=Coordinate(x=6, y=3)),
                Symbol(value="*", location=Coordinate(x=3, y=4)),
                Symbol(value="+", location=Coordinate(x=5, y=5)),
                Symbol(value="$", location=Coordinate(x=3, y=8)),
                Symbol(value="*", location=Coordinate(x=5, y=8)),
            },
        )
        self.assertEqual(
            self.example.numbers,
            {
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
            },
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

    def test_neighborhood_iter(self):
        neighborhood = Symbol("*", Coordinate(3, 3)).neighborhood
        self.assertEqual(
            {
                Coordinate(2, 2),
                Coordinate(3, 2),
                Coordinate(4, 2),
                Coordinate(2, 3),
                Coordinate(4, 3),
                Coordinate(2, 4),
                Coordinate(3, 4),
                Coordinate(4, 4),
            },
            {c for c in neighborhood},
        )

    def test_schematic_part_numbers(self):
        self.assertEqual(8, len(self.example.part_numbers))
        self.assertEqual(
            {
                Number(value="114", location=Coordinate(x=5, y=0)),
                Number(value="58", location=Coordinate(x=7, y=5)),
            },
            self.example.numbers - self.example.part_numbers,
        )
        self.assertEqual(
            4361, sum(map(int, (n.value for n in self.example.part_numbers)))
        )

    def test_solution_1(self):
        self.assertEqual(
            525911, sum(map(int, (n.value for n in self.input.part_numbers)))
        )

    def test_gears(self):
        self.assertEqual(
            {
                Symbol(value="*", location=Coordinate(x=3, y=1)),
                Symbol(value="*", location=Coordinate(x=5, y=8)),
            },
            self.example.gears,
        )

    def test_gear_ratios(self):
        self.assertEqual(
            {
                Symbol(value="*", location=Coordinate(x=3, y=1)): 16345,
                Symbol(value="*", location=Coordinate(x=5, y=8)): 451490,
            },
            self.example.gear_ratios_by_gear,
        )
        self.assertEqual(467835, sum(self.example.gear_ratios_by_gear.values()))

    def test_solution_2(self):
        print(self.input.gear_ratios_by_gear)
        self.assertEqual(75805607, sum(self.input.gear_ratios_by_gear.values()))

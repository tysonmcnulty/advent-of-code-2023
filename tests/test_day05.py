import unittest
from collections import Counter
from pathlib import Path

from src.day05 import load, Unit, Category, Almanac


class Day05Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day05/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day05/input.txt")

    def test_load_example(self):
        self.assertEqual(
            [
                Unit(Category.SEED, 79),
                Unit(Category.SEED, 14),
                Unit(Category.SEED, 55),
                Unit(Category.SEED, 13),
            ],
            self.example[0],
        )
        self.assertEqual(
            [
                Unit.Range(Category.SEED, 79, 14),
                Unit.Range(Category.SEED, 55, 13),
            ],
            self.example[1]
        )
        self.assertEqual(
            self.example[2].maps["seed"].lines,
            [Almanac.Map.Line(50, 98, 2), Almanac.Map.Line(52, 50, 48)],
        )

    def test_almanac_map(self):
        lines = [Almanac.Map.Line(50, 98, 2), Almanac.Map.Line(52, 50, 48)]

        almanac_map = Almanac.Map(
            source=Category.SEED,
            destination=Category.SOIL,
            lines=lines,
        )

        self.assertEqual(Unit(Category.SOIL, 81), almanac_map[Unit(Category.SEED, 79)])
        self.assertEqual(Unit(Category.SOIL, 14), almanac_map[Unit(Category.SEED, 14)])
        self.assertEqual(Unit(Category.SOIL, 57), almanac_map[Unit(Category.SEED, 55)])
        self.assertEqual(Unit(Category.SOIL, 13), almanac_map[Unit(Category.SEED, 13)])

    def test_resolve(self):
        (seeds, _, almanac) = self.example
        self.assertEqual(
            [
                Unit(Category.LOCATION, 82),
                Unit(Category.LOCATION, 43),
                Unit(Category.LOCATION, 86),
                Unit(Category.LOCATION, 35),
            ],
            [almanac.resolve(s) for s in seeds],
        )

    def test_solution_1(self):
        (seeds, _, almanac) = self.input
        self.assertEqual(
            Unit(Category.LOCATION, 196167384),
            min([almanac.resolve(s) for s in seeds], key=(lambda loc: loc.id)),
        )

import unittest
from collections import Counter
from itertools import chain
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
            self.example[1],
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

    def test_resolve_unit(self):
        (seeds, _, almanac) = self.example
        self.assertEqual(
            [
                Unit(Category.LOCATION, 82),
                Unit(Category.LOCATION, 43),
                Unit(Category.LOCATION, 86),
                Unit(Category.LOCATION, 35),
            ],
            [almanac.resolve_unit(s) for s in seeds],
        )

    def test_solution_1(self):
        (seeds, _, almanac) = self.input
        self.assertEqual(
            Unit(Category.LOCATION, 196167384),
            min([almanac.resolve_unit(s) for s in seeds], key=(lambda loc: loc.id)),
        )

    def test_split(self):
        first = Unit.Range(Category.SEED, 10, 10)
        second = Unit.Range(Category.SEED, 15, 20)
        [overlap, *remainder] = first.split(second)

        self.assertEqual(Unit.Range(Category.SEED, 15, 5), overlap)
        self.assertEqual([Unit.Range(Category.SEED, 10, 5)], remainder)

    def test_split_2(self):
        first = Unit.Range(Category.SEED, 15, 10)
        second = Unit.Range(Category.SEED, 10, 10)
        [overlap, *remainder] = first.split(second)
        self.assertEqual(Unit.Range(Category.SEED, 15, 5), overlap)
        self.assertEqual([Unit.Range(Category.SEED, 20, 5)], remainder)

    def test_split_3(self):
        first = Unit.Range(Category.SEED, 15, 15)
        second = Unit.Range(Category.SEED, 20, 5)
        [overlap, *remainder] = first.split(second)
        self.assertEqual(Unit.Range(Category.SEED, 20, 5), overlap)
        self.assertEqual(
            [Unit.Range(Category.SEED, 15, 5), Unit.Range(Category.SEED, 25, 5)],
            remainder,
        )

    def test_split_4(self):
        first = Unit.Range(Category.SEED, 15, 15)
        second = Unit.Range(Category.SEED, 20, 10)
        [overlap, *remainder] = first.split(second)
        self.assertEqual(Unit.Range(Category.SEED, 20, 10), overlap)
        self.assertEqual([Unit.Range(Category.SEED, 15, 5)], remainder)

    def test_split_5(self):
        first = Unit.Range(Category.SEED, 15, 5)
        second = Unit.Range(Category.SEED, 10, 15)
        [overlap, *remainder] = first.split(second)
        self.assertEqual(Unit.Range(Category.SEED, 15, 5), overlap)
        self.assertEqual([], remainder)

    def test_split_6(self):
        first = Unit.Range(Category.SEED, 15, 5)
        second = Unit.Range(Category.SEED, 15, 10)
        [overlap, *remainder] = first.split(second)
        self.assertEqual(Unit.Range(Category.SEED, 15, 5), overlap)
        self.assertEqual([], remainder)

    def test_split_7(self):
        first = Unit.Range(Category.SEED, 45, 10)
        second = Unit.Range(Category.SEED, 50, 48)
        [overlap, *remainder] = first.split(second)
        self.assertEqual(Unit.Range(Category.SEED, 50, 5), overlap)
        self.assertEqual([Unit.Range(Category.SEED, 45, 5)], remainder)

    def test_map_seed_range(self):
        seed_range = Unit.Range(Category.SEED, 0, 100)
        seed_to_soil_map = self.example[2].maps["seed"]

        self.assertEqual(
            {
                Unit.Range(Category.SOIL, 0, 50),
                Unit.Range(Category.SOIL, 50, 2),
                Unit.Range(Category.SOIL, 52, 48),
            },
            seed_to_soil_map[seed_range],
        )

    def test_resolve_range(self):
        (_, seed_ranges, almanac) = self.example
        location_ranges = {
            *chain.from_iterable(almanac.resolve_range(r) for r in seed_ranges)
        }
        self.assertEqual(
            {
                Unit.Range(category=Category.LOCATION, start=60, length=1),
                Unit.Range(category=Category.LOCATION, start=82, length=3),
                Unit.Range(category=Category.LOCATION, start=46, length=10),
            }
            | {
                Unit.Range(category=Category.LOCATION, start=94, length=3),
                Unit.Range(category=Category.LOCATION, start=97, length=2),
                Unit.Range(category=Category.LOCATION, start=86, length=4),
                Unit.Range(category=Category.LOCATION, start=56, length=4),
            },
            location_ranges,
        )

    def test_solution_2(self):
        (_, seed_ranges, almanac) = self.input
        location_ranges = {
            *chain.from_iterable(almanac.resolve_range(r) for r in seed_ranges)
        }
        self.assertEqual(
            Unit.Range(Category.LOCATION, 125742456, 20229261),
            min(location_ranges, key=(lambda loc_range: loc_range.start)),
        )

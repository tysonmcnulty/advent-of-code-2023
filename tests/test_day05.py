import unittest
from collections import Counter
from pathlib import Path

from src.day05 import load, Seed, Soil, Almanac, Location


class Day05Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = load(Path(__file__).parent / "resources/day05/example.txt")
        cls.input = load(Path(__file__).parent / "../src/day05/input.txt")

    def test_load_example(self):
        self.assertEqual([Seed(79), Seed(14), Seed(55), Seed(13)], self.example[0])
        self.assertEqual(
            self.example[1].maps["seed"].lines,
            [Almanac.Map.Line(50, 98, 2), Almanac.Map.Line(52, 50, 48)],
        )

    def test_almanac_map(self):
        lines = [Almanac.Map.Line(50, 98, 2), Almanac.Map.Line(52, 50, 48)]

        almanac_map = Almanac.Map(
            source_category="seed",
            destination_category="soil",
            lines=lines,
        )

        self.assertEqual(Soil(1), almanac_map[Seed(1)])
        self.assertEqual(Soil(81), almanac_map[Seed(79)])
        self.assertEqual(Soil(14), almanac_map[Seed(14)])
        self.assertEqual(Soil(57), almanac_map[Seed(55)])
        self.assertEqual(Soil(13), almanac_map[Seed(13)])

    def test_resolve_location(self):
        (seeds, almanac) = self.example
        self.assertEqual(
            [Location(82), Location(43), Location(86), Location(35)],
            [almanac.resolve_location(s) for s in seeds],
        )

    def test_solution_1(self):
        (seeds, almanac) = self.input
        self.assertEqual(
            Location(196167384),
            min([almanac.resolve_location(s) for s in seeds], key=(lambda loc: loc.id)),
        )

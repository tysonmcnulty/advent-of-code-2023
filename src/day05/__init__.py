import re
from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path
from typing import ClassVar, Self


class Category(StrEnum):
    SEED = auto()
    SOIL = auto()
    FERTILIZER = auto()
    WATER = auto()
    LIGHT = auto()
    TEMPERATURE = auto()
    HUMIDITY = auto()
    LOCATION = auto()


@dataclass(frozen=True)
class Unit:
    category: Category
    id: int

    @dataclass(frozen=True)
    class Range:
        category: Category
        start: int
        length: int

@dataclass
class Almanac:
    maps: dict[Category, "Almanac.Map"]

    def resolve(self, unit: Unit) -> Unit:
        _next = unit
        while _next.category in self.maps:
            _next = self.maps[_next.category][_next]

        return _next

    @dataclass
    class Map:
        source: Category
        destination: Category
        lines: list["Almanac.Map.Line"]

        @dataclass
        class Line:
            destination_range_start: int
            source_range_start: int
            range_length: int

            @property
            def source_range(self) -> range:
                return range(
                    self.source_range_start,
                    self.source_range_start + self.range_length,
                )

            @staticmethod
            def parse(data: str) -> Self:
                return Almanac.Map.Line(
                    *(int(number) for number in re.findall(r"\d+", data))
                )

        def __getitem__(self, item):
            if not (item.category == self.source):
                raise KeyError(
                    f"category '{item.category}' of item does not match category '{self.source}' of map source"
                )

            if isinstance(item, Unit):
                unit = item
                for line in self.lines:
                    if unit.id in line.source_range:
                        return Unit(
                            category=self.destination,
                            id=(
                                unit.id
                                - line.source_range_start
                                + line.destination_range_start
                            ),
                        )

                return Unit(category=self.destination, id=unit.id)

            if isinstance(item, Unit.Range):
                return item


def load(data_file: Path):
    with open(data_file) as data:
        seed_data, *almanac_maps_data = re.split(r"\n\n+", data.read())
        seed_numbers = [int(match) for match in re.findall(r"\d+", seed_data)]
        seeds = [Unit(Category.SEED, id=n) for n in seed_numbers]
        seed_ranges = [Unit.Range(Category.SEED, seed_numbers[n], seed_numbers[n + 1]) for n in range(0, len(seed_numbers), 2)]

        almanac_maps = []
        for almanac_map_data in almanac_maps_data:
            header, *lines_data = almanac_map_data.split("\n")
            source, destination = map(
                Category, re.match(r"(\w+)-to-(\w+) map:", header).groups()
            )
            lines = [Almanac.Map.Line.parse(line_data) for line_data in lines_data]
            almanac_maps.append(Almanac.Map(source, destination, lines))

        almanac = Almanac(maps=dict((m.source, m) for m in almanac_maps))

    return (seeds, seed_ranges, almanac)

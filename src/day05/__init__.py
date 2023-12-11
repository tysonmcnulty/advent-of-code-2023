import re
from dataclasses import dataclass, field
from enum import StrEnum, auto
from itertools import chain
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

        @property
        def end(self):
            return self.start + self.length

        @property
        def last(self):
            return self.end - 1

        def __contains__(self, item: int):
            return item in range(self.start, self.end)

        def split(self, other):
            if not isinstance(other, Unit.Range):
                raise TypeError()

            if not self.category == other.category:
                return [self]

            if self.start in other:
                if self.last in other:
                    return [self]
                if self.last not in other:
                    return [
                        Unit.Range(self.category, self.start, other.end - self.start),
                        Unit.Range(self.category, other.end, self.end - other.end),
                    ]

            if other.start in self:
                if other.last in self:
                    overlap = other
                    remainder = [
                        Unit.Range(self.category, self.start, other.start - self.start)
                    ]
                    if self.last > other.last:
                        remainder.append(
                            Unit.Range(self.category, other.end, self.end - other.end)
                        )
                    return [overlap, *remainder]
                if other.last not in self:
                    return [
                        Unit.Range(self.category, other.start, self.end - other.start),
                        Unit.Range(self.category, self.start, other.start - self.start),
                    ]

            return [None, self]


@dataclass
class Almanac:
    maps: dict[Category, "Almanac.Map"]

    def resolve_unit(self, unit: Unit) -> Unit:
        _next = unit
        while _next.category in self.maps:
            _next = self.maps[_next.category][_next]

        return _next

    def resolve_range(self, unit_range: Unit.Range) -> set[Unit.Range]:
        _next = {unit_range}
        while (category := next(iter(_next)).category) in self.maps:
            category_map = self.maps[category]
            _next = set(chain.from_iterable(category_map[r] for r in _next))

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
                source_unit = item
                for line in self.lines:
                    if source_unit.id in line.source_range:
                        return Unit(
                            category=self.destination,
                            id=(
                                source_unit.id
                                - line.source_range_start
                                + line.destination_range_start
                            ),
                        )

                return Unit(category=self.destination, id=source_unit.id)

            if isinstance(item, Unit.Range):
                destination_ranges = set()
                remainders = {item}
                for line in self.lines:
                    line_source_range = Unit.Range(
                        self.source, line.source_range_start, line.range_length
                    )
                    next_remainders = set()
                    overlapped_remainders = set()
                    for r in remainders:
                        [overlap, *line_remainders] = r.split(line_source_range)
                        if overlap is not None:
                            overlapped_remainders.add(r)
                            destination_ranges.add(
                                Unit.Range(
                                    category=self.destination,
                                    start=(
                                        overlap.start
                                        - line.source_range_start
                                        + line.destination_range_start
                                    ),
                                    length=overlap.length,
                                )
                            )

                        next_remainders |= set(line_remainders)

                    remainders |= next_remainders
                    remainders -= overlapped_remainders

                destination_ranges.update(
                    map(
                        lambda r: Unit.Range(self.destination, r.start, r.length),
                        remainders,
                    )
                )

                return destination_ranges


def load(data_file: Path):
    with open(data_file) as data:
        seed_data, *almanac_maps_data = re.split(r"\n\n+", data.read())
        seed_numbers = [int(match) for match in re.findall(r"\d+", seed_data)]
        seeds = [Unit(Category.SEED, id=n) for n in seed_numbers]
        seed_ranges = [
            Unit.Range(Category.SEED, seed_numbers[n], seed_numbers[n + 1])
            for n in range(0, len(seed_numbers), 2)
        ]

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

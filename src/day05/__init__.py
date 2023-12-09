import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Self


@dataclass(frozen=True)
class Seed:
    category: ClassVar[str] = "seed"
    id: int


@dataclass(frozen=True)
class Soil:
    category: ClassVar[str] = "soil"
    id: int


@dataclass(frozen=True)
class Fertilizer:
    category: ClassVar[str] = "fertilizer"
    id: int


@dataclass(frozen=True)
class Water:
    category: ClassVar[str] = "water"
    id: int


@dataclass(frozen=True)
class Light:
    category: ClassVar[str] = "light"
    id: int


@dataclass(frozen=True)
class Temperature:
    category: ClassVar[str] = "temperature"
    id: int


@dataclass(frozen=True)
class Humidity:
    category: ClassVar[str] = "humidity"
    id: int


@dataclass(frozen=True)
class Location:
    category: ClassVar[str] = "location"
    id: int


CATEGORY_MAP = {
    "seed": Seed,
    "soil": Soil,
    "fertilizer": Fertilizer,
    "water": Water,
    "light": Light,
    "temperature": Temperature,
    "humidity": Humidity,
    "location": Location,
}


@dataclass
class Almanac:
    maps: dict[str, "Almanac.Map"]

    def resolve_location(self, seed: Seed) -> Location:
        _next = seed
        while _next.category in self.maps:
            _next = self.maps[_next.category][_next]

        return _next

    @dataclass
    class Map:
        source_category: str
        destination_category: str
        lines: list["Almanac.Map.Line"]

        @dataclass
        class Line:
            destination_range_start: int
            source_range_start: int
            range_length: int

            @staticmethod
            def parse(data: str) -> Self:
                return Almanac.Map.Line(
                    *(int(number) for number in re.findall(r"\d+", data))
                )

        def __getitem__(self, item):
            if not (
                hasattr(item, "category") and item.category == self.source_category
            ):
                raise KeyError(
                    f"category '{item.category}' of source item does not match source category '{self.source_category}'"
                )

            DestinationCategory = CATEGORY_MAP[self.destination_category]

            for line in self.lines:
                if (
                    item.id >= line.source_range_start
                    and item.id < line.source_range_start + line.range_length
                ):
                    return DestinationCategory(
                        item.id - line.source_range_start + line.destination_range_start
                    )

            return DestinationCategory(item.id)


def load(data_file: Path):
    with open(data_file) as data:
        seed_data, *almanac_maps_data = re.split(r"\n\n+", data.read())

        seeds = [Seed(int(id)) for id in re.findall(r"\d+", seed_data)]

        almanac_maps = []
        for almanac_map_data in almanac_maps_data:
            header, *lines_data = almanac_map_data.split("\n")
            source_category, destination_category = re.match(
                r"(\w+)-to-(\w+) map:", header
            ).groups()
            lines = [Almanac.Map.Line.parse(line_data) for line_data in lines_data]
            almanac_maps.append(
                Almanac.Map(source_category, destination_category, lines)
            )

        almanac = Almanac(maps=dict((m.source_category, m) for m in almanac_maps))

    return (seeds, almanac)

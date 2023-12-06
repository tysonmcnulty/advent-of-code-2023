import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class Extent:
    top_left: Coordinate
    bottom_right: Coordinate

    @cached_property
    def neighborhood(self) -> "Neighborhood":
        return Neighborhood(inner=self)

    def __contains__(self, item: Coordinate) -> bool:
        return (
            self.top_left.x <= item.x
            and item.x <= self.bottom_right.x
            and self.top_left.y <= item.y
            and item.y <= self.bottom_right.y
        )

    def __iter__(self) -> Iterable[Coordinate]:
        return (
            Coordinate(x, y)
            for x in range(self.top_left.x, self.bottom_right.x + 1)
            for y in range(self.top_left.y, self.bottom_right.y + 1)
        )

    def __len__(self):
        return (self.bottom_right.x - self.top_left.x + 1) * (
            self.bottom_right.y - self.top_left.y + 1
        )


@dataclass(frozen=True)
class Neighborhood:
    inner: Extent

    @cached_property
    def outer(self) -> Extent:
        return Extent(
            top_left=Coordinate(
                x=(self.inner.top_left.x - 1), y=(self.inner.top_left.y - 1)
            ),
            bottom_right=Coordinate(
                x=(self.inner.bottom_right.x + 1), y=(self.inner.bottom_right.y + 1)
            ),
        )

    def __contains__(self, item: Coordinate) -> bool:
        return item in self.outer and not item in self.inner

    def __len__(self):
        return len(self.outer) - len(self.inner)


@dataclass(frozen=True)
class Symbol:
    value: str
    location: Coordinate


@dataclass(frozen=True)
class Number:
    value: str
    location: Coordinate

    @cached_property
    def extent(self):
        return Extent(
            self.location,
            Coordinate(self.location.x + len(self.value) - 1, self.location.y),
        )


@dataclass
class Schematic:
    extent: Extent
    symbols: set[Symbol] = field(default_factory=set)
    numbers: set[Number] = field(default_factory=set)


def load(data_file: Path):
    symbols = set()
    numbers = set()
    with open(data_file) as lines:
        for y, line in enumerate(lines):
            for symbol_match in re.finditer(r"(?![\d\\.]).", line.strip()):
                x = symbol_match.start()
                value = symbol_match.group()
                symbols.add(Symbol(value=value, location=Coordinate(x, y)))

            for number_match in re.finditer(r"\d+", line.strip()):
                x = number_match.start()
                value = number_match.group()
                numbers.add(Number(value=value, location=Coordinate(x, y)))

        extent = Extent(
            top_left=Coordinate(0, 0),
            bottom_right=Coordinate(x=(len(line) - 1), y=y),
        )

    return Schematic(extent=extent, symbols=symbols, numbers=numbers)

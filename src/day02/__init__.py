import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


def load(data_file: Path):
    games = []
    with open(data_file) as lines:
        for game_data in lines:
            games.append(Game.from_str(game_data))

    return games


@dataclass
class Bag:
    blue: int = 0
    green: int = 0
    red: int = 0

    @property
    def power(self) -> int:
        return self.blue * self.green * self.red


@dataclass
class Drawing:
    blue: int = 0
    green: int = 0
    red: int = 0

    @staticmethod
    def from_str(drawing_data: str) -> Self:
        drawing_kwargs = dict(
            (k, int(v)) for v, k in re.findall(r"(\d+) (blue|green|red)", drawing_data)
        )
        return Drawing(**drawing_kwargs)

    def is_possible(self, bag) -> bool:
        return self.blue <= bag.blue and self.green <= bag.green and self.red <= bag.red


@dataclass
class Game:
    id: int
    drawings: list[Drawing] = field(default_factory=list)

    @staticmethod
    def from_str(game_data: str) -> Self:
        (id_data, drawings_data) = game_data.split(":")
        id = int(re.search(r"Game (\d+)", id_data).group(1))
        drawings = [Drawing.from_str(d) for d in drawings_data.split(";")]
        return Game(id, drawings)

    @property
    def smallest_possible_bag(self) -> Bag:
        return Bag(
            red=max(d.red for d in self.drawings),
            blue=max(d.blue for d in self.drawings),
            green=max(d.green for d in self.drawings),
        )

    def is_possible(self, bag: Bag) -> bool:
        return all(d.is_possible(bag) for d in self.drawings)

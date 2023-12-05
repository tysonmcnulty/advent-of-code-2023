import re
from dataclasses import dataclass, field
from pathlib import Path


def load(data_file: Path):
    games = []
    with open(data_file) as lines:
        for game_data in lines:
            games.append(Game.from_str(game_data))

    return games


@dataclass
class Drawing:
    blue: int = 0
    green: int = 0
    red: int = 0

    @staticmethod
    def from_str(drawing_data: str):
        drawing_kwargs = dict(
            (k, int(v)) for v, k in re.findall(r"(\d+) (blue|green|red)", drawing_data)
        )
        return Drawing(**drawing_kwargs)


@dataclass
class Game:
    id: int
    drawings: list[Drawing] = field(default_factory=list)

    @staticmethod
    def from_str(game_data: str):
        (id_data, drawings_data) = game_data.split(":")
        id = int(re.search(r"Game (\d+)", id_data).group(1))
        drawings = [Drawing.from_str(d) for d in drawings_data.split(";")]
        return Game(id, drawings)

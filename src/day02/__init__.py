from pathlib import Path


def load(data_file: Path):
    games = []
    with open(data_file) as lines:
        for game_data in lines:
            games.append(Game.from_str(game_data))

    return games


class Drawing:
    def __init__(self, blue: int = 0, green: int = 0, red: int = 0):
        self.blue = blue
        self.green = green
        self.red = red

    def __eq__(self, other):
        if isinstance(other, Drawing):
            return (
                self.red == other.red
                and self.green == other.green
                and self.blue == other.blue
            )
        else:
            return NotImplemented

    @staticmethod
    def from_str(drawing_data: str):
        return Drawing(0, 0, 0)


class Game:
    def __init__(self, id: int, drawings: list[Drawing]):
        self.id = id
        self.drawings = drawings

    def __eq__(self, other):
        if isinstance(other, Game):
            return self.id == other.id and self.drawings == other.drawings
        else:
            return NotImplemented

    @staticmethod
    def from_str(game_data: str):
        return Game(0, [Drawing()])

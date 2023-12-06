import re
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path


@dataclass(frozen=True)
class ScratchCard:
    id: int
    winning_numbers: list[int] = field(default_factory=list)
    picks: list[int] = field(default_factory=list)

    @cached_property
    def point_value(self):
        winning_picks = set(self.winning_numbers) & set(self.picks)
        return 0 if len(winning_picks) == 0 else 2 ** (len(winning_picks) - 1)


def load(data_file: Path):
    scratch_cards = []
    with open(data_file) as lines:
        for line in lines:
            id_data, rest = line.split(":")
            winning_numbers_data, picks_data = rest.split("|")
            id = int(re.search(r"\d+", id_data).group())
            winning_numbers = list(map(int, re.findall(r"\d+", winning_numbers_data)))
            picks = list(map(int, re.findall(r"\d+", picks_data)))
            scratch_cards.append(ScratchCard(id, winning_numbers, picks))

    return scratch_cards

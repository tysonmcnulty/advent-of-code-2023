import re
from pathlib import Path
from enum import Enum


DIGIT_MAP = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


class Strategy(Enum):
    DIGITS_ONLY = r"(?=(\d))"
    DIGITS_OR_WORDS = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"


def load(data_file: Path, strategy: Strategy = Strategy.DIGITS_ONLY):
    calibration_values = []

    with open(data_file) as calibration_data:
        for line in calibration_data:
            digits = parse_digits(line, strategy)
            calibration_values.append(digits[0] * 10 + digits[-1])

    return calibration_values


def parse_digits(line: str, strategy: Strategy):
    return list(map(lambda s: DIGIT_MAP[s], re.findall(strategy.value, line)))

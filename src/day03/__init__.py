import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


def load(data_file: Path):
    with open(data_file) as lines:
        for line in lines:
            pass

    return []
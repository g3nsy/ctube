from enum import Enum
from typing import Set


class Color(Enum):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def get_color_by_name(color_name: str) -> Color:
    return Color.__members__[color_name.upper()]


def color(string: str, col: Color) -> str:
    return f"{col.value}{string}{Color.RESET.value}"


def get_color_names() -> Set[str]:
    upper_color_names = set(Color.__members__.keys())
    upper_color_names.remove("RESET")
    return {color_name.lower() for color_name in upper_color_names}

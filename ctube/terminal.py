import sys
import tty
import termios
from typing import List, Optional
from ctube.colors import Color, color


class Prompt:
    def __init__(self, char: str = "❯", col: Color = Color.GREEN):

        self.char = char
        self.col = col

    def get_input(self):
        return input(f"{color(self.char, self.col)} ")


class Buffer:
    def __init__(self, infinite_scroll: bool = True):
        self.infinite_scroll = infinite_scroll
        self._index = 0
        self._buffer: List[str] = []

    def get(self) -> Optional[str]:
        return self._buffer[self._index]

    def next(self) -> None:
        if self._index == len(self._buffer) - 1:
            if self.infinite_scroll:
                self._index = 0
        else:
            self._index += 1

    def prev(self) -> None:
        if self._index == 0:
            if self.infinite_scroll:
                self._index = len(self._buffer) - 1
        else:
            self._index -= 1

    def add(self, string: str) -> None:
        self._buffer.append(string)


def get_fchar_unix() -> str:
    charlist: List[str] = []

    for i in range(3):
        charlist.append(get_char_unix())

        # chr(27): '\x1b'
        # chr(91): '['

        if charlist[i] not in [chr(27), chr(91)]:
            break

        if len(charlist) > 1:
            if charlist == [chr(27), chr(27)]:
                break

    if len(charlist) == 3:
        if charlist[2] == "A":
            return "UP"
        if charlist[2] == "B":
            return "DOWN"
        if charlist[2] == "C":
            return "RIGHT"
        if charlist[2] == "D":
            return "LEFT"

    if len(charlist) == 2:
        if charlist == [chr(27), chr(27)]:
            return chr(27)

    if len(charlist) == 1:
        return charlist[0]

    return ""


def get_char_unix() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

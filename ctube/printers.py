import shutil
from typing import List
import ctube
from ctube.cmds import Command
from ctube.colors import color, Color
from ctube.containers import MusicItem


def print_header() -> None:
    write("░█▀▀░▀█▀░█░█░█▀▄░█▀▀░", Color.GREEN)
    write("░█░░░░█░░█░█░█▀▄░█▀▀░", Color.GREEN)
    write("░▀▀▀░░▀░░▀▀▀░▀▀░░▀▀▀░", Color.GREEN)
    print(f"\u2022 {color('version', Color.BOLD)}: {color(ctube.__version__, Color.BLUE)}")
    print("\u2022 source: https://github.com/g3nsy/ctube")
    print("\u2022 Type 'help' to list the available commands")


def print_help() -> None:
    write(":: Helper", Color.GREEN)
    for cmd in Command:
        print(f"\u2022 {color(cmd.value.name, Color.BOLD)}:")
        write(cmd.value.description, Color.GREEN)
        print()


def print_music_items(music_items: List[MusicItem]) -> None:
    terminal_columns = shutil.get_terminal_size().columns
    max_index_len = len(str(len(music_items)))
    space_for_title = terminal_columns - max_index_len - 3  # [, ], ' '
    for i, music_item in enumerate(music_items):
        if len(music_item.title) > space_for_title:
            title = f"{music_item.title[:space_for_title - 3]}..."
        else:
            title = music_item.title
        lb = color("[", Color.BLUE)
        rb = color("]", Color.BLUE)
        ci = color(str(i), Color.GREEN)
        print(f"{lb}{ci}{rb}{' ' * (1 + max_index_len - len(str(i)))}{title}")


def clear_screen() -> None:
    print("\033c", end="")


def write(string: str, col: Color = Color.WHITE):
    print(color(string, color=col))

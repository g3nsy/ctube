import shutil
from typing import List, Dict
import ctube
from ctube.cmds import Command
from ctube.colors import color, Color
from ctube.containers import Album


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


def print_albums_list(albums: List[Album]) -> None:
    max_index_len = len(str(len(albums)))
    title_space = _get_title_space(max_index_len)
    for i, album in enumerate(albums):
        _print_album_title(i, album.title, title_space, max_index_len)


def print_albums_dict(albums: Dict[int, Album]) -> None:
    max_index_len = len(str(max(albums.keys())))
    title_space = _get_title_space(max_index_len)
    for i in albums:
        _print_album_title(i, albums[i].title, title_space, max_index_len)


def _get_title_space(max_index_len: int) -> int:
    terminal_columns = shutil.get_terminal_size().columns
    return terminal_columns - max_index_len - 3  # [, ], ' '

def _print_album_title(index: int, title: str, title_space: int, max_index_len: int):
    if len(title) > title_space:
        title = f"{title[:title_space - 3]}..."
    lb = color("[", Color.BLUE)
    rb = color("]", Color.BLUE)
    ci = color(str(index), Color.GREEN)
    print(f"{lb}{ci}{rb}{' ' * (1 + max_index_len - len(str(index)))}{title}")


def clear_screen() -> None:
    print("\033c", end="")


def write(string: str, col: Color = Color.WHITE):
    print(color(string, col=col))

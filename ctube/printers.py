import shutil
from typing import List
import ctube
from ctube.cmds import Commands
from ctube.colors import color, Color
from ctube.containers import MusicItem


def print_header() -> None:
    print(color("░█▀▀░▀█▀░█░█░█▀▄░█▀▀░", Color.GREEN))
    print(color("░█░░░░█░░█░█░█▀▄░█▀▀░", Color.GREEN))
    print(color("░▀▀▀░░▀░░▀▀▀░▀▀░░▀▀▀░", Color.GREEN))
    print(f"\u2022 {color('version', Color.BOLD)}: {color(ctube.__version__, Color.BLUE)}")
    print("\u2022 source: https://github.com/g3nsy/ctube")
    print("\u2022 Type 'help' to list the available commands")


def print_info(cmd_name: str, verbose: bool = False) -> None:
    try:
        cmd_obj = Commands.get_by_name(cmd_name)
        if verbose:
            print(cmd_obj.value.long_description)
        else:
            print(cmd_obj.value.short_description)
        print(color("Args:", Color.BLUE))
        if cmd_obj.value.args:
            for arg in cmd_obj.value.args:
                print(color(f"{arg.name}:", Color.BOLD), arg.description)
    except KeyError:
        print(color(f"Invalid argument for command 'info': {cmd_name}", Color.RED))
        print(color(f"Valid arguments are {Commands.INFO.value.accepted_args}", Color.RED))


def print_help(verbose: bool = False) -> None:
    print(color(":: Helper", Color.GREEN))
    for cmd in Commands:
        print(f"\u2022 {color(cmd.value.name, Color.BOLD)}:")
        if verbose:
            print(color(cmd.value.long_description, Color.BLUE))
        else:
            print(color(cmd.value.short_description, Color.BLUE))
        print()

def print_centered(string: str) -> None:
    terminal_columns = shutil.get_terminal_size().columns
    spaces = " " * ((terminal_columns // 2) - len(string) // 2)
    print(f"{spaces}{string}")


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

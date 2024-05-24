from typing import Callable, Any
from ctube.cmds import Commands
from ctube.colors import Color, color
from ctube.errors import InvalidIndexSyntax


def handle_invalid_index_syntax(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> None:
        try:
            return func(*args, **kwargs)
        except InvalidIndexSyntax as error:
            print(color(str(error), Color.RED))
    return inner


def handle_extraction(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (KeyError, IndexError, TypeError, ValueError):
            pass
    return inner


def handle_invalid_cmd_args(cmd: Commands) -> Callable:
    accepted_args = cmd.value.accepted_args
    if not accepted_args:
        raise ValueError("Invalid usage")
    def wrapper(func: Callable) -> Callable:
        def inner(*cmd_args: str) -> Any:
            invalid_args = {cmd_arg for cmd_arg in cmd_args[1:] if cmd_arg not in accepted_args}
            if invalid_args:
                print(color(f"Invalid input for command '{cmd.value.name}': {invalid_args}", Color.RED))
            else:
                return func(*cmd_args)
        return inner
    return wrapper

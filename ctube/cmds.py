from enum import Enum
from dataclasses import dataclass
from typing import List, Set, Optional
from ctube.colors import get_color_names


@dataclass
class Command:
    name: str
    description: str
    expected_args: str
    expected_num_args: int
    accepted_args: Optional[Set[str]] = None


class Commands(Enum):
    SEARCH = Command(
        name="search", 
        description="Search by artist name",
        expected_args="<artist name>",
        expected_num_args=1
    )
    ID = Command(
        name="id", 
        description="Search by artist ID",
        expected_args="<artist id>",
        expected_num_args=1
    )
    DOWNLOAD = Command(
        name="download", 
        description="Downloads",
        expected_args="Indexes",
        expected_num_args=-1
    )
    EXIT = Command(
        name="exit", 
        description="Exit the program",
        expected_args="",
        expected_num_args=0
    )
    HELP = Command(
        name="help", 
        description="Print the help message",
        expected_args="",
        expected_num_args=0
    )
    CLEAR = Command(
        name="clear", 
        description="Clear the console",
        expected_args="",
        expected_num_args=0
    )
    INFO = Command(
        name="info", 
        description="Print the info of a specific command",
        expected_args="<command name>",
        expected_num_args=1,
        accepted_args={"search", "id", "exit", "help", "clear", "info"}
    )
    PROMPT_CHAR = Command(
        name="prompt-char",
        description="Change the prompt char",
        expected_args="<char>",
        expected_num_args=1,
    )
    PROMPT_COLOR = Command(
        name="prompt-color",
        description="Change the prompt color",
        expected_args="<color>",
        expected_num_args=1,
        accepted_args=get_color_names()
    )


def get_cmd_with_args() -> List[Commands]:
    return [
        cmd for cmd in Commands 
        if cmd.value.expected_num_args > 0 
        or cmd.value.expected_num_args == -1
    ]


def get_available_cmds_names() -> List[str]:
    return [cmd.value.name for cmd in Commands]


def get_cmd_by_name(cmd_name: str) -> Commands:
    return Commands.__members__[cmd_name.replace("-", "_").upper()]


def is_command(cmd_name: str, cmd: Commands) -> bool:
    return cmd_name == cmd.value.name

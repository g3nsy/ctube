from enum import Enum
from dataclasses import dataclass
from typing import Optional, Type, Set


@dataclass(unsafe_hash=True)
class Argument:
    name: str
    description: str
    type: Type


@dataclass(unsafe_hash=True)
class Option:
    short_name: str
    long_name: str
    required_args: int
    description: Optional[str] = None
    accepted_args: Optional[Set[Argument]] = None
    args: Optional[Set[Argument]] = None


@dataclass(unsafe_hash=True)
class Command:
    name: str
    short_description: str
    long_description: str
    required_args: int
    opts: Optional[Set[Option]] = None
    accepted_args: Optional[Set[Argument]] = None
    args: Optional[Set[Argument]] = None


class Commands(Enum):
    SEARCH = Command(
        name="search", 
        short_description="",
        long_description="",
        required_args=1,
        args={
            Argument(
                name="<artist name>", 
                description="", 
                type=str
            )
        }
    )

    ID = Command(
        name="id", 
        short_description="",
        long_description="",
        required_args=1,
        args={
            Argument(
                name="<artist id>", 
                description="", 
                type=str
            )
        }
    )

    DOWNLOAD = Command(
        name="download", 
        short_description="",
        long_description="",
        required_args=1,
        args={
            Argument(
                name="<indexes>", 
                description="", 
                type=str
            )
        }
    )

    EXIT = Command(
        name="exit", 
        short_description="",
        long_description="",
        required_args=0
    )

    HELP = Command(
        name="help", 
        short_description="",
        long_description="",
        required_args=0,
        opts={
            Option(
                short_name="-v", 
                long_name="--verbose", 
                description="",
                required_args=0
            )
        }
    )

    CLEAR = Command(
        name="clear", 
        short_description="",
        long_description="",
        required_args=0,
    )

    INFO = Command(
        name="info", 
        short_description="",
        long_description="",
        required_args=1,
        accepted_args={
            Argument(name="search", description="The 'search' command", type=str),
            Argument(name="id", description="The 'id' command", type=str),
            Argument(name="exit", description="The 'exit' command", type=str),
            Argument(name="help", description="The 'help' command", type=str),
            Argument(name="clear", description="The 'clear' command", type=str),
            Argument(name="info", description="The 'info' command", type=str)
        }
    )


def get_cmd_with_args() -> Set[Commands]:
    return {cmd for cmd in Commands if cmd.value.required_args > 0}


def get_cmd_by_name(cmd_name: str) -> Commands:
    return Commands.__members__[cmd_name.replace("-", "_").upper()]

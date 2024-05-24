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
        short_description="Searches for and provides music associated with the specified artist name.",
        long_description=(
            "Searches for and provides music associated with the specified artist name.\n"
            "Some artists, although present, are not detected by the algorithm\n"
            "that is responsible for providing the information. In this case\n"
            "you need to consider using the 'id' command. For more information\n"
            "about the 'id' command type 'info id'"
        ),
        required_args=1,
        args={
            Argument(
                name="<artist name>", 
                description="The name of the artist to search for", 
                type=str
            )
        }
    )

    ID = Command(
        name="id", 
        short_description="Searches for and provides music associated with the specified ID.",
        long_description=(
            "Searches for and provides music associated with the specified ID.\n"
            "This command is useful when the artist of interest is not found\n"
            "by the 'search' command. The id can be extracted from the url of\n"
            "the artist's page (music.youtube.com).\n"
            "For example:\n"
            "https://music.youtube.com/channel/UCrpJvPlZprRX930AKTID1KA\n" 
            "                                  ^^^^^^^^^^^^^^^^^^^^^^^^"
        ),
        required_args=1,
        args={
            Argument(
                name="<artist id>", 
                description="the id of the artist to search for", 
                type=str
            )
        }
    )

    DOWNLOAD = Command(
        name="download", 
        short_description="Starts downloading the specified media contents.",
        long_description=(
            "Starts downloading the specified media contents.\n"
            "The contents are specified through the respective indexes.\n"
            "If you intend to download only one content, simply provide\n"
            "its index as an argument to the command.\n"
            "Multiple contents can be specified as follows:\n"
            "\u2022 Indices separated by a comma, for example 0, 1, ...\n"
            "\u2022 A slice that respects the Python syntax, for example\n"
            " 0:3 to download contents with index 0, 1, and 2."
        ),
        required_args=1,
        args={
            Argument(
                name="<indexes>", 
                description="The indexes of musical contents to download.", 
                type=str
            )
        }
    )

    EXIT = Command(
        name="exit", 
        short_description="Exit the program.",
        long_description="Exit the program.",
        required_args=0
    )

    HELP = Command(
        name="help", 
        short_description="Print the help message.",
        long_description=(
            "Print the help message. If the flag -v (or --verbose) is specified\n"
            "a long description of the commands is printed."
        ),
        required_args=0,
        opts={
            Option(
                short_name="-v", 
                long_name="--verbose", 
                description="Adds verbosity to the description of printed commands.",
                required_args=0
            )
        }
    )

    CLEAR = Command(
        name="clear", 
        short_description="Clear the terminal screen.",
        long_description="Clear the terminal screen.",
        required_args=0,
    )

    INFO = Command(
        name="info", 
        short_description="Provides information about the specified command.",
        long_description="Provides information about the specified command.",
        required_args=1,
        args={
            Argument(name="<command name>", description="The name of the command", type=str)
        },
        accepted_args={
            Argument(name="search", description="The 'search' command", type=str),
            Argument(name="id", description="The 'id' command", type=str),
            Argument(name="exit", description="The 'exit' command", type=str),
            Argument(name="help", description="The 'help' command", type=str),
            Argument(name="clear", description="The 'clear' command", type=str),
            Argument(name="info", description="The 'info' command", type=str)
        }
    )

    @classmethod
    def get_by_name(cls, name: str) -> "Commands":
        return cls.__members__[name.replace("-", "_").upper()]

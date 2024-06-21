from enum import Enum
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class _Command:
    name: str
    description: str


class Command(Enum):
    SEARCH = _Command(
        name="search", 
        description=(
            "Searches for and provides music associated with the specified artist name.\n"
            "Some artists, although present, are not detected by the algorithm\n"
            "that is responsible for providing the information. In this case\n"
            "you need to consider using the 'id' command."
        )
    )

    ID = _Command(
        name="id", 
        description=(
            "Searches for and provides music associated with the specified ID.\n"
            "This command is useful when the artist of interest is not found\n"
            "by the 'search' command. The id can be extracted from the url of\n"
            "the artist's page (music.youtube.com).\n"
            "For example:\n"
            "https://music.youtube.com/channel/UCrpJvPlZprRX930AKTID1KA\n" 
            "                                  ^^^^^^^^^^^^^^^^^^^^^^^^"
        )
    )

    DOWNLOAD = _Command(
        name="download", 
        description=(
            "Starts downloading the specified media contents.\n"
            "The contents are specified through the respective indexes.\n"
            "If you intend to download only one content, simply provide\n"
            "its index as an argument to the command.\n"
            "Multiple contents can be specified as follows:\n"
            "\u2022 'all': download all contents.\n"
            "\u2022 Indices separated by a comma, for example 0, 1, ...\n"
            "\u2022 A slice that respects the Python syntax, for example\n"
            " 0:3 to download contents with index 0, 1, and 2."
        )
    )

    FILTER = _Command(
        name="filter",
        description=(
            "Filter the previously listed multimedia contents\n"
            "using the specified regular expression."
        )
    )

    EXIT = _Command(
        name="exit", 
        description="Exit the program."
    )

    HELP = _Command(
        name="help", 
        description="Print the help message."
    )

    CLEAR = _Command(
        name="clear", 
        description="Clear the terminal screen."
    )

    @classmethod
    def get_by_name(cls, name: str) -> "Command":
        return cls.__members__[name.replace("-", "_").upper()]

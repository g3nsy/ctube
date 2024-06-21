import re
import requests
from typing import List , Callable, Dict
from urllib.error import URLError
from httpx import ReadTimeout, ConnectTimeout, ConnectError
from innertube.errors import RequestError
from ctube.containers import Album
from ctube.errors import InvalidIndexSyntax
from ctube.parser import parse_indexes
from ctube.colors import Color
from ctube.printers import write


def filter_albums_by_indexes(albums: List[Album], user_input: str) -> List[Album]:
    selected_indexes = parse_indexes(user_input)
    if not selected_indexes:
        return albums

    elif isinstance(selected_indexes, slice):
        selected_albums = albums[selected_indexes]
        if not selected_albums:
            if selected_indexes.start == selected_indexes.stop - 1:
                raise InvalidIndexSyntax(f"Invalid index: {selected_indexes.start}")
            else:
                raise InvalidIndexSyntax(f"Invalid slice: {selected_indexes.start}:{selected_indexes.stop}")
        else:
            return selected_albums
    else:
        incorrect_indexes: List[int] = []
        for index in selected_indexes:
            if index >= len(albums):
                incorrect_indexes.append(index)
        if incorrect_indexes:
            str_incorrect_indexes = ', '.join(map(str, incorrect_indexes))
            if len(incorrect_indexes) > 1:
                raise InvalidIndexSyntax(f"Invalid indexes: {str_incorrect_indexes}")
            else:
                raise InvalidIndexSyntax(f"Invalid index: {str_incorrect_indexes}")
        else:
            return [albums[index] for index in selected_indexes]


def filter_albums_by_regex(albums: List[Album], pattern: str) -> Dict[int, Album]:
    filtered_albums: Dict[int, Album] = {}
    for i in range(len(albums)):
        res = re.search(string=albums[i].title, pattern=pattern)
        if res:
            filtered_albums[i] = albums[i]
    return filtered_albums


def handle_connection_errors(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestError:
            write("Invalid request", Color.RED)
        except (ConnectTimeout, ReadTimeout):
            write("A timeout error occurred. Try again.", Color.RED)
        except (ConnectError, URLError):
            write("No internet connection", Color.RED)
    return inner


def connected_to_internet(url: str = 'http://www.google.com/', timeout: int = 5) -> bool:
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

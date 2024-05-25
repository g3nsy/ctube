import requests
from typing import List , Callable
from urllib.error import URLError
from httpx import ReadTimeout, ConnectTimeout, ConnectError
from innertube.errors import RequestError
from ctube.containers import MusicItem
from ctube.errors import InvalidIndexSyntax
from ctube.parser import parse_indexes
from ctube.colors import Color
from ctube.printers import write


def get_filtered_music_items(music_items: List[MusicItem], user_input: str) -> List[MusicItem]:
    selected_indexes = parse_indexes(user_input)
    if not selected_indexes:
        return music_items

    elif isinstance(selected_indexes, slice):
        selected_music_items = music_items[selected_indexes]
        if not selected_music_items:
            if selected_indexes.start == selected_indexes.stop - 1:
                raise InvalidIndexSyntax(f"Invalid index: {selected_indexes.start}")
            else:
                raise InvalidIndexSyntax(f"Invalid slice: {selected_indexes.start}:{selected_indexes.stop}")
        else:
            return selected_music_items
    else:
        incorrect_indexes: List[int] = []
        for index in selected_indexes:
            if index >= len(music_items):
                incorrect_indexes.append(index)
        if incorrect_indexes:
            str_incorrect_indexes = ', '.join(map(str, incorrect_indexes))
            if len(incorrect_indexes) > 1:
                raise InvalidIndexSyntax(f"Invalid indexes: {str_incorrect_indexes}")
            else:
                raise InvalidIndexSyntax(f"Invalid index: {str_incorrect_indexes}")
        else:
            return [music_items[index] for index in selected_indexes]


def handle_connection_errors(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestError:
            write("Invalid request", Color.RED)
        except (ConnectTimeout, ReadTimeout):
            write("An error occurred. try again.", Color.RED)
        except (ConnectError, URLError):
            write("No internet connection", Color.RED)
    return inner


def connected_to_internet(url: str = 'http://www.google.com/', timeout: int = 5) -> bool:
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

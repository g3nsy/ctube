from typing import Tuple, List, Optional, Union
from ctube.containers import MusicItem
from ctube.errors import InvalidIndexSyntax


def get_filtered_input(user_input: str) -> Tuple[str, str]:
    splitted_user_input = user_input.split()
    prefix = splitted_user_input[0]
    arg = ' '.join(splitted_user_input[1:])
    return prefix, arg


def get_filtered_music_items(music_items: List[MusicItem], user_input: str) -> List[MusicItem]:
    selected_indexes = get_selected_indexes(user_input)
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


def get_selected_indexes(string: str) -> Optional[Union[slice, List[int]]]:
    if string.lower() == "all":
        return None
    else:
        # x
        if string.isdigit():
            return slice(int(string), int(string) + 1)

        # x: y
        double_points_splitted_string = string.split(":")
        if len(double_points_splitted_string) > 1:
            if len(double_points_splitted_string) != 2:
                raise InvalidIndexSyntax("Missing stop index.")

            first, second = double_points_splitted_string
            if not first.isdigit() or not second.isdigit():
                raise InvalidIndexSyntax("Indexes must be integers.")

            first, second = int(first), int(second)
            if first < 0 or second < 0 or second <= first:
                raise InvalidIndexSyntax("Indexes must be positive integers.")

            return slice(first, second)

        # x, y, ..., z
        comma_splitted_string = string.split(",")
        if len(comma_splitted_string) > 1:
            try:
                indexes = list(map(int, comma_splitted_string))
            except ValueError:
                raise InvalidIndexSyntax("Indexes must be integers.")

            filtered_indexes: List[int] = []
            for index in indexes:
                if index < 0:
                    raise InvalidIndexSyntax("Indexes must be positive integers.")
                if index not in filtered_indexes:
                    filtered_indexes.append(index)
            return filtered_indexes
        raise InvalidIndexSyntax(f"Invalid index syntax: {string}")

from typing import Tuple, List, Optional, Union
from ctube.decorators import handle_invalid_index_syntax
from ctube.colors import color, Color
from ctube.containers import MusicItem
from ctube.errors import InvalidIndexSyntax


def get_filtered_input(user_input: str) -> Tuple[str, str]:
    splitted_user_input = user_input.split()
    prefix = splitted_user_input[0]
    arg = ' '.join(splitted_user_input[1:])
    return prefix, arg


@handle_invalid_index_syntax
def get_filtered_music_items(music_items: List[MusicItem], user_input: str) -> Optional[List[MusicItem]]:
    selected_indexes = get_selected_indexes(user_input)
    if not selected_indexes:
        return music_items

    elif isinstance(selected_indexes, slice):
        selected_music_items = music_items[selected_indexes]
        if not selected_music_items:
            if selected_indexes.start == selected_indexes.stop + 1:
                print(color("Invalid index", Color.RED))
            else:
                print(color("Invalid slice", Color.RED))
        else:
            return selected_music_items
    else:
        incorrect_indexes: List[int] = []
        for index in selected_indexes:
            if index >= len(music_items):
                incorrect_indexes.append(index)
        if incorrect_indexes:
            print(f"Invalid indexes: {', '.join(map(str, incorrect_indexes))}")
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
                raise InvalidIndexSyntax

            first, second = double_points_splitted_string
            
            if not first.isdigit() or not second.isdigit():
                raise InvalidIndexSyntax

            first, second = int(first), int(second)

            if first < 0 or second < 0 or second <= first:
                raise InvalidIndexSyntax

            return slice(first, second)

        # x, y, ..., z
        comma_splitted_string = string.split(",")
        if len(comma_splitted_string) > 1:
            try:
                indexes = list(map(int, comma_splitted_string))
            except ValueError:
                raise InvalidIndexSyntax

            filtered_indexes: List[int] = []
            for index in indexes:
                if index < 0:
                    raise InvalidIndexSyntax
                if index not in filtered_indexes:
                    filtered_indexes.append(index)

            return filtered_indexes

        raise InvalidIndexSyntax



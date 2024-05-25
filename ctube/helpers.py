from typing import List 
from ctube.containers import MusicItem
from ctube.errors import InvalidIndexSyntax
from ctube.parser import parse_indexes


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

from typing import Tuple, Optional, Union, List
from ctube.errors import InvalidIndexSyntax


def parse_user_input(user_input: str) -> Tuple[str, str]:
    splitted_user_input = user_input.split()
    prefix = splitted_user_input[0]
    arg = ' '.join(splitted_user_input[1:])
    return prefix, arg


def parse_indexes(string: str) -> Optional[Union[slice, List[int]]]:
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

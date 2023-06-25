"""
A collection of functions that performs list handling operations within a script.
"""

__name__ = "__main__"

from typing import Optional


# system modules, packages, libraries, and programs ###


def get_first_element(a_list_item: Optional[list | tuple]) -> str:
    """ gets the first element of a list or tuple"""

    return a_list_item[0]

def get_second_element(a_list_item: Optional[list | tuple]) -> str:
    """ gets the second element of a list or tuple"""

    return a_list_item[1]

def get_at_least_fifth_element(a_list_item: Optional[list | tuple]) -> str:
    """ gets at least fifth element of a list or tuple"""

    return a_list_item[4:]

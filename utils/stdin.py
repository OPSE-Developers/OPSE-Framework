# -*- coding: utf-8 -*-

from utils import NOP, YES
from utils.stdout import print_error, print_log

def get_int(msg: str = "") -> int:
    """Helper to get an integer from a user input.
    
    It handles integer input basic errors.

    :param msg: The message to display before the input, defaults to "".
    :type msg: str, optional
    :return: The integer from the input.
    :rtype: int
    """
    valid = False
    while not valid:
        try:
            if msg != "":
                print_log(msg=msg, display=False)

            number = input(msg)
            valid = True
            number = int(number)
            print_log(msg="(INPUT) " + str(number), display=False)
            return number

        except ValueError:
            valid = False
            print_error(" Input is not a valid number")

def get_yes_or_no(msg: str = "") -> bool:
    """Helper to responde a Yes or No question. 

    :param msg: The message to display before input, defaults to ""
    :type msg: str, optional
    :return: True if answer is positive (yes), else False for negative (no).
    :rtype: bool
    """
    valid: bool = False
    while not valid:
        response = input(msg + " [y/N] ")
        valid = (response in YES or response in NOP) or not (response == '\n')
    return response in YES
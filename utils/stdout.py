# -*- coding: utf-8 -*-

import logging
import os

from datetime import date
from typing import List

from utils.config.Config import Config
from utils.utils import remove_plural, whoami


class Colors:
    """
    Class that defines the colors used in output display.
    """    
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ITALIC = "\033[3m"


def clear():
    """Clear stdout."""
    print(os.get_terminal_size().lines*"\033E"+"\033[H")


def print_warning(msg: str = "", on_debug_only: bool = False):
    """Function that displays a warning message.

    :param msg: The message to display, defaults to "".
    :type msg: str, optional
    :param on_debug_only: Setting to display only in debug, defaults to
     False.
    :type on_debug_only: bool, optional
    """
    if on_debug_only and not Config.is_debug():
        return
    print_log(Colors.WARNING + "[WARNING]" + str(msg) + Colors.ENDC,
              logging.WARNING)


def print_error(msg: str = "", on_debug_only: bool = False):
    """Function that displays an error message.

    :param msg: The message to display, defaults to "".
    :type msg: str, optional
    :param on_debug_only: Setting to display only in debug, defaults to
     False.
    :type on_debug_only: bool, optional
    """
    if on_debug_only and not Config.is_debug():
        return
    print_log(Colors.FAIL + "[ERREUR]" + str(msg) + Colors.ENDC,
              logging.ERROR)


def print_sucess(msg: str = "", on_debug_only: bool = False):
    """Function that displays a success message.

    :param msg: The message to display, defaults to "".
    :type msg: str, optional
    :param on_debug_only: Setting to display only in debug, defaults to
     False.
    :type on_debug_only: bool, optional
    """
    if on_debug_only and not Config.is_debug():
        return
    print_log(Colors.OKGREEN + "[OK]" + str(msg) + Colors.ENDC)


def print_debug(msg: str = ""):
    """Function that displays a debug message.

    :param msg: The message to display, defaults to "".
    :type msg: str, optional
    """
    msg = str(msg)
    debug_str = "[DEBUG]" + whoami() + " "

    if len(msg) > 0:
        if msg[:1] == "\n":
            debug_str = "\n" + debug_str
            msg = msg[1:]
    else:
        debug_str = ""

    print_log(
        debug_str + Colors.ITALIC + str(msg) + Colors.ENDC,
        logging.DEBUG,
        Config.is_debug(),
    )


def print_title(msg: str = ""):
    """Function that displays a title message.

    :param msg: The message to display, defaults to "".
    :type msg: str, optional
    """
    print_log(Colors.HEADER + str(msg) + Colors.ENDC)


def print_log(msg: str = "", log_level: int = logging.INFO,
              display: bool = True):
    """Function that manage logs. It is used to log message and display
    them on stdout during execution.

    See :py:mod:`~logging` for more details.

    :param msg: The message to log, defaults to ""
    :type msg: str, optional
    :param log_level: The logging level, defaults to
     :py:data:`INFO <~logging.INFO>`.
    :type log_level: int, optional
    :param display: Setting to display log message on stdout, defaults
     to True.
    :type display: bool, optional
    """
    if display:
        print(msg)
    if log_level == logging.INFO:
        logging.info(msg.replace("\n", " "))
    elif log_level == logging.DEBUG:
        logging.debug(msg.replace("\n", " "))
    elif log_level == logging.WARN:
        logging.warning(msg.replace("\n", " "))
    elif log_level == logging.WARNING:
        logging.warning(msg.replace("\n", " "))
    elif log_level == logging.ERROR:
        logging.error(msg.replace("\n", " "))
    elif log_level == logging.CRITICAL:
        logging.critical(msg.replace("\n", " "))


def print_menu(title: str, proposed_items: List[str], special_opts: List[str] = []):
    """Function to print a menu with simple selection.

    :param title: Title of the menu
    :type title: str
    :param proposed_items: List of choices
    :type proposed_items: List[str]
    :param special_opts: Special options, like 'validate', 'continue', etc, defaults to []
    :type special_opts: List[str], optional
    """
    print_title(title)
    for index, item in enumerate(proposed_items):
        print("\t- (" + str(index) + ") " + str(item))

    print()
    for index, opt in enumerate(special_opts):
        print("\t- (" + str(len(proposed_items) + index) + ") " + opt)
    print()


def show(dictionary: dict, depth: list[bool], name: str = "Name") -> str:
    """Function that builds a string as a tree to display complex object
    structures.

    This function is recursive. The dictionary used should not point to
    itself and its attributes should not loop to themselves.

    :param dictionary: The dictionary to convert.
    :type dictionary: dict
    :param depth: The current depth of the call.
    :type depth: list[bool]
    :param name: The name of the current dictionary, defaults to "Name".
    :type name: str, optional
    :return: A string representation of the dictionary.
    :rtype: str
    """
    string: str = ""

    string += "[*] " + name + " " + str(hex(id(dictionary))) + "\n"

    try:
        active_attr = dictionary
    except Exception as e:
        print_error(str(e))

    for (index, attr) in enumerate(active_attr):

        for b in depth:
            if b == 1:
                string += " |   "
            else:
                string += "     "
            string += " "

        if index != (len(active_attr) - 1):
            string += " |--- "
        else:
            string += " \--- "

        attr_name = attr.split("__")[-1].replace('lst_', '').capitalize().replace('_', ' ')
        attr_value = dictionary[attr]

        if isinstance(attr_value, list):

            if index != (len(active_attr) - 1):
                depth.append(1)
            else:
                depth.append(0)

            string += "[+] " + attr_name + ": (" + str(len(attr_value)) + ")\n"

            for (lst_index, lst_elem) in enumerate(attr_value):
                for b in depth:
                    if b == 1:
                        string += " |   "
                    else:
                        string += "     "
                    string += " "

                if lst_index != (len(attr_value) - 1):
                    string += " |--- "
                    depth.append(1)
                else:
                    string += " \--- "
                    depth.append(0)

                if isinstance(lst_elem, (str, int, float, bool, date)):
                    string += str(lst_elem) + "\n"
                    if lst_index == (len(attr_value) - 1):
                        for b in depth:
                            if b == 1:
                                string += " |   "
                            else:
                                string += "     "
                            string += " "
                        string += "\n"
                else:
                    string += show(lst_elem, depth, remove_plural(attr_name))

                depth.pop()
            depth.pop()

        elif isinstance(attr_value, dict):

            if index != (len(active_attr) - 1):
                depth.append(1)
            else:
                depth.append(0)

            string += show(attr_value, depth, attr_name)
            depth.pop()
        else:
            string += attr_name + ": "
            string += str(attr_value)[:100] + "\n"

        if index == (len(active_attr) - 1):
            for b in depth:
                if b == 1:
                    string += " |   "
                else:
                    string += "     "
                string += " "
            string += "\n"

    return string
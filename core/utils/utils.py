#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import date
from datetime import datetime

import requests
from requests import RequestException
from utils.config.Config import Config
from utils.Colors import bcolors
from classes.Profile import Profile
from classes.types.OpseType import OpseType


def clear():
    """Clear stdout."""
    os.system('cls' if os.name == 'nt' else 'clear -x')


def init_log_path():
    """Function that initializes the log directory path if it doesn't
    exist.
    """
    if not os.path.exists(Config.get()["config"]["log_path"]):
        print("\nLog directory create in '" + str(Config.get()["config"]["log_path"]) + "'")
        os.makedirs(Config.get()["config"]["log_path"], mode=0o777)


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
    print_log(bcolors.WARNING + "[WARNING]" + str(msg) + bcolors.ENDC,
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
    print_log(bcolors.FAIL + "[ERREUR]" + str(msg) + bcolors.ENDC,
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
    print_log(bcolors.OKGREEN + "[OK]" + str(msg) + bcolors.ENDC)


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
        debug_str + bcolors.ITALIC + str(msg) + bcolors.ENDC,
        logging.DEBUG,
        Config.is_debug(),
    )


def print_title(msg: str = ""):
    """Function that displays a title message.

    :param msg: The message to display, defaults to "".
    :type msg: str, optional
    """
    print_log(bcolors.HEADER + str(msg) + bcolors.ENDC)


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


def whoami(depth: int = 2) -> str:
    """Function that returns a whoami's function tag for debugging.

    The tag contains the name of the current function and its file.

    For example, if the :py:func:`~core.utils.utils.print_debug`
    function is called in :py:func:`~core.Opse.main` function in
    `Opse.py`, it would return "[Opse:main]".

    :param depth: Depth of the function call, defaults to 2.
    :type depth: int, optional
    :return: A string containing file name and function name.
    :rtype: str
    """
    frame = sys._getframe(depth)
    file = frame.f_code.co_filename.split('\\' if os.name == 'nt' else '/')[-1][:-3].capitalize()
    func = frame.f_code.co_name
    return "[" + file + ":" + func + "]"


def to_dict(obj: object, display_none_value: bool = False) -> dict:
    """Function that builds a dictionary from complex object
    structures.

    :param obj: The object to transform.
    :type obj: object
    :param display_none_value: Setting to continue displaying None
     attributes values, defaults to False.
    :type display_none_value: bool, optional
    :return: A dictionary containing the object.
    :rtype: dict
    """
    dict = {}
    active_attr = obj.__dict__
    for (index, attr) in enumerate(active_attr):

        attr_name = attr.split("__")[-1]
        attr_value = getattr(obj, attr)

        if isinstance(attr_value, list):

            dict[attr_name] = []

            for (lst_index, lst_elem) in enumerate(attr_value):

                if isinstance(lst_elem, (str, int, float, bool, date)):
                    dict[attr_name].append(str(lst_elem))
                elif not isinstance(lst_elem, Profile):
                    dict[attr_name].append(to_dict(lst_elem))

        elif isinstance(getattr(obj, attr, None), (OpseType)):
            dict[attr_name] = to_dict(getattr(obj, attr, None))
        elif not isinstance(attr, Profile):
            if str(getattr(obj, attr, None)):
                if display_none_value:
                    dict[attr_name] = str(getattr(obj, attr, None))
                elif str(getattr(obj, attr, None)) != "None":
                    dict[attr_name] = str(getattr(obj, attr, None))

    return dict


def remove_plural(plural_word: str) -> str:
    """Function that removes plural in English words.

    :param plural_word: The word in the plural. 
    :type plural_word: str
    :return: A word in singular.
    :rtype: str
    """
    return plural_word if plural_word[len(plural_word)-1] != 's' else plural_word[:-1]


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


def get_today_date(format: str = "%d/%m/%Y") -> str:
    """Function that returns today's date in a specific format.

    See :py:meth:`~datetime.date.today` and
    :py:meth:`~datetime.date.strftime` for more details.

    :param format: The format wanted, defaults to "%d/%m/%Y".
    :type format: str, optional
    :return: A string containing today's date.
    :rtype: str
    """
    return date.today().strftime(format)


def is_valid_date(date_str: str, format: str = "%d/%m/%Y") -> bool:
    """Function that tests the validity of a date in a specific format.

    :param date_str: The date to test.
    :type date_str: str
    :param format: The date format, defaults to "%d/%m/%Y".
    :type format: str, optional
    :return: True if the date is correct, else False.
    :rtype: bool
    """
    try:
        datetime.strptime(date_str, format)
        return True
    
    except ValueError:
        return False


def get_dict_key_by_index(dictionary : dict, index: int) -> any:
    """Function that returns a key stored at a specific index in a
    dictionary.

    :param dictionary: The dictionary.
    :type dictionary: dict
    :param index: The index of the wanted key.
    :type index: int
    :return: The key stored at the index.
    :rtype: any
    """
    cpt = 0
    for key in dictionary:
        if cpt == index:
            return key
        cpt += 1
    return None


def is_url_image(image_url: str) -> bool:
    """Function that tests if a URL is pointing to an image.

    The supported image formats are PNG, JPG and JPEG.

    :param image_url: The URL to test.
    :type image_url: str
    :return: True if the URL points to an image, else False.
    :rtype: bool
    """
    try:

        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)

        if r.headers["content-type"] in image_formats:
            print_debug(str(image_url) + " is picture")
            return True
        print_debug(str(image_url)+ " is not picture --> Wrong format")
        return False

    except RequestException as e:
        print_debug(str(image_url) + " is not picture --> Wrong format" + str(e))
        return False

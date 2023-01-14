# -*- coding: utf-8 -*-

import importlib
import importlib.util
import os
import pkgutil
import requests
import sys
from typing import Any, Dict

from datetime import date, datetime
from requests import RequestException

from classes.Profile import Profile
from classes.types.OpseType import OpseType
from utils.config.Config import Config
# from utils.stdout import print_debug


def init_log_path():
    """Function that initializes the log directory path if it doesn't
    exist.
    """
    if not os.path.exists(Config.get()["config"]["log_path"]):
        print("\nLog directory create in '" + str(Config.get()["config"]["log_path"]) + "'")
        os.makedirs(Config.get()["config"]["log_path"], mode=0o777)


def import_subclasses(mother_class, subclasses_package_name: str) -> Dict[str, Any]:
    """Method that tries to import every subclasses it finds in the specified package 
    directory.

    It stores all available/loaded/imported subclasses in a dictionary.

    Subclasses must have the mother class' name as sufix.
    Example: Mother and ChildMother

    :param mother_class: The abstract class mother of the subclasses.
    :param subclasses_package_name: Directory's name (Python package).
    :type subclasses_package_name: str
    """
    package = subclasses_package_name
    if isinstance(package, str):
        package = importlib.import_module(package)

    lst_available_subclasses: Dict[str, mother_class] = {}
    for loader, sub_package, is_pkg in pkgutil.walk_packages(package.__path__):

        try:
            if is_pkg:

                for _, module_name, _ in pkgutil.walk_packages([os.path.join(package.__path__[0], sub_package)]):
                    full_name = package.__name__ + '.' + sub_package + '.' + module_name

                    mod_type = importlib.import_module(full_name)
                    module = getattr(mod_type, module_name + mother_class.__name__, None)

                    if module is None:
                        continue

                    if issubclass(module, mother_class):
                        lst_available_subclasses[full_name] = module
            else:
                if sub_package != mother_class.__name__:
                    print("[WARNING] " + sub_package + " can not be import because it is not a package.")

        except Exception as e:
            print("[DEBUG] Error while importing " + sub_package + ". " + str(e))
            continue

    return lst_available_subclasses


def whoami(depth: int = 2) -> str:
    """Function that returns a whoami's function tag for debugging.

    The tag contains the name of the current function and its file.

    For example, if the :py:func:`~utils.utils.print_debug`
    function is called in :py:func:`~Opse.main` function in
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
            # print_debug(str(image_url) + " is picture")
            return True
        # print_debug(str(image_url)+ " is not picture --> Wrong format")
        return False

    except RequestException as e:
        # print_debug(str(image_url) + " is not picture --> Wrong format" + str(e))
        return False


def verify_date(input_date):
  try:
    datetime.strptime(input_date, '%Y%m%d')
    return True
  except ValueError:
    return False


def check_py_version():
    if not sys.version_info >= (3,8):
        print("Python 3.8 or higher is required.")
        print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
        sys.exit(1)
# -*- coding: utf-8 -*-
# Author : FengWan

import pathlib
import yaml


class Config:
    """
    Class that defines OPSE configuration.
    
    It generates a configuration file from a default configuration.
    Once the configuration file is modified by the user, it gets the
    user's configuration to improve OPSE usage.
    """
    __config: dict = {}

    def __init__(self):
        pass

    @staticmethod
    def update_map(default_map: dict, current_map: dict):
        """Method that updates a dictionary from another.

        From the default dictionary, updates the current dictionary as:

        - Check that all keys from the default dictionary are present in
          the current dictionary ;
        - Check that attribute's values have the same type in both
          dictionaries.

        This method ensures that the user configuration file will
        respect the script's needs and will not raises errors such as:

        - KeyError ;
        - TypeError ;
        - ...

        :param default_map: The default dictionary.
        :type default_map: dict
        :param current_map: The dictionary to update.
        :type current_map: dict
        """
        for key in default_map.keys():
            if key not in current_map.keys():
                # If the key doesn't exist
                # We initialize it to the default value
                current_map[key] = default_map[key]
            elif type(default_map[key]) is dict and type(current_map[key]) is dict:
                # We compare recursively sub-dictionaries
                Config.update_map(default_map[key], current_map[key])
            elif not isinstance(default_map[key], type(current_map[key])):
                # If two values at the same key have not the same type
                # We override the current value by the default value
                current_map[key] = default_map[key]

        # We remove keys from the current configuration that are not in
        # the default configuration
        lst_key_to_remove = []
        for key in current_map.keys():
            if key not in default_map.keys():
                lst_key_to_remove.append(key)
        
        for key in lst_key_to_remove:
            current_map.pop(key)

    @staticmethod
    def update_config(default_config: dict):
        """Method that updates user's configuration.

        :param default_config: Default configuration.
        :type default_config: dict
        """
        current_config = {}
        try:
            with open("config.yml", "r") as ymlfile:
                current_config = yaml.load(ymlfile, yaml.Loader)
            Config.update_map(default_config, current_config)

        except FileNotFoundError:
            current_config = default_config
        
        # We apply changes
        Config.__config = current_config
        with open("config.yml", "w") as new_conf:
            yaml.dump(current_config, new_conf, default_flow_style=False)

    @staticmethod
    def set_debug(activate: bool):
        """Setter of debug mode.
        It allows to enable debug mode without changing the
        configuration file.
        
        This method is necessary for command line arguments.

        :param activate: Setting of debug mode, True to enable it, False
         to disable it.
        :type activate: bool
        """
        Config.get()["config"]["debug"] = activate

    @staticmethod
    def set_strict(activate: bool):
        """Setter of strict mode.
        It allows to enable strict mode without changing the
        configuration file.
        
        This method is necessary for command line arguments.
        :param activate: Setting of strict mode, True to enable it,
         False to disable it.
        :type activate: bool
        """
        Config.get()["config"]["strict"] = activate

    @staticmethod
    def is_debug() -> bool:
        """Return whether the program is in debug mode.

        :return: True if debug mode is enabled, else False.
        :rtype: bool
        """
        return bool(Config.get()["config"]["debug"])

    @staticmethod
    def is_strict() -> bool:
        """Return whether the program is in strict mode.
        :return: True if strict mode is enabled, else False.
        :rtype: bool
        """
        return bool(Config.get()["config"]["strict"])

    @staticmethod
    def read():
        """Read config.yml file to store OPSE configuration.
        """
        try:
            with open("config.yml", "r") as ymlfile:
                Config.__config = yaml.load(ymlfile, yaml.Loader)

        except FileNotFoundError:
            raise

    @staticmethod
    def get() -> dict:
        """Return the current configuration.

        If the configuration does not exist or if the configuration is
        incomplete, adds the missing entries to the configuration file.

        :return: The current configuration.
        :rtype: dict
        """
        return Config.__config


def get_default_config() -> dict:
    """Return the default configuration.

    :return: A dictionary containing the default configuration.
    :rtype: dict
    """

    default_config = {}
    config = {}

    # Create default configuration
    config["api"] = {"port": 6060, "is_in_dev_mode": False, "unsafe": False, "host": "0.0.0.0"}
    config["debug"] = False
    config["log_path"] = str(pathlib.Path(__file__).parent.parent.absolute()) + "/log"
    config["max_file_log"] = 14
    config["tools"] = {}
    config["strict"] = True

    # Create the fully complete dictionary
    default_config = {}
    default_config["config"] = config

    return default_config

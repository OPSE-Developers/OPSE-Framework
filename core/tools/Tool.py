#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import pkgutil
import importlib
from abc import ABC
from time import sleep
from typing import Type, TypeVar

from classes.Profile import Profile
from exceptions.ToolGetProfileDuringExecutionException import ToolGetProfileDuringExecutionException
from utils.config.Config import Config
from utils.Task import Task
from utils.utils import print_debug, print_sucess, print_warning


T = TypeVar('T', bound='Tool')

class Tool(Task, ABC):
    """
    Class that represents a Tool in OPSE context.

    In OPSE, a Tool is a process which produce a Profile from input
    data. The Profile could produce more information than the beginning.
    """
    lst_available_tools: dict = {}
    lst_active_tools: list = []

    def __init__(self):
        """Constructor of a Tool."""
        super().__init__()

        # Profile which will be return when the Tool finish its job
        self.__default_profile: Profile = None
        self.__result_profiles: list[Profile] = []

    def launch(self, default_profile: Profile):
        """Method that launches the current tool with a default profile.

        :param default_profile: The default profile.
        :type default_profile: Profile
        """
        print_debug("Asking input for " + str(self.get_lst_input_data_types()))
        print_debug("Calling tool with " + str(default_profile.get_lst_data_type()))

        self.__default_profile = default_profile
        self.start()

    def get_default_profile(self) -> Profile:
        """Getter of the default profile.

        :return: The default profile.
        :rtype: Profile
        """
        return self.__default_profile

    def get_profiles(self) -> list[Profile]:
        """Method that returns the list of
        :py:class:`~core.classes.Profile` generated by this tool.

        :raises ToolGetProfileDuringExecutionException: If the method is
         called during execution.
        :return: The list of generated profiles.
        :rtype: list[Profile]
        """
        if self.is_running():
            raise ToolGetProfileDuringExecutionException

        return self.__result_profiles

    def append_profile(self, profile: Profile):
        """Method that adds a profile to the tool's profiles list.

        :param profile: The profile to add.
        :type profile: Profile
        """
        self.__result_profiles.append(profile)

    @staticmethod
    def get_config() -> dict:
        """Method that returns the tool default configuration as a
        dictionary.

        :return: The tool's default configuration.
        :rtype: dict
        """
        return {}

    @staticmethod
    def get_lst_input_data_types() -> dict[str, bool]:
        """Method that returns the list of data types that can be use to
        run this Tool.

        The returned dictionary contains a string as key representing
        the data type, and a boolean as value representing if the data
        type is require or optional.

        :return: A dictionary containing the input data types.
        :rtype: dict[str, bool]
        """
        return {}

    @staticmethod
    def get_lst_output_data_types() -> list[str]:
        """Method that returns the list of data types that can be
        receive by using this Tool.

        :return: _description_
        :rtype: list[str]
        """
        return []

    @classmethod
    def get_name(cls) -> str:
        """Getter of the class name.

        :return: The name of the class.
        :rtype: str
        """
        return cls.__name__

    @classmethod
    def is_active(cls) -> bool:
        """Return whether the tool is enabled.

        All tool are disabled in the default configuration.

        :raises UserWarning: If the tool is not configured.
        :return: True if the tool is enabled, else False.
        :rtype: bool
        """
        tool_is_active: bool = Config.get().get('config', {}).get('tools', {}).get(cls.get_name().lower(), {}).get('active', None)
        if tool_is_active is None:
            raise UserWarning(" Tool is not configured. See documentation.")
        return tool_is_active

    @classmethod
    def is_deprecated(cls) -> bool:
        """Return whether the tool is deprecated.

        :raises UserWarning: If the tool is not configured.
        :return: True if the tool is deprecated, else False.
        :rtype: bool
        """
        tool_is_deprecated: bool = Config.get().get('config', {}).get('tools', {}).get(cls.get_name().lower(), {}).get('deprecated', None)
        if tool_is_deprecated is None:
            raise UserWarning(" Tool is not configured. See documentation.")
        return tool_is_deprecated

    @classmethod
    def import_tools(cls):
        """Method that tries to import every tools it finds in the tools
        directory.
        
        It stores all available/loaded/imported tools in the class
        variable lst_available_tools.
        """
        package = "tools"
        if isinstance(package, str):
            package = importlib.import_module(package)

        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):

            try:
                if is_pkg:
                    # print(os.path.join(package.__path__[0], name))
                    for _, sub_name, _ in pkgutil.walk_packages([os.path.join(package.__path__[0], name)]):
                        full_name = package.__name__ + '.' + name + '.' + sub_name

                        m = getattr(importlib.import_module(full_name), sub_name + 'Tool', None)

                        if m is None:
                            continue

                        if issubclass(m, Tool):
                            cls.lst_available_tools[full_name] = m
                # else:
                #     print_warning("[DEBUG] " + name + " can not be import because it is not a package.", True)

            except Exception as e:
                # print("[DEBUG] Error while importing " + name + ". " + str(e), True)
                continue

    @classmethod
    def get_lst_active_tools(cls: Type[T]) -> list[T]:
        """Return the OPSE active tools list.

        :return: The list of active tools.
        :rtype: list[Tool]
        """
        tool: Tool
        for tool in cls.lst_available_tools.values():

            if tool.is_active():
                print_sucess(" Plugin " + tool.get_name() + " has been loaded.")

                cls.lst_active_tools.append(tool)

                if tool.is_deprecated():
                    print_warning(" Plugin " + tool.get_name() + " is deprecated. You should not use it.")

            else:
                print_warning(" Plugin " + tool.get_name() + " is not active.")

        sleep(3)
        return cls.lst_active_tools

    @classmethod
    def get_tool_config(cls) -> dict[str, dict]:
        """Method that returns all tools configuration as a dictionary.

        :return: A dictionary of 'tool':'config'.
        :rtype: dict[str, dict]
        """
        cls.import_tools()

        tool: Tool
        config = {}
        for tool in cls.lst_available_tools.values():

            tool_name = tool.get_name().lower()

            if tool_name not in config:
                config[tool_name] = tool.get_config()

            # Init mandatory default value in each Tool config
            # print(tool_name + ": " + str(config[tool_name])) # DEBUG only

            if "active" not in config[tool_name]:
                config[tool_name]["active"] = False

            elif not isinstance(config[tool_name]["active"], bool):
                config[tool_name]["active"] = False
                # print_debug("CONFIG ERROR : " + tool_name + ">active is not set as an boolean. Value reset to False")

            if "deprecated" not in config[tool_name]:
                config[tool_name]["deprecated"] = False

            elif not isinstance(config[tool_name]["deprecated"], bool):
                config[tool_name]["deprecated"] = False
                # print_debug("CONFIG ERROR : " + tool_name + ">deprecated is not set as an boolean. Value reset to False")

        print(config)
        return config

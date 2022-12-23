#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pathlib
from tools.Tool import Tool


def get_default_config() -> dict:
    """Return the default configuration.

    :return: A dictionary containing the default configuration.
    :rtype: dict
    """

    default_config = {}
    config = {}
    text = {}

    # Create default configuration
    config["debug"] = False
    config["strict"] = True
    config["log_path"] = str(pathlib.Path(__file__).parent.parent.absolute()) + "/log"
    config["max_file_log"] = 14
    config["api"] = {"port": 6060, "is_in_dev_mode": False, "unsafe": False, "host": "0.0.0.0"}
    config["tools"] = Tool.get_tool_config()

    # Create default message to esy create language file
    text_error = {}
    text_fonctionnality = {}
    text["error"] = text_error
    text["fonctionnality"] = text_fonctionnality

    # Create the fully complete dictionary
    default_config["Opse"] = {}
    default_config["Opse"]["config"] = config
    default_config["Opse"]["text"] = text

    return default_config

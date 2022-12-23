#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ToolMissDataInputException(Exception):
    """
    This exception is derived from Exception.
    It is raised when an OPSE tool is ask to run without all required
    input data.
    """

    def __init__(self):
        super().__init__()

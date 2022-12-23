#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ToolGetProfileDuringExecutionException(Exception):
    """
    This exception is derived from Exception.
    It is raised when an OPSE tool is ask to return profiles while it is
    still running.
    """

    def __init__(self):
        super().__init__()

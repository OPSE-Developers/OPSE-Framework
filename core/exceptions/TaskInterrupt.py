#!/usr/bin/python3
# -*- coding: utf-8 -*-


class TaskInterrupt(Exception):
    """
    This exception is derived from Exception.
    It is thrown into a specific thread when a PreviousException has
    been raised. It allows the program to shutdown all running threads.
    """

    def __init__(self):
        super().__init__()

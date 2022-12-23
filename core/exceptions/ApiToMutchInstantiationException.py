#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ApiToMutchInstantiationException(Exception):
    """
    This exception is derived from Exception.
    It is Raised when more than one API is instantiated.
    """

    def __init__(self):
        super().__init__()


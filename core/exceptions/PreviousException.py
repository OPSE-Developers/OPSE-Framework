#!/usr/bin/python3
# -*- coding: utf-8 -*-


class PreviousException(Exception):
    """
    This exception is derived from Exception.
    It is Raised when a :py:data:`~signal.SIGINT` is detected by the
    :py:func:`~signal.signal` function.
    """
    
    def __init__(self):
        super().__init__()

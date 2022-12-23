#!/usr/bin/python3
# -*- coding: utf-8 -*-
from exceptions.PreviousException import PreviousException
from utils.Task import Task
from utils.utils import clear, print_debug


def previous():
    """
    Function that raise a :py:class:`PreviousException
    <core.exceptions.PreviousException>`.

    :raises PreviousException: CTRL-C Exception.
    """
    print_debug("CTRL-C")
    raise PreviousException


def reset(clear: bool = True):
    """
    Function that resets environnement.
    
    It stops properly all tasks and clear stdout.

    :param clear: Set display erasing, defaults to True.
    :type clear: bool, optional
    """
    for task in Task.get_tasks():
        task.interrupt()

    if clear:
        clear()
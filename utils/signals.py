# -*- coding: utf-8 -*-

from utils.exceptions import PreviousException
from utils.stdout import clear, print_debug
from utils.Task import Task


def previous(signal_received, frame):
    """
    Function that raise a :py:class:`PreviousException
    <utils.exceptions.PreviousException>`.

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
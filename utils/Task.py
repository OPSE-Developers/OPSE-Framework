# -*- coding: utf-8 -*-

import ctypes
import threading
import traceback

from abc import ABC, abstractmethod
from typing import List, Type, TypeVar

from utils.stdout import print_error, print_debug
from utils.exceptions import TaskInterrupt


T = TypeVar('T', bound='Task')

class Task(ABC, threading.Thread):
    """
    Class that represents a task during OPSE execution.
    It is used by the :py:class:`~tool.Tool` class and the
    :py:class:`~api.Api` class.
    """

    __lst_task = []

    def __init__(self):
        """Constructor of a Task."""
        super().__init__()

        self.__is_running = False
        self.__lst_task.append(self)

    @classmethod
    def get_tasks(cls: Type[T]) -> List[T]:
        """
        Return the list of all the tasks instantiated.

        :return: List of instantiated tasks.
        :rtype: List[Task]
        """        
        return cls.__lst_task

    @abstractmethod
    def execute(self):
        """
        Method representing the task's job.

        This method should be override in each Task.
        """
        pass

    def run(self):
        """
        Method representing the task's activity.
        Overloads the thread's :py:meth:`run <threading.Thread.run>`
        method.
        
        It adds error and interruption management.
        Each Task can interrupt or be interrupted during execution (see
        :py:class:`~utils.exceptions.TaskInterrupt` for more details).
        """
        self.__is_running = True
        try:
            self.execute()
        except TaskInterrupt:
            print_debug("Task " + self.__class__.__name__ + " stoped")
        except Exception as e:
            print_error(str(e) + "\n" + traceback.format_exc())
        finally:
            self.__is_running = False

    def is_running(self) -> bool:
        """
        Return whether the task is running or not.

        This method allows developers to know if the current Task is
        still running.
        It is recommended to use :py:meth:`join <threading.Thread.join>`
        method to wait until the task ends.
        """
        return self.__is_running

    def __get_id(self) -> int:
        """
        Return the thread identifier.

        :return: The thread ID.
        :rtype: int
        """
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def interrupt(self):
        """
        Interrupt the current Task.

        This method throws a :py:class:`~utils.exceptions.TaskInterrupt`
        into the current Task to stop it.
        """
        thread_id = self.__get_id()
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(TaskInterrupt))
        print_debug("Signal interruption sent to "
                    + self.__class__.__name__)

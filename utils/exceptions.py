# -*- coding: utf-8 -*-

class ApiToMutchInstantiationException(Exception):
    """
    This exception is derived from Exception.
    It is Raised when more than one API is instantiated.
    """

    def __init__(self):
        super().__init__()

class PreviousException(Exception):
    """
    This exception is derived from Exception.
    It is Raised when a :py:data:`~signal.SIGINT` is detected by the
    :py:func:`~signal.signal` function.
    """
    
    def __init__(self):
        super().__init__()

class TaskInterrupt(Exception):
    """
    This exception is derived from Exception.
    It is thrown into a specific thread when a PreviousException has
    been raised. It allows the program to shutdown all running threads.
    """

    def __init__(self):
        super().__init__()

class ToolGetProfileDuringExecutionException(Exception):
    """
    This exception is derived from Exception.
    It is raised when an OPSE tool is ask to return profiles while it is
    still running.
    """

    def __init__(self):
        super().__init__()

class ToolMissDataInputException(Exception):
    """
    This exception is derived from Exception.
    It is raised when an OPSE tool is ask to run without all required
    input data.
    """

    def __init__(self):
        super().__init__()
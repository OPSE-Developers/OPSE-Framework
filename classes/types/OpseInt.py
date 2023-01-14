# -*- coding: utf-8 -*-

from typing import Any

from classes.types.OpseType import OpseType


class OpseInt(OpseType):
    """
    Class that represents a "primitive" Integer type in OPSE.
    """

    def __init__(
        self,
        data_source: str,
        int_value: int,
        data_source_help_text: str = "",
        data_source_help_url: str = "",
        *args,
        **kwargs
    ):
        """Constructor of an OpseInt."""
        super().__init__(data_source, data_source_help_text, data_source_help_url)
        self.__int_value: int = int_value

    def __eq__(self, other: Any) -> bool:
        """Redefine equals method for the OpseInt type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseInt is equal to other, else
         False.
        :rtype: bool
        """
        if isinstance(other, int):
            return self.__int_value == other
        elif not isinstance(other, OpseType):
            return False
        else:
            return self.__int_value == int(other)

    def __le__(self, other: Any) -> bool:
        """Redefine lower or equal method for the OpseInt type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseInt is lower or equal to
         other, else False.
        :rtype: bool
        """
        if isinstance(other, int):
            return self.__int_value <= other
        elif not isinstance(other, OpseInt):
            return False
        else:
            return self.__int_value <= int(other)

    def __lt__(self, other: Any) -> bool:
        """Redefine lower than method for the OpseInt type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseInt is lower than other, else
         False.
        :rtype: bool
        """
        if isinstance(other, int):
            return self.__int_value < other
        elif not isinstance(other, OpseInt):
            return False
        else:
            return self.__int_value < int(other)

    def __ge__(self, other: Any) -> bool:
        """Redefine greater or equal method for the OpseInt type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseInt is greater or equal to
         other, else False.
        :rtype: bool
        """
        if isinstance(other, int):
            return self.__int_value >= other
        elif not isinstance(other, OpseInt):
            return False
        else:
            return self.__int_value >= int(other)

    def __gt__(self, other: Any) -> bool:
        """Redefine greater than method for the OpseInt type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseInt is greater than other,
         else False.
        :rtype: bool
        """
        if isinstance(other, int):
            return self.__int_value > other
        elif not isinstance(other, OpseInt):
            return False
        else:
            return self.__int_value > int(other)

    def __str__(self) -> str:
        """Redefine str method for the OpseInt type.

        :return: A string representation of the OpseInt.
        :rtype: str
        """
        return str(self.__int_value)
    
    def __int__(self) -> int:
        """Redefine int method for OpseInt type.

        :return: An integer of OpseInt value.
        :rtype: int
        """
        return int(self.__int_value)

    def __add__(self, other: Any):
        """Redefine add method for OpseInt type.

        :param other: The object to add.
        :type other: Any
        """
        self.__int_value += int(other)

    def __sub__(self, other: Any):
        """Redefine sub method for the OpseInt type.

        :param other: The object to substract.
        :type other: Any
        """
        self.__int_value -= int(other)

    def __hash__(self) -> int:
        """Return the identity of the OpseInt.

        :return: An identifier.
        :rtype: int
        """
        return id(self)



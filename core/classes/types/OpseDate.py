#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import date
from typing import Any

from classes.types.OpseType import OpseType


class OpseDate(OpseType):
    """
    Class that represents an OpseDate in OPSE context.
    """

    def __init__(
            self,
            date_value: date,
            data_source: str,
            data_source_help_text: str = "",
            data_source_help_url: str = ""
    ):
        """Constructor of an OpseDate."""
        super().__init__(data_source, data_source_help_text, data_source_help_url)
        self.date_value: date = date_value

    def __eq__(self, other: Any) -> bool:
        """Redefine equals method for the OpseDate type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseDate is equal to other, else
         False.
        :rtype: bool
        """
        if not isinstance(other, date):
            return self.date_value == other
        elif not isinstance(other, OpseType):
            return False
        else:
            return self.date_value == OpseDate(other).date_value

    def __le__(self, other: Any) -> bool:
        """Redefine lower or equal method for the OpseDate type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseDate is lower or equal to
         other, else False.
        :rtype: bool
        """
        if not isinstance(other, date):
            return self.date_value <= other
        elif not isinstance(other, OpseDate):
            return False
        else:
            return self.date_value <= OpseDate(other).date_value

    def __lt__(self, other: Any) -> bool:
        """Redefine lower than method for the OpseDate type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseDate is lower than other, else
         False.
        :rtype: bool
        """
        if not isinstance(other, date):
            return self.date_value < other
        elif not isinstance(other, OpseDate):
            return False
        else:
            return self.date_value < OpseDate(other).date_value

    def __ge__(self, other: Any) -> bool:
        """Redefine greater or equal method for the OpseDate type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseDate is greater or equal to
         other, else False.
        :rtype: bool
        """
        if not isinstance(other, date):
            return self.date_value >= other
        elif not isinstance(other, OpseDate):
            return False
        else:
            return self.date_value >= OpseDate(other).date_value

    def __gt__(self, other: Any) -> bool:
        """Redefine greater than method for the OpseDate type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseDate is greater than other,
         else False.
        :rtype: bool
        """

        if not isinstance(other, date):
            return self.date_value > other
        elif not isinstance(other, OpseDate):
            return False
        else:
            return self.date_value > OpseDate(other).date_value

    def __str__(self) -> str:
        """Redefine str method for the OpseDate type.

        :return: A string representation of the OpseDate.
        :rtype: str
        """
        return str(self.date_value)

    def __add__(self, other: Any):
        """Redefine add method for OpseDate type.

        :param other: The object to add.
        :type other: Any
        """
        self.date_value += date(other)

    def __sub__(self, other: Any):
        """Redefine sub method for the OpseDate type.

        :param other: The object to substract.
        :type other: Any
        """
        self.date_value -= date(other)

    def __hash__(self) -> int:
        """Return the identity of the OpseDate.

        :return: An identifier.
        :rtype: int
        """
        return id(self)


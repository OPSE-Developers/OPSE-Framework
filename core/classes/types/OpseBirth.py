#!/usr/bin/python3
# -*- coding: utf-8 -*-

from classes.types.OpseAddress import OpseAddress
from classes.types.OpseDate import OpseDate
from classes.types.OpseType import OpseType


class OpseBirth(OpseType):
    """
    Class that represents an OpseBirth in OPSE context.
    """

    def __init__(
        self,
        date: OpseDate,
        address: OpseAddress = None,
        data_source_help_text: str = "",
        data_source_help_url: str = ""
    ):
        """Constructor of an OpseBirth."""
        super().__init__(None, data_source_help_text, data_source_help_url)
        self.__date = date
        self.__address = address

    def get_date(self) -> OpseDate:
        """Getter of the birth date.

        :return: The birth date.
        :rtype: OpseDate
        """
        return self.__date

    def get_address(self) -> OpseAddress:
        """Getter of the birth address.

        :return: The birth address.
        :rtype: OpseAddress
        """
        return self.__address

    def set_date(self, date: OpseDate):
        """Setter of the birth date.

        :param date: The new birth date.
        :type date: OpseDate
        """
        self.__date = date

    def set_address(self, address: OpseAddress):
        """Setter of the birth address.

        :param address: The new birth address.
        :type address: OpseAddress
        """
        self.__address = address

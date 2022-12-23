#!/usr/bin/python3
# -*- coding: utf-8 -*-

from classes.types.OpseAddress import OpseAddress
from classes.types.OpseDate import OpseDate
from classes.types.OpseType import OpseType


class OpseDeath(OpseType):
    """
    Class that represents an OpseDeath in OPSE context.
    """

    def __init__(
        self,
        date: OpseDate,
        address: OpseAddress = None,
        data_source_help_text: str = "",
        data_source_help_url: str = ""
    ):
        """Constructor of an OpseDeath."""
        super().__init__(None, data_source_help_text, data_source_help_url)
        self.__date = date
        self.__address = address

    def get_date(self) -> OpseDate:
        """Getter of the death date.

        :return: The death date.
        :rtype: OpseDate
        """
        return self.__date

    def get_address(self) -> OpseAddress:
        """Getter of the death address.

        :return: The death address.
        :rtype: OpseAddress
        """
        return self.__address

    def set_date(self, date: OpseDate):
        """Setter of the death date.

        :param date: The new death date.
        :type date: OpseDate
        """
        """Setter of self.__date"""
        self.__date = date

    def set_address(self, address: OpseAddress):
        """Setter of the death address.

        :param address: The new death address.
        :type address: OpseAddress
        """
        self.__address = address

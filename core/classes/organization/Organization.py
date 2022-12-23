#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABC
from classes.types.OpseAddress import OpseAddress


class Organization(ABC):
    """Abstract class that represents an Organisation in OPSE context.
    """

    def __init__(
        self,
        name: str,
        address: OpseAddress = None
    ):
        self.__type = self.__class__.__name__.replace("Opse", "")
        self.__name: str = name
        self.__address: OpseAddress = address

    def get_name(self) -> str:
        """Getter of the organization name.

        :return: The name of the organization.
        :rtype: str
        """
        return self.__name

    def get_address(self) -> OpseAddress:
        """Getter of the organization address.

        :return: The address of the organization.
        :rtype: OpseAddress
        """
        return self.__address

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
from classes.types.OpseType import OpseType


class OpsePhoneNumber(OpseType):
    """
    Class that represents an OpsePhoneNumber in OPSE context.
    """

    def __init__(
        self,
        data_source: str,
        number: str,
        country: str,
        country_code: str,
        location: str = None,
        timezone: str = None,
        carrier: str = None,
        footprints: list = None,
        data_source_help_text: str = "",
        data_source_help_url: str = ""
    ):
        """Constructor of an OpsePhoneNumber."""
        super().__init__(data_source, data_source_help_text, data_source_help_url)
        self.__number: str = number
        self.__country: str = country
        self.__country_code: str = country_code
        self.__location: str = location
        self.__timezone: str = timezone
        self.__carrier: str = carrier
        self.__footprints: str = footprints

    def get_number(self) -> str:
        """Getter of the phone number.

        :return: The phone number.
        :rtype: str
        """
        return self.__number

    def get_country(self) -> str:
        """Getter of the phone number country.

        :return: The country of the phone number.
        :rtype: str
        """
        return self.__country

    def get_country_code(self) -> str:
        """Getter of the phone number country code.

        :return: The country code of the phone number.
        :rtype: str
        """
        return self.__country_code

    def get_national_number(self) -> str:
        """Return the national version of the phone number.

        :return: The national phone number.
        :rtype: str
        """
        return "0" + self.__number

    def get_international_number(self) -> str:
        """Return the international version of the phone number.

        :return: The international phone number.
        :rtype: str
        """
        return self.__country_code + self.__number

    def get_location(self) -> str:
        """Getter of the phone number location.

        :return: The location of the phone number.
        :rtype: str
        """
        return self.__location

    def get_timezone(self) -> str:
        """Getter of the phone number timezone.

        :return: The timezone of the phone number.
        :rtype: str
        """
        return self.__timezone

    def get_carrier(self) -> str:
        """Getter of the phone number carrier.

        :return: The carrier of the phone number.
        :rtype: str
        """
        return self.__carrier

    def get_footprints(self) -> str:
        """Getter of the phone number footprints.

        :return: The footprints of the phone number.
        :rtype: str
        """
        return self.__footprints

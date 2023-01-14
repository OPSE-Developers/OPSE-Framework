# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
from typing import Type, TypeVar

from classes.types.OpseType import OpseType


T = TypeVar('T', bound='OpseLocation')

class OpseLocation(OpseType):
    """
    Class that represents an OpseLocation in OPSE context.
    """

    loc = Nominatim(user_agent="GetLoc")

    def __init__(self,
        data_source: str,
        latitude: int,
        longitude: int,
        data_source_help_text: str = "",
        data_source_help_url: str = "",
        *args,
        **kwargs
    ):
        """Constructor of an OpseLocation."""
        super().__init__(data_source, data_source_help_text, data_source_help_url)
        self.__longitude: int = longitude
        self.__latitude: int = latitude

    def get_longitude(self) -> int:
        """Getter of the location longitude.

        :return: The longitude.
        :rtype: int
        """
        return self.__longitude

    def get_latitude(self) -> int:
        """Getter of the location latitude.

        :return: The latitude.
        :rtype: int
        """
        return self.__latitude

    def get_position(self) -> tuple:
        """Method that returns the position as a tuple, containing both
        latitude and longitude.

        :return: A tuple containing latitude and longitude.
        :rtype: tuple
        """
        return self.get_latitude(), self.get_longitude()

    @classmethod
    def get_location(cls: Type[T], adress_str: str) -> T:
        """Return an OpseLocation instance from an address string.

        :param adress_str: The address to locate.
        :type adress_str: str
        :return: The location of the address.
        :rtype: OpseLocation
        """
        get_loc = OpseLocation.loc.geocode(adress_str)
        return OpseLocation(get_loc.latitude, get_loc.longitude)

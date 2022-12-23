#!/usr/bin/python3
# -*- coding: utf-8 -*-

from classes.types.OpseType import OpseType


class OpseAddress(OpseType):
    """
    Class that represents an OpseAddress in OPSE context.
    """

    def __init__(
        self,
        data_source: str,
        number: int = None,
        street: str = None,
        state_code: int = None,
        city: str = None,
        country: str = None,
        data_source_help_text: str = "",
        data_source_help_url: str = ""
    ):
        """Constructor of an OpseAddress."""
        super().__init__(data_source, data_source_help_text, data_source_help_url)
        self.__number: int = number
        self.__street: str = street
        self.__state_code: int = state_code
        self.__city: str = city
        self.__country = country

        try:
            self.unpack_street()
        except TypeError as e:
            pass

        if isinstance(city, str):
            try:
                self.unpack_city()
            except TypeError as e:
                pass

    def unpack_street(self):
        """Split a full street address into street number and street
        name.

        :raises TypeError: If street is missing.
        """
        if self.__street is None:
            raise TypeError("Missing street argument")

        street_elems = self.__street.split(' ')

        numbers = []
        for elem in street_elems:
            try:
                numbers.append(int(elem))
                street_elems.remove(elem)
            except ValueError:
                pass

        if len(numbers) > 0:
            self.__number = numbers[0]
            self.__street = ' '.join(street_elems)

    def unpack_city(self):
        """Split a full city address into state code and city name.

        :raises TypeError: If city is missing.
        """
        if self.__city is None:
            raise TypeError("Missing city argument")

        city_elems = self.__city.split(' ')

        numbers = []
        for elem in city_elems:
            try:
                numbers.append(int(elem))
                city_elems.remove(elem)
            except ValueError:
                pass

        if len(numbers) > 0:
            self.__state_code = numbers[0]
            self.__city = ' '.join(city_elems)

    def get_number(self) -> int:
        """Getter of the address's number.

        :return: The number of the address.
        :rtype: int
        """
        return self.__number

    def get_street(self) -> str:
        """Getter of the address's street name.

        :return: The street of the address.
        :rtype: str
        """
        return self.__street

    def get_state_code(self) -> int:
        """Getter of the address's state code.

        :return: The state code of the address.
        :rtype: int
        """
        return self.__state_code

    def get_city(self) -> str:
        """Getter of the address's city.

        :return: The city of the address.
        :rtype: str
        """
        return self.__city

    def get_country(self) -> str:
        """Getter of the address's country.

        :return: The country of the address.
        :rtype: str
        """
        return self.__country

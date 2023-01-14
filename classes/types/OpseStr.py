# -*- coding: utf-8 -*-

from classes.types.OpseType import OpseType


class OpseStr(OpseType):
    """
    Class that represents a "primitive" String type in OPSE.
    """

    def __init__(
        self,
        data_source: str,
        str_value: str,
        data_source_help_text: str = "",
        data_source_help_url: str = "",
        *args,
        **kwargs
    ):
        """Constructor of an OpseStr."""
        super().__init__(data_source, data_source_help_text, data_source_help_url)
        self.str_value: str = str_value

    def __eq__(self, other) -> bool:
        """Redefine equals method for the OpseStr type.

        :param other: The object to compare.
        :type other: Any
        :return: True if the current OpseStr is equal to other, else
         False.
        :rtype: bool
        """
        if isinstance(other, str):
            return self.str_value == other
        elif not isinstance(other, OpseStr):
            return False
        else:
            return self.str_value == str(other)

    def __len__(self) -> int:
        """Redefine len method for the OpseStr type.

        :return: The length of the OpseStr value.
        :rtype: int
        """
        return len(self.str_value)

    def __str__(self) -> str:
        """Redefine str method for the OpseStr type.

        :return: A string representation of the OpseStr.
        :rtype: str
        """
        return str(self.str_value)

    def __add__(self, other):
        """Redefine add method for OpseStr type.

        :param other: The object to add.
        :type other: Any
        """
        self.str_value += str(other)

    def __hash__(self):
        """Return the identity of the OpseStr.

        :return: An identifier.
        :rtype: int
        """
        return id(self)


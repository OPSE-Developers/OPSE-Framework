# -*- coding: utf-8 -*-

class OpseType():
    """
    Class that represents a "primitive" type in OPSE.
    """

    def __init__(
        self,
        data_source: str,
        data_source_help_text: str = "",
        data_source_help_url: str = "",
        *args,
        **kwargs
    ):
        """Constructor of an OpseType."""
        self.__type = self.__class__.__name__.replace("Opse", "")
        self.__data_source = data_source
        self.__data_source_help_text = data_source_help_text
        self.__data_source_help_url = data_source_help_url

    def get_data_source(self) -> str:
        """Getter of the data source.

        The source can be a URL or just the name of the source.
        It allows the user to retrieve the data.

        :return: The data source.
        :rtype: str
        """
        return self.__data_source

    def get_data_source_help_text(self) -> str:
        """Getter of the data source help text.

        :return: The help text.
        :rtype: str
        """
        return self.__data_source_help_text

    def get_data_source_help_url(self) -> str:
        """Getter of the data source help URL.

        :return: The help URL.
        :rtype: str
        """
        return self.__data_source_help_url

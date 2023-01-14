# -*- coding: utf-8 -*-

from abc import ABC


class Account(ABC):
    """Abstract class that represents an Account in OPSE context.
    """

    def __init__(
        self,
        username: str,
        url: str = None,
        lst_messages: list = None,
        *args,
        **kwargs
    ):
        self.__type = self.__class__.__name__.replace("Opse", "")
        self.__username: str = username
        self.__url: str = url
        self.__lst_messages: list = lst_messages

    def get_username(self) -> str:
        """Getter of the account username.

        :return: The username of the account.
        :rtype: str
        """
        return self.__username

    def get_url(self) -> str:
        """Getter of the account URL.

        :return: The URL of the account.
        :rtype: str
        """
        return self.__url

    def get_lst_messages(self) -> list:
        """Getter of the account messages.

        :return: A list of messages of the account.
        :rtype: list
        """
        return self.__lst_messages

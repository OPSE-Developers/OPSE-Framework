# -*- coding: utf-8 -*-

from abc import ABC


class Message(ABC):
    """Abstract class that represents a Message in OPSE context."""

    def __init__(
        self,
        content: str,
        author: str = None,
        *args,
        **kwargs
    ):
        self.__type = self.__class__.__name__.replace("Opse", "")
        self.__content: str = content
        self.__author: str = author

    def get_content(self) -> str:
        """Getter of the message content.

        :return: The content of the message.
        :rtype: str
        """
        return self.__content

    def get_author(self) -> str:
        """Getter of the message author.

        :return: The author of the message.
        :rtype: str
        """
        return self.__author

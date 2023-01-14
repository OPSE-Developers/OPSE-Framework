# -*- coding: utf-8 -*-

from classes.account.Account import Account


class WebsiteAccount(Account):
    """
    Class that represents a WebsiteAccount in OPSE context.
    """

    def __init__(
        self,
        website_name: str,
        website_url: str,
        login: str = None,
        username: str = None,
        recovery_email: str = None,
        phone_number: str = None,
        *args,
        **kwargs
    ):
        """Constructor of an OPSE WebsiteAccount."""
        super().__init__(username, website_url)
        self.__type = self.__class__.__name__.replace("Opse", "")
        self.__login: str = login
        self.__website_name: str = website_name
        self.__recovery_email: str = recovery_email
        self.__phone_number: str = phone_number

    def get_login(self) -> str:
        """Getter of the website account login.

        :return: The login of the account.
        :rtype: str
        """
        return self.__login

    def get_website_name(self) -> str:
        """Getter of the website name.

        :return: The name of the website.
        :rtype: str
        """
        return self.__website_name

    def get_recovery_email(self) -> str:
        """Getter of the website account recovery email.

        :return: The recovery email of the account.
        :rtype: str
        """
        return self.__recovery_email

    def get_phone_number(self) -> str:
        """Getter of the website account phone number.

        :return: The phone number of the account.
        :rtype: str
        """
        return self.__phone_number

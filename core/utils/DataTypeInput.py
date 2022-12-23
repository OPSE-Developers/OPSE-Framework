# -*- coding: utf-8 -*-
class DataTypeInput:
    """
    Class that defines the possible input data for a tool.
    It allows developers to define what input data will be useful for
    their tools.
    Also it normalizes OPSE as developers use these variables and not
    hard-coded strings.
    """

    FIRSTNAME = "FIRSTNAME"
    LASTNAME = "LASTNAME"
    MIDDLENAME = "MIDDLENAME"
    USERNAME = "USERNAME"
    GENDER = "GENDER"
    BIRTHDATE = "BIRTHDATE"
    DEATHDATE = "DEATHDATE"
    AGE = "AGE"
    PHONE_NUMBER = "PHONE_NUMBER"
    EMAIL = "EMAIL"
    ACCOUNT = "ACCOUNT"
    IP = "IP"
    ADRESSE = "ADRESSE"
    LOCATION = "LOCATION"
    ORGANIZATION = "ORGANIZATION"

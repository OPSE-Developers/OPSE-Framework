# -*- coding: utf-8 -*-

import copy
import uuid

from datetime import date
from typing import Type, TypeVar

from classes.account.Account import Account
from classes.types.OpseAddress import OpseAddress
from classes.types.OpseBirth import OpseBirth
from classes.types.OpseDeath import OpseDeath
from classes.types.OpseLocation import OpseLocation
from classes.organization.Organization import Organization
from classes.types.OpseStr import OpseStr
from classes.types.OpseDate import OpseDate
from classes.types.OpseInt import OpseInt
from utils.config.Config import Config
from utils.datatypes import DataTypeOutput


T = TypeVar('T', bound='Profile')

class Profile:
    """
    Class that represents a Profile in OPSE context.
    """

    __lst_profile: list = []

    def __init__(
            self,
            firstname: OpseStr = None,
            lastname: OpseStr = None,
            lst_middlenames: list[OpseStr] = [],
            gender: OpseStr = None,
            birthdate: OpseDate = None,
            deathdate: OpseDate = None,
            age: OpseInt = None,
            lst_phone_numbers: list[OpseStr] = [],
            lst_usernames: list[OpseStr] = [],
            lst_emails: list[OpseStr] = [],
            lst_accounts: list[Account] = [],
            lst_pictures: list[OpseStr] = [],
            lst_ips: list[OpseStr] = [],
            lst_addresses: list[OpseAddress] = [],
            lst_locations: list[OpseLocation] = [],
            lst_organizations: list[Organization] = [],
            political_orientation: OpseStr = None,
            *args,
            **kwargs
    ):
        """Constructor of an OPSE Profile."""
        self.__id = str(uuid.uuid4().hex)

        if Config.get()["config"]["api"]["unsafe"]:
            # If we are in unsafe mode, we generate predictible ID.
            # This is supposed to help devs to test the API.
            # /!\ Unsafe mode should never be used in production.
            self.__id = str(len(Profile.get_lst_profile()))

        self.__firstname: OpseStr = firstname
        self.__lastname: OpseStr = lastname
        self.__lst_middlenames: list = lst_middlenames
        self.__lst_usernames: list = lst_usernames
        self.__gender: OpseStr = gender
        self.__birth: OpseBirth = OpseBirth(birthdate) if birthdate is not None else None
        self.__death: OpseDeath = OpseDeath(deathdate) if deathdate is not None else None
        self.__age: OpseStr = age
        self.__lst_phone_numbers: list = lst_phone_numbers
        self.__lst_emails: list = lst_emails
        self.__lst_accounts: list = lst_accounts
        self.__lst_pictures: list = lst_pictures
        self.__lst_ips: list = lst_ips
        self.__lst_addresses = lst_addresses
        self.__lst_locations: list = lst_locations
        self.__lst_organizations: list = lst_organizations
        self.__political_orientation: OpseStr = political_orientation
        Profile.get_lst_profile().append(self)

    def get_id(self) -> str:
        """Getter of the profile identifier."""
        return self.__id

    @classmethod
    def get_lst_profile(cls):
        """Return the list of existing profiles."""
        return cls.__lst_profile

    @classmethod
    def get_profile(cls: Type[T], profile_id: str) -> T:
        """Return a Profile from an identifier.

        If the identifier given to the function is not linked to a
        Profile, then the function will return None.

        :param profile_id: The profile's identifier.
        :type profile_id: str
        :return: The desire profile.
        :rtype: Profile
        """
        for profile in cls.get_lst_profile():
            if profile.get_id() == profile_id:
                return profile
        return None

    def get_lst_data_type(self) -> list[str]:
        """Method that returns the list of data types used in the
        profile.

        :return: A list of data types.
        :rtype: list[str]
        """
        lst_data_type = []
        if self.get_firstname() is not None:
            lst_data_type.append(DataTypeOutput.FIRSTNAME)

        if self.get_lastname() is not None:
            lst_data_type.append(DataTypeOutput.LASTNAME)

        if len(self.get_lst_middlenames()) > 0:
            lst_data_type.append(DataTypeOutput.MIDDLENAME)

        if len(self.get_lst_usernames()) > 0:
            lst_data_type.append(DataTypeOutput.USERNAME)

        if self.get_gender() is not None:
            lst_data_type.append(DataTypeOutput.GENDER)

        if self.get_birthdate() is not None:
            lst_data_type.append(DataTypeOutput.BIRTHDATE)

        if self.get_deathdate() is not None:
            lst_data_type.append(DataTypeOutput.DEATHDATE)

        if self.get_age() is not None:
            lst_data_type.append(DataTypeOutput.AGE)

        if len(self.get_lst_phone_numbers()) > 0:
            lst_data_type.append(DataTypeOutput.PHONE_NUMBER)

        if len(self.get_lst_emails()) > 0:
            lst_data_type.append(DataTypeOutput.EMAIL)

        if len(self.get_lst_accounts()) > 0:
            lst_data_type.append(DataTypeOutput.ACCOUNT)

        if len(self.get_lst_pictures()) > 0:
            lst_data_type.append(DataTypeOutput.PICTURE)

        if len(self.get_lst_ips()) > 0:
            lst_data_type.append(DataTypeOutput.IP)

        if len(self.get_lst_addresses()) > 0:
            lst_data_type.append(DataTypeOutput.ADDRESS)

        if len(self.get_lst_locations()) > 0:
            lst_data_type.append(DataTypeOutput.LOCATION)

        if len(self.get_lst_organizations()) > 0:
            lst_data_type.append(DataTypeOutput.ORGANIZATION)

        if self.get_political_orientation() is not None:
            lst_data_type.append(DataTypeOutput.POLITICAL_ORIENTATION)

        return lst_data_type

    def get_firstname(self) -> OpseStr:
        """Getter of the profile first name.

        :return: The first name.
        :rtype: OpseStr
        """
        return self.__firstname

    def get_lastname(self) -> OpseStr:
        """Getter of the profile last name.

        :return: The last name.
        :rtype: OpseStr
        """
        return self.__lastname

    def get_lst_middlenames(self) -> list[OpseStr]:
        """Getter of the profile middle names.

        :return: A list of the profile middle names.
        :rtype: list[OpseStr]
        """
        return self.__lst_middlenames

    def get_lst_usernames(self) -> list[OpseStr]:
        """Getter of the profile usernames.

        :return: A list of the profile usernames.
        :rtype: list[OpseStr]
        """
        return self.__lst_usernames

    def get_gender(self) -> OpseStr:
        """Getter of the profile gender.

        :return: The profile gender.
        :rtype: OpseStr
        """
        return self.__gender

    def get_birthdate(self) -> OpseDate:
        """Getter of the profile birth date.

        :return: The profile birth date.
        :rtype: OpseDate
        """
        return self.__birth.get_date() if self.__birth is not None else None

    def get_deathdate(self) -> OpseDate:
        """Getter of the profile death date.

        :return: The profile death date.
        :rtype: OpseDate
        """
        return self.__death.get_date()if self.__death is not None else None

    def get_birth_address(self) -> OpseAddress:
        """Getter of the profile birth address.

        :return: The profile birth address.
        :rtype: OpseAddress
        """
        return self.__birth.get_address()

    def get_death_address(self) -> OpseAddress:
        """Getter of the profile death address.

        :return: The profile death address.
        :rtype: OpseAddress
        """
        return self.__death.get_address()

    def get_age(self) -> OpseInt:
        """Getter of the profile age.

        :return: The profile age.
        :rtype: OpseInt
        """
        return self.__age

    def get_lst_phone_numbers(self) -> list[OpseStr]:
        """Getter of the profile phone numbers.

        :return: A list of the profile phone numbers.
        :rtype: list[OpseStr]
        """
        return self.__lst_phone_numbers

    def get_lst_emails(self) -> list[OpseStr]:
        """Getter of the profile emails.

        :return: A list of the profile emails.
        :rtype: list[OpseStr]
        """
        return self.__lst_emails

    def get_lst_accounts(self) -> list[Account]:
        """Getter of the profile accounts.

        :return: A list of the profile accounts.
        :rtype: list[Account]
        """
        return self.__lst_accounts

    def get_lst_pictures(self) -> list[OpseStr]:
        """Getter of the profile pictures.

        :return: A list of the profile pictures.
        :rtype: list[OpseStr]
        """
        return self.__lst_pictures

    def get_lst_ips(self) -> list[OpseStr]:
        """Getter of the profile IP addresses.

        :return: A list of the profile IP addresses.
        :rtype: list[OpseStr]
        """
        return self.__lst_ips

    def get_lst_addresses(self) -> list[OpseAddress]:
        """Getter of the profile physical addresses.

        :return: A list of the profile addresses.
        :rtype: list[OpseStr]
        """
        return self.__lst_addresses

    def get_lst_locations(self) -> list[OpseLocation]:
        """Getter of the profile locations.

        :return: A list of the profile locations.
        :rtype: list[OpseStr]
        """
        return self.__lst_locations

    def get_lst_organizations(self) -> list[Organization]:
        """Getter of the profile organizations.

        :return: A list of the profile organizations.
        :rtype: list[OpseStr]
        """
        return self.__lst_organizations

    def get_political_orientation(self) -> OpseStr:
        """Getter of the profile political orientation.

        :return: The profile political orientation.
        :rtype: OpseStr
        """        
        return self.__political_orientation

    def set_firstname(self, firstname: OpseStr):
        """Setter of the profile first name.

        :param firstname: The new first name.
        :type firstname: OpseStr
        """
        self.__firstname = firstname

    def set_lastname(self, lastname: OpseStr):
        """Setter of the profile last name.

        :param lastname: The new last name.
        :type lastname: OpseStr
        """
        self.__lastname = lastname

    def set_lst_middlenames(self, lst_middlenames: list[OpseStr]):
        """Setter of self.__lst_second_name"""
        self.__lst_middlenames.extend(lst_middlenames)

    def set_lst_usernames(self, lst_usernames: list[OpseStr]):
        """Setter of self.__lst_usernames"""
        self.__lst_usernames.extend(lst_usernames)

    def set_gender(self, gender: OpseStr):
        """Setter of the profile gender.

        :param gender: The new gender.
        :type gender: OpseStr
        """
        self.__gender = gender

    def set_birthdate(self, birthdate: OpseDate):
        """Setter of the profile birth date.

        :param birthdate: The new birth date.
        :type birthdate: OpseDate
        """
        if self.__birth is None:
            self.__birth = OpseBirth(birthdate)
        else:
            self.__birth.set_date(birthdate)

    def set_deathdate(self, deathdate: OpseDate):
        """Setter of the profile death date.

        :param deathdate: The new death date.
        :type deathdate: OpseDate
        """
        if self.__death is None:
            self.__death = OpseDeath(deathdate)
        else:
            self.__death.set_date(deathdate)

    def set_birth_address(self, birth_address: OpseAddress):
        """Setter of the profile birth address.

        :param birth_address: The new birth address.
        :type birth_address: OpseAddress
        """
        self.__birth.set_address(birth_address)

    def set_death_address(self, death_address: OpseAddress):
        """Setter of the profile death address.

        :param death_address: The new death address.
        :type death_address: OpseAddress
        """
        """Setter of self.__death.address"""
        self.__death.set_address(death_address)

    def set_age(self, age: OpseInt):
        """Setter of the profile age.

        :param age: The new age.
        :type age: OpseInt
        """
        """Setter of self.__age"""
        self.__age = age

    def calc_age(self):
        """Method that calculates the age between the birth and the
        death dates. Set the profile age with the result.

        :raises TypeError: If birth date is missing.
        """
        birthdate = self.__birth.get_date()
        deathdate = self.__death.get_date()
        if birthdate is not None:
            if deathdate is not None:
                self.__age = deathdate.year - birthdate.year - ((deathdate.month, deathdate.day) < (birthdate.month, birthdate.day))
            else:
                today = date.today()
                self.__age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        else:
            raise TypeError("Missing birthdate argument")

    def set_lst_phone_numbers(self, lst_phone_numbers: list[OpseStr]):
        """Setter of the profile phone numbers.

        This method extends the current list of phone numbers. Use the
        getter to do other actions on the list.

        :param lst_phone_numbers: The new phone numbers.
        :type lst_phone_numbers: list[OpseStr]
        """
        """Setter of self.__lst_phone_numbers"""
        self.__lst_phone_numbers.extend(lst_phone_numbers)

    def set_lst_emails(self, lst_emails: list[OpseStr]):
        """Setter of the profile emails.

        This method extends the current list of emails. Use the
        getter to do other actions on the list.

        :param lst_emails: The new 
        :type lst_emails: list[OpseStr]
        """
        """Setter of self.__lst_emails"""
        self.__lst_emails.extend(lst_emails)

    def set_lst_accounts(self, lst_accounts: list[Account]):
        """Setter of the profile accounts.

        This method extends the current list of accounts. Use the
        getter to do other actions on the list.

        :param lst_accounts: The new accounts.
        :type lst_accounts: list[Account]
        """
        """Setter of self.__lst_accounts"""
        self.__lst_accounts.extend(lst_accounts)

    def set_lst_pictures(self, lst_pictures: list[OpseStr]):
        """Setter of the profile pictures.

        This method extends the current list of pictures. Use the
        getter to do other actions on the list.

        :param lst_pictures: The new pictures.
        :type lst_pictures: list[OpseStr]
        """
        """Setter of self.__lst_pictures"""
        self.__lst_pictures.extend(lst_pictures)

    def set_lst_ips(self, lst_ips: list[OpseStr]):
        """Setter of the profile IP addresses.

        This method extends the current list of IP addresses. Use the
        getter to do other actions on the list.

        :param lst_ips: The new IP addresses.
        :type lst_ips: list[OpseStr]
        """
        """Setter of self.__lst_ips"""
        self.__lst_ips.extend(lst_ips)

    def set_lst_addresses(self, lst_addresses: list[OpseAddress]):
        """Setter of the profile physical addresses.

        This method extends the current list of addresses. Use the
        getter to do other actions on the list.

        :param lst_addresses: The new addresses.
        :type lst_addresses: list[OpseAddress]
        """
        """Setter of self.__lst_addresses"""
        self.__lst_addresses.extend(lst_addresses)

    def set_lst_locations(self, lst_locations: list[OpseLocation]):
        """Setter of the profile locations.

        This method extends the current list of locations. Use the
        getter to do other actions on the list.

        :param lst_locations: The new locations.
        :type lst_locations: list[OpseLocation]
        """
        """Setter of self.__lst_locations"""
        self.__lst_locations.extend(lst_locations)

    def set_lst_organizations(self, lst_organizations: list[Organization]):
        """Setter of the profile organizations.

        This method extends the current list of organizations. Use the
        getter to do other actions on the list.

        :param lst_organizations: The new organizations.
        :type lst_organizations: list[Organization]
        """
        """Setter of self.__lst_organizations"""
        self.__lst_organizations.extend(lst_organizations)

    def set_political_orientation(self, political_orientation: OpseStr):
        """Setter of the profile political orientation.

        :param political_orientation: The new political orientation.
        :type political_orientation: OpseStr
        """
        """Setter of self.__political_orientation"""
        self.__political_orientation = political_orientation

    def get_summary(self) -> str:
        """Method that generates a string summary of the current
        profile.

        :return: A short string representation of the profile.
        :rtype: str
        """
        summary = ""
        dict_type_name = {}

        lst_data_type = []
        if self.get_firstname() is not None:
            summary += str(self.get_firstname())

        if len(self.get_lst_middlenames()) > 0:
            for middlename in self.get_lst_middlenames():
                summary += " " + str(middlename)

        if self.get_lastname() is not None:
            summary += " " + str(self.get_lastname()).upper()

        if self.get_age() is not None:
            summary += ", " + str(self.get_age()) + " old"

        if self.get_gender() is not None:
            summary += " (" + str(self.get_gender())+")"

        if len(self.get_lst_usernames()) > 0:
            summary += ", " + str(len(self.get_lst_usernames())) + " username"

        if self.get_birthdate() is not None:
            summary += ", born " + str(self.get_birthdate())

        if self.get_deathdate() is not None:
            summary += ", death " + str(self.get_deathdate())

        if len(self.get_lst_emails()) > 0:
            summary += ", " + str(len(self.get_lst_emails())) + " emails"

        if len(self.get_lst_addresses()) > 0:
            summary += ", " + str(len(self.get_lst_addresses())) + " address"

        if len(self.get_lst_phone_numbers()) > 0:
            summary += ", "+str(len(self.get_lst_phone_numbers())) + " phone number"

        if len(self.get_lst_ips()) > 0:
            summary += ", "+str(len(self.get_lst_ips())) + " IP"

        if len(self.get_lst_locations()) > 0:
            summary += ", "+str(len(self.get_lst_locations())) + " location"

        dict_type_name = {}
        if len(self.get_lst_organizations()) > 0:

            for organisation in self.get_lst_organizations():
                type_name = str(type(organisation).__name__).replace("Opse", "").replace("Organisation", "")
                if type_name not in dict_type_name:
                    dict_type_name[type_name] = 0
            dict_type_name[type_name] += 1

        if len(self.get_lst_accounts()) > 0:

            for account in self.get_lst_accounts():
                type_name = str(type(account).__name__).replace("Opse", "").replace("Account", "")
                if type_name not in dict_type_name:
                    dict_type_name[type_name] = 0
                dict_type_name[type_name] += 1

        for key in dict_type_name.keys():
            if summary == "":
                summary = str(self.get_id())
            summary += ", " + str(dict_type_name[key]) + " " + str(key)

        return summary

    def clone(self) -> T:
        """Return a fully independant clone of the current Profile.

        :return: A deepcopy of the profile.
        :rtype: Profile
        """
        new_profile = copy.deepcopy(self)
        new_profile.__id = str(uuid.uuid4().hex)
        Profile.get_lst_profile().append(new_profile)
        return new_profile

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime

from classes.Profile import Profile
from classes.Research import Research

from utils.utils import is_valid_date
from utils.utils import print_debug
from utils.utils import print_error

from classes.types.OpseBirth import OpseBirth
from classes.types.OpseInt import OpseInt
from classes.types.OpseStr import OpseStr

from classes.types.OpseAddress import OpseAddress


def make_research(
    target_firstname: str,
    target_middlename:list[str],
    target_lastname: str,
    target_gender: str,
    target_birthdate: str,
    target_age: str,
    target_address: list[str],
    target_phone: list[str],
    target_email: list[str],
    target_username: list[str],
    start_research: bool = True,
) -> Research:
    """Function that makes a research from target's information.

    :param target_firstname: First name of the target.
    :type target_firstname: str
    :param target_middlename: Middle name of the target.
    :type target_middlename: list[str]
    :param target_lastname: Last name of the target.
    :type target_lastname: str
    :param target_gender: Gender of the target.
    :type target_gender: str
    :param target_birthdate: Birth date of the target.
    :type target_birthdate: str
    :param target_age: Age of the target.
    :type target_age: str
    :param target_address: Address of the target.
    :type target_address: list[str]
    :param target_phone: Phone number of the target.
    :type target_phone: list[str]
    :param target_email: Email  of the target.
    :type target_email: list[str]
    :param target_username: Username of the target.
    :type target_username: list[str]
    :param start_research: Setting to start the research, defaults to
     True.
    :type start_research: bool, optional
    :return: The research containing profiles.
    :rtype: Research
    """
    user_input = "USER INPUT"

    # Check user input
    if target_birthdate is not None:
        if not is_valid_date(target_birthdate):
            print_error(" OpseBirthday is not a valid date, please use format dd/mm/YYYY, this date will not be used")
            target_birthdate = None
        else:
            target_birthdate = datetime.strptime(target_birthdate, "%d/%m/%Y")

    if target_age is not None:
        try:
            target_age = int(target_age)
        except ValueError:
            print_error(" Old is not a valid integer, this old will not be used")
            target_age = None

    if target_address is not None:

        tmp_lst = []
        if isinstance(target_address,list):
            for tmp_address in target_address:
                if isinstance(tmp_address, dict):

                    try:
                        tmp_lst.append(OpseAddress(user_input,
                                                     int(tmp_address["number"]),
                                                     tmp_address["street"],
                                                     int(tmp_address["state_code"]),
                                                     tmp_address["city"],
                                                     tmp_address["country"]
                                                     )
                                       )
                    except ValueError:
                        print_error("Not able to use given address. Value error raised.")
                else:
                    tmp_lst.append(OpseAddress(user_input, street=tmp_address))
        else:
            print_error("No address add because we need list of adresses")

        target_address = tmp_lst
    else:
        target_address = []

    if target_phone is not None:
        tmp_lst = []
        for phone in target_phone:
            tmp_lst.append(OpseStr(user_input, phone))

        target_phone = tmp_lst
    else:
        target_phone = []

    if target_email is not None:
        tmp_lst = []
        for email in target_email:
            tmp_lst.append(OpseStr(user_input, email))

        target_email = tmp_lst
    else:
        target_email = []

    if target_middlename is not None:
        tmp_lst = []
        for middlename in target_middlename:
            tmp_lst.append(OpseStr(user_input, middlename))

        target_middlename = tmp_lst
    else:
        target_middlename = []

    if target_username is not None:
        tmp_lst = []
        for username in target_username:
            tmp_lst.append(OpseStr(user_input, username))

        target_username = target_username
    else:
        target_username = []

    default_profile = Profile(
        firstname=OpseStr(user_input, target_firstname) if target_firstname is not None else None,
        lst_middlenames=target_middlename,
        lastname=OpseStr(user_input, target_lastname) if target_lastname is not None else None,
        gender=OpseStr(user_input, target_gender) if target_gender is not None else None,
        birthdate=OpseBirth(user_input, target_birthdate) if target_birthdate is not None else None,
        age=OpseInt(user_input, target_age) if target_age is not None else None,
        lst_addresses=target_address,
        lst_phone_numbers=target_phone,
        lst_emails=target_email,
        lst_usernames=target_username
    )

    print_debug("New default profile created" + " with " + str(default_profile.get_lst_data_type()) + ":\n\t" + str(
        default_profile))

    research = Research(default_profile)

    if start_research:
        research.enrich_profiles()

    return research

# -*- coding: utf-8 -*-

import gc
import uuid

from datetime import datetime
from typing import Type, TypeVar

from classes.Profile import Profile
from classes.types.OpseAddress import OpseAddress
from classes.types.OpseBirth import OpseBirth
from classes.types.OpseInt import OpseInt
from classes.types.OpseStr import OpseStr
from tools.Tool import Tool
from utils.config.Config import Config
from utils.exceptions import ToolGetProfileDuringExecutionException, ToolMissDataInputException
from utils.stdout import print_debug, print_error, print_sucess, print_warning
from utils.utils import is_valid_date, remove_plural

T = TypeVar('T', bound='Research')

class Research:
    """
    Class that represents a Reseach in OPSE context.
    """
    __lst_research: list = []

    def __init__(self, default_profile: Profile):
        """
        Constructor of a Research.

        To make a Research, we assume we have a default profile which
        contains information given by the user.
        """
        self.__id = str(uuid.uuid4().hex)

        if Config.get()["config"]["api"]["unsafe"]:
            # If we are in unsafe mode, we generate predictible ID.
            # This is supposed to help devs to test the API.
            # /!\ Unsafe mode should never be used in production.
            self.__id = str(len(Research.get_lst_research()))

        self.__lst_profile: list[Profile] = [default_profile]
        # self.__profiles_visibility = self.__init_profile_visibility(default_profile)

        Research.get_lst_research().append(self)

    def get_lst_profile(self) -> list[Profile]:
        """Getter of the research's list of profiles.

        :return: The list of profiles found.
        :rtype: list[Profile]
        """
        return self.__lst_profile

    def get_id(self) -> str:
        """Getter of the research identifier.

        :return: The research identifier.
        :rtype: str
        """
        return self.__id

    def get_linked_id(self) -> dict:
        """Method that returns all linked identifiers to a this
        Research.
        
        It is used to manage permissions.

        :return: A dictionary containing the research identifier and a
         list of all the profile's identifiers.
        :rtype: dict
        """
        linked_id = {
            "research": self.get_id(),
            "profile": []
        }

        for profile in self.get_lst_profile():
            linked_id["profile"].append(profile.get_id())
        
        return linked_id

    @classmethod
    def get_lst_research(cls) -> list:
        """Return the list of existing researches.

        :return: A list of all researches.
        :rtype: list
        """
        return cls.__lst_research

    @classmethod
    def get_research(cls: Type[T], research_id: str) -> T:
        """Return a Research from an identifier.

        If the identifier given to the function is not linked to a
        Research, then the function will return None.

        :param research_id: The research's identifier.
        :type research_id: str
        :return: The desire research.
        :rtype: Research
        """
        for research in cls.get_lst_research():
            if str(research.get_id()) == str(research_id):
                return research
        return None

    def enrich_profiles(self):
        """Method that enriches the profile list depending on data
        available in the current profile(s).
        
        The objective is to get more profiles from an existing profile.
        """
        # 1) Define wich tool could be used for each profile
        print_debug("\nStarting profile enrichment...")
        map_tool_for_profile: dict[Profile, list[Tool]] = {}
        active_tools: list[Tool] = Tool.get_lst_active_tools() # List of tools. Each tool should be add in here.

        for profile in self.get_lst_profile():

            # Depending on each DataType input of Profile and Tool, we add or not Profile in map
            for data_type_input in profile.get_lst_data_type():

                for tool in active_tools:
                    if data_type_input in tool.get_lst_input_data_types():
                        print_debug("--> " + data_type_input + " from " + str(
                            hex(id(profile))) + " could be use by " + tool.get_name() + ".")
                        Research.__add_profile_in_map_tool(map_tool_for_profile, profile, tool())

        # 2) Launch each tool
        print_debug("\nLaunching each tool")
        lst_process: list = []
        for profile in map_tool_for_profile.keys():

            for tool in map_tool_for_profile[profile]:
                print_debug("--> " + tool.get_name() + " launched for " + str(hex(id(profile))))
                try:
                    tool.launch(profile)
                    lst_process.append(tool)
                except ToolMissDataInputException:
                    print_debug("--> " + tool.get_name() + " canceled for " + str(
                        hex(id(profile))) + " because some needed values are not present.")

        # 3) Wait the end of each tool process
        for tool_process in lst_process:
            tool_process.join()

        # 4) Add new profile in Research profile list
        for profile in map_tool_for_profile.keys():
            # Add new profile in Research profile list
            for tool in map_tool_for_profile[profile]:
                nb_profile_added = 0
                try:
                    for new_profile in tool.get_profiles():
                        self.__lst_profile.append(new_profile)
                        nb_profile_added += 1
                except ToolGetProfileDuringExecutionException:
                    # This exception should nether exist
                    print_error(" Could not get profile when profile tool is already running", on_debug_only=True)
                    print_debug(
                        "Unable to add profile because process(" + tool.get_name() + ") is already running")

            # TODO
            # TRY TO MERGE THIS NEW PROFILE FROM SAME TOOL AND SAME PROFILE

            # Remove original profile if new profile was find
            if nb_profile_added > 0:
                self.__lst_profile.remove(profile)
                print_debug("Removing profile\n" + str(profile))
                print_sucess(" Successfull research: " + str(nb_profile_added) + " profile" + ("s" if nb_profile_added > 1 else "") + " found.")
            else:
                print_debug("The profile " + str(hex(id(profile))) + " does not produce more valide profile")
                print_warning(" No profile found.")

    @staticmethod
    def __add_profile_in_map_tool(
        map_tool_for_profile: dict,
        profile: Profile,
        tool: Tool
    ):
        """Private method that adds profile in map_tool_for_profile.
        
        If the tool key is not define, it defines the key as an empty
        list. Else, it will only update the list.
        """
        # If the key don't exist, we define its as a list
        if profile not in map_tool_for_profile.keys():
            map_tool_for_profile[profile] = []

        # Check if the tool is already instantiated
        is_instantiated = False
        for profile_tool in map_tool_for_profile[profile]:
            if isinstance(profile_tool, tool.__class__):
                is_instantiated = True
                break

        if not is_instantiated:
            map_tool_for_profile[profile].append(tool)

    @staticmethod
    def merge_profile(profile_A: Profile, profile_B: Profile) -> Profile:
        """Method that will try to merge profiles.

        Merge if values do not produce conflicts.

        :param lst_profile: The list of all profiles, defaults to [].
        :type lst_profile: list[Profile], optional
        :return: The merged profile or None if it didn't work.
        :rtype: Profile
        """
        try:
            if (
                profile_A.get_firstname()  == profile_B.get_firstname() and
                profile_A.get_lastname()   == profile_B.get_lastname() and
                profile_A.get_gender()     == profile_B.get_gender() and
                profile_A.get_birthdate()  == profile_B.get_birthdate() and
                profile_A.get_deathdate()  == profile_B.get_deathdate() and
                profile_A.get_age()        == profile_B.get_age()
            ):
                # Clone first selected profile
                merged_profile = profile_A.clone()
                
                merged_profile.get_lst_middlenames().extend(profile_B.get_lst_middlenames())
                merged_profile.get_lst_usernames().extend(profile_B.get_lst_usernames())
                merged_profile.get_lst_phone_numbers().extend(profile_B.get_lst_phone_numbers())
                merged_profile.get_lst_emails().extend(profile_B.get_lst_emails())
                merged_profile.get_lst_accounts().extend(profile_B.get_lst_accounts())
                merged_profile.get_lst_pictures().extend(profile_B.get_lst_pictures())
                merged_profile.get_lst_ips().extend(profile_B.get_lst_ips())
                merged_profile.get_lst_addresses().extend(profile_B.get_lst_addresses())
                merged_profile.get_lst_locations().extend(profile_B.get_lst_locations())
                merged_profile.get_lst_organizations().extend(profile_B.get_lst_organizations())
                
                return merged_profile
        except:
            print_error("Merge Error")
            return None


    def remove_profile(self, profile: Profile):
        """Method that removes a profile and deletes it from the memory.

        :param profile: The profile to remove.
        :type profile: Profile
        """
        self.get_lst_profile().remove(profile)
        # Remove profile from indexed variables
        del profile

        # Clear memory using the garbage collector.
        gc.collect()


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

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gc
import uuid
from typing import Type, TypeVar

from classes.Profile import Profile
from exceptions.ToolGetProfileDuringExecutionException import ToolGetProfileDuringExecutionException
from exceptions.ToolMissDataInputException import ToolMissDataInputException
from tools.Tool import Tool

from utils.config.Config import Config
from utils.utils import print_debug
from utils.utils import print_error
from utils.utils import print_sucess
from utils.utils import print_warning
from utils.utils import remove_plural


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
        self.__profiles_visibility = self.__init_profile_visibility(default_profile)

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

    def __init_profile_visibility(self, default_profile: Profile) -> dict:
        """Method that initialize the visibility of all attributes in a
        profile.

        :param default_profile: The profile to set the visibility.
        :type default_profile: Profile
        :return: A dictionary containing the visibility for each
         attributes.
        :rtype: dict
        """

        profile_visibility = {}
        # Data type given by user are set visible.

        for attr in default_profile.__dict__:

            default_visibility = False
            if isinstance(default_profile.__dict__[attr], list):
                if len(default_profile.__dict__[attr]) >= 1:
                    default_visibility = True
            elif default_profile.__dict__[attr] is not None:
                default_visibility = True

            attr_name = attr.split("__")[-1]
            profile_visibility[attr_name] = default_visibility

        print_debug("Default visibility for research "+self.get_id())
        for key in profile_visibility.keys():
            print_debug(" - " + str(key) + " : " + str(profile_visibility[key]))
        
        return profile_visibility

    def set_profiles_visibility(self, profile_visibility: dict):
        """Setter of profiles visibility.

        :param profile_visibility: The new visibility setting.
        :type profile_visibility: dict
        """
        self.__profiles_visibility = profile_visibility

    def get_profiles_visibility(self) -> dict:
        """Getter of profiles visibility.

        :return: The current visibility setting.
        :rtype: dict
        """
        return self.__profiles_visibility

    def anonymise_unvisible_data(self, profile_to_dict: dict) -> dict:
        """Method that takes a generated dictionary from
        :py:func:`~core.utils.utils.to_dict` function and masks
        data which are set to 'unvisible' in the profiles visibility
        setting.

        :param profile_to_dict: The profile to anonymize.
        :type profile_to_dict: dict
        :return: A dictionary profile containing masked data.
        :rtype: dict
        """
        print_debug("Anonymise unvisible data.")
        for key in profile_to_dict.keys():
            if key in self.get_profiles_visibility().keys():
                if not self.get_profiles_visibility()[key]:

                    # If data should be anonymise.
                    name = str(key).replace("lst_", "").replace("_", " ")
                    nb = "1" if profile_to_dict[key] != "None" else "0"

                    if isinstance(profile_to_dict[key], list):
                        nb = str(len(profile_to_dict[key]))

                    if nb == "0":
                        name = remove_plural(name)

                    find = "found."

                    profile_to_dict[key] = nb + " " + name + " " + find
                    print_debug(" - " + str(key) + " --> " + str(profile_to_dict[key]))

        return profile_to_dict

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

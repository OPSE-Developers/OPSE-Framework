# -*- coding: utf-8 -*-

import copy

from classes.Research import Research
from utils.exceptions import PreviousException
from utils.stdin import get_int
from utils.stdout import clear, print_error, print_title, print_warning, show
from utils.utils import get_dict_key_by_index, to_dict


def main_menu(research: Research):
    """Function that displays the main menu of OPSE in CLI.

    :param research: The research associated.
    :type research: Research
    """
    choice = -1
    while choice != 5:

        if choice >= 0:
            try:
                if choice == 0:
                    menu_display_profiles(research)
                # elif choice == 1:
                #     menu_update_data_visibility(research)
                elif choice == 2:
                    menu_merge_manual_profile(research)
                elif choice == 3:
                    menu_remove_profile(research)
                elif choice == 4:
                    research.enrich_profiles()

            except PreviousException:
                pass

        clear()
        print_title("Menu")
        print("\n[0] Display profiles")
        # print("[1] Update data visibility")
        print("[2] Merge datas")
        print("[3] Remove profiles")
        print("[4] Research enrichment\n")
        print("[5] Quit\n")

        choice: int = get_int("Choice : ")

        while choice < 0 or choice > 5:
            print_error(" Wrong choice.\nPlease select value between 0 and 4.")
            choice: int = get_int("Choice : ")


def menu_merge_manual_profile(research: Research):
    """Function that displays the merge menu to the user.

    :param research: The research associated.
    :type research: Research
    """
    choice = -1
    profile_nbr = len(research.get_lst_profile())

    if profile_nbr < 2:
        print_error(" Error\n There are no profiles to merge.")
        choice: int = get_int("Choice : ")

    while choice != profile_nbr:
        if choice >= 0:
            profile_A = research.get_lst_profile().__getitem__(choice)
            choice2: int = get_int("Choose a second profile : ")

            while (choice2 < 0 or choice2 > len(research.get_lst_profile())) and choice2 != choice:
                print_error(" Wrong choice.\nPlease select value between 0 and " + str(len(research.get_lst_profile())))
                choice2: int = get_int("Choose a second profile : ")
                
            profile_B = research.get_lst_profile().__getitem__(choice2)
            try:
                # try merge
                new_profile = research.merge_profile(profile_A, profile_B)
                
                # if success enrich profiles list
                research.get_lst_profile().append(new_profile)
                # delete 2 merged profiles
                research.remove_profile(profile_A)
                research.remove_profile(profile_B)
                profile_nbr-=1

            except PreviousException:
                print_error(" Error.\nMerge Fail")
                
        clear()
        print_title("Merge profile : ")
        cpt = 0
        for profile in research.get_lst_profile():
            display_value = profile.get_summary()
            print(" - [" + str(cpt) + "] Profile : " + display_value)
            cpt += 1

        print("\n - [" + str(cpt) + "] Return\n")
        choice: int = get_int("Choice : ")

        while choice < 0 or choice > len(research.get_lst_profile()):
            print_error(" Wrong choice.\nPlease select value between 0 and " + str(len(research.get_lst_profile())))
            choice: int = get_int("Choice : ")


def menu_remove_profile(research: Research):
    """Function that displays the remove menu to the user.

    :param research: The research associated.
    :type research: Research
    """
    choice = -1
    while choice != len(research.get_lst_profile()):

        if choice >= 0:
            try:
                research.remove_profile(research.get_lst_profile().__getitem__(choice))
            except PreviousException:
                pass

        clear()
        print_title("Removable profiles : ")
        cpt = 0
        for profile in research.get_lst_profile():
            display_value = profile.get_summary()
            print(" - [" + str(cpt) + "] Profile : " + display_value)
            cpt += 1

        print("\n - [" + str(cpt) + "] Return\n")
        choice: int = get_int("Choice : ")

        while choice < 0 or choice > len(research.get_lst_profile()):
            print_error(" Wrong choice.\nPlease select value between 0 and " + str(len(research.get_lst_profile())))
            choice: int = get_int("Choice : ")


# def menu_update_data_visibility(research: Research):
#     """Function that displays the menu to update data visibility to the
#     user.

#     :param research: The research associated.
#     :type research: Research
#     """
#     choice = -1
#     previous_data_visibility: dict = copy.deepcopy(research.get_profiles_visibility())

#     while choice != len(previous_data_visibility.keys())+1:

#         if choice == len(previous_data_visibility.keys()):
#             for key in research.get_profiles_visibility().keys():
#                 research.get_profiles_visibility()[key] = True
#         elif choice == len(previous_data_visibility.keys())+1:
#             print_warning(" Modification applied.")

#         elif choice >= 0:
#             key = get_dict_key_by_index(research.get_profiles_visibility(), choice)
#             research.get_profiles_visibility()[key] = not research.get_profiles_visibility()[key]

#         clear()
#         print_title("Change data visibility ")
#         print()

#         cpt = 0
#         for key in research.get_profiles_visibility().keys():
#             visibility = "visible" if research.get_profiles_visibility()[key] else "not visible"
#             are = "is "
#             if "lst_" in key:
#                 key = key.replace("lst_", "")
#                 are = "are "
#                 visibility += "s"
#             print("["+str(cpt)+"] " + key.replace("_", " ") + " " + are + visibility)
#             cpt += 1

#         print("\n["+str(cpt)+"] Make every things visible")
#         print("\n[" + str(cpt+1) + "] Apply change.\n")
#         choice: int = get_int("Choice : ")
#         print(choice)

#         while choice < 0 or choice > len(previous_data_visibility.keys()) + 1:
#             print_error(" Wrong choice.\nPlease select value between 0 and " + str(1+len(previous_data_visibility.keys())))
#             choice: int = get_int("Choice : ")


def menu_display_profiles(research: Research):
    """Function that displays the menu to list profiles to the user.

    :param research: The research associated.
    :type research: Research
    """
    choice = -1
    while choice != len(research.get_lst_profile()):

        if choice >= 0:
            try:
                profile = research.get_lst_profile().__getitem__(choice)
                menu_display_data_in_profile_dict(
                    to_dict(profile),
                    " Profile : "+str(profile.get_summary())
                )

            except PreviousException:
                pass

        clear()
        print_title("Display profile : ")
        cpt = 0
        for profile in research.get_lst_profile():
            display_value = profile.get_summary()
            print(" - [" + str(cpt) + "] Profile : " + display_value)
            cpt += 1

        print("\n - [" + str(cpt) + "] Return\n")
        choice: int = get_int("Choice : ")

        while choice < 0 or choice > len(research.get_lst_profile()):
            print_error(" Wrong choice.\nPlease select value between 0 and " + str(len(research.get_lst_profile())))
            choice: int = get_int("Choice : ")


def menu_display_data_in_profile_dict(dict_values: dict, display_name: str = "Menu :"):
    """Function that builds dynamically a menu using an OPSE
    functionality.

    :param dict_values: The dict to show.
    :type dict_values: dict
    :param display_name: The menu name, defaults to "Menu :"
    :type display_name: str, optional
    """
    clear()
    print(show(dict_values, [], display_name))
    print("Press any key to return.")
    input()










# -*- coding: utf-8 -*-

from classes.Profile import Profile
from classes.account.Account import Account
from tools.Tool import Tool

from utils.datatypes import DataTypeInput, DataTypeOutput
from utils.stdout import print_debug, print_error, print_warning


class ExampleTool(Tool):
    """
    Class which describe an ExampleTool
    """
    deprecated = False

    def __init__(self):
        super().__init__()
        self.example_arg = 0

    @staticmethod
    def get_config() -> dict[str]:
        return {
            'example_parameter_1': 'default_user_conf',
            'example_parameter_2': True
        }

    @staticmethod
    def get_lst_input_data_types() -> dict[str, bool]:
        return {
            DataTypeInput.USERNAME: True, # Required data
            DataTypeInput.EMAIL: False, # Optionnal data
        }

    @staticmethod
    def get_lst_output_data_types() -> list[str]:
        return [
            DataTypeOutput.ACCOUNT,
        ]

    def execute(self):
        default_profile = self.get_default_profile()

        # Your main code goes here.
        # Example: Get the account of the username on example.com.
        accounts: list = [Account]
        for username in default_profile.get_lst_usernames():
            try:
                # You have to develop this \/ \/ \/ \/ \/ \/ \/
                example_account: Account = get_example_account(username)
                # You can request an API or scrap a website, found dirty
                # requests on the web and get data.

                accounts.append(example_account)

            except Exception as e:
                # Might be an error during the request
                print_error(" " + str(e))

        profile: Profile = default_profile.clone()
        profile.set_lst_accounts(accounts)
        self.append_profile(profile)

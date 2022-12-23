#!/usr/bin/python3
# -*- coding: utf-8 -*-

import signal
import logging
import argparse
import traceback
from api.Api import Api
from view.menu import main_menu
from utils.utils import print_sucess
from utils.config.Config import Config
from utils.signals import previous
from utils.make_research import make_research
from exceptions.PreviousException import PreviousException
from utils.config.default_config import get_default_config
from utils.utils import get_today_date, clear, print_error, init_log_path


class Opse:
    """
    Opse is the main class of this project.
    It must contain all abstract information to perform a research on a
    target.
    """

    __api: Api = None

    @staticmethod
    def launch_api():
        Opse.__api = Api.get()
        Opse.__api.start()
        Opse.__api.join()


def main():
    clear()
    
    # Catch CTRL-C to reset without errors the system.
    try:
        signal.signal(signal.SIGINT, previous)

        # Initiation of config and log directory
        Config.get(get_default_config())

        YES = [True, 'Yes', 'yes', 'y', 'True', 'true', '1']

        parser = argparse.ArgumentParser()
        parser.add_argument('-R', '--research', help="Do a research", action='store', const=True, nargs='?')
        parser.add_argument('-f', '--firstname', help="Target's firstname")
        parser.add_argument('-m', '--middlename', help="Target's midle name")
        parser.add_argument('-l', '--lastname', help="Target's lastname")
        parser.add_argument('-g', '--gender', help="Target's gender")
        parser.add_argument('-b', '--birthdate', help="Target's birthdate (must follow this format dd/mm/YYYY)")
        parser.add_argument('-a', '--age', help="Target's age (must be integer)")
        parser.add_argument('-d', '--address', help="Target's address", nargs="+")
        parser.add_argument('-p', '--phone', help="Target's phone", nargs="+")
        parser.add_argument('-e', '--email', help="Target's email", nargs="+")
        parser.add_argument('-u', '--username', help="Target's username", nargs="+")
        parser.add_argument('-S', '--strict', help="Strict mode", action='store', const=True, nargs='?')
        parser.add_argument('-D', '--debug', help="Debug mode", action='store', const=True, nargs='?')
        parser.add_argument('-A', '--api', help="Launch the API", action='store', const=True, nargs='?')

        args = parser.parse_args()

        target_firstname = args.firstname
        target_middlename = args.middlename
        target_lastname = args.lastname
        target_gender = args.gender
        target_birthdate = args.birthdate
        target_age = args.age
        target_address = args.address
        target_phone = args.phone
        target_email = args.email
        target_username = args.username

        if args.debug in YES:
            Config.set_debug(True)

        if args.strict is not None and args.strict not in YES:
            Config.set_strict(False)

        init_log_path()
        log_level = logging.DEBUG if Config.get()["config"]["debug"] else logging.INFO
        log_path = str(Config.get()["config"]["log_path"]) + "/" + str(get_today_date("%Y%m%d")) + "_opse.log"
        logging.basicConfig(format='%(asctime)s - %(message)s', level=log_level, filename=log_path, filemode='w')

        if args.api in YES:
            Opse.launch_api()

        if args.research in YES:
            print_sucess(" Starting new research...")
            main_menu(make_research(
                    target_firstname,
                    target_middlename,
                    target_lastname,
                    target_gender,
                    target_birthdate,
                    target_age,
                    target_address,
                    target_phone,
                    target_email,
                    target_username,
                )
            )

    except PreviousException:
        pass

    except Exception as e:
        print_error(str(e) + "\n" + (traceback.format_exc() if Config.is_debug() else ""))


if __name__ == "__main__":
    main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

NAME    = "OPSE"
SCRIPT  = "opse.py"
VERSION = "2.0.0"
AUTHORS = "OPSE Developpers"
LICENSE = "GNU GPLv3"
COPYRIGHT = "Copyright (c) OPSE 2021-2023"

CREATION = "2021-09-15"
LTUPDATE = "2023-01-16"

# Must be firt
from utils import YES

import argparse
import logging
import signal
import textwrap
import time
import traceback
import os
import webbrowser

from api.Api import Api
from classes.Research import make_research
from tools.Tool import Tool
from utils.config.Config import Config, get_default_config
from utils.exceptions import PreviousException
from utils.menu import main_menu
from utils.signals import previous
from utils.stdout import Colors, clear, print_error, print_sucess
from utils.utils import check_py_version, get_today_date, import_subclasses, init_log_path


def args_parser():
    # Creating main argument parser
    parser = argparse.ArgumentParser(
        prog='opse.py', 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='OPSE Framework, gather information quickly.', 
        epilog=textwrap.dedent(f'''\
        Implementation:
          Version      {SCRIPT} {VERSION}
          Authors      {AUTHORS}
          Copyright    {COPYRIGHT}
          License      {LICENSE}  
        ''')
    )
    # Script Options
    parser.add_argument('-D', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-V', '--version', action='store_true', help='Print script version and exit')
    parser.add_argument('-S', '--strict', action='store_true', help='Disable strict mode')
    parser.add_argument('-A', '--api', action='store_true', help="Launch the API only")

    parser.add_argument('-f', '--firstname', type=str, help='Specify target\'s firstname')
    parser.add_argument('-m', '--middlename', type=str, help='Specify target\'s middlename', nargs="+")
    parser.add_argument('-l', '--lastname', type=str, help='Specify target\'s lastname')
    parser.add_argument('-g', '--gender',type=str, choices=['female', 'male'],help='Specify target\'s gender.')
    parser.add_argument('-b', '--birthdate', type=str, help='Specify target\'s date of birth. Format: <YYYYMMDD>')
    parser.add_argument('-a', '--age', type=str, help='Specify target\'s age')
    parser.add_argument('-d', '--address', type=str, help='Specify target\'s address')
    parser.add_argument('-e', '--email', type=str, help='Specify target\'s email address', nargs="+")
    parser.add_argument('-p', '--phone', type=str, help='Specify target\'s phone number. Format: <+33XXXXXXXXX>', nargs="+")
    parser.add_argument('-u', '--username', type=str, help='Specify target\'s username', nargs="+")

    return parser

class OPSE:
    """
    OPSE is the main class of this project.
    """

    @staticmethod
    def main():
        try:
            # Catch CTRL-C to reset without errors the system.
            signal.signal(signal.SIGINT, previous)

            # Check if python version is >=3.8
            check_py_version()

            # Get parser
            parser = args_parser()
            # Parse args
            args = parser.parse_args()

            # Print version
            if args.version:
                print(f"OPSE {VERSION}")
                exit()

            at_least_one: list = [
                args.firstname,
                args.middlename,
                args.lastname,
                args.gender,
                args.birthdate,
                args.age,
                args.address,
                args.phone,
                args.email,
                args.username,
                args.api
            ]
            # Exit without at_least_one
            if not any(at_least_one):
                parser.print_help()
                exit()
            
            # Set debug mode with argument
            Config.get().setdefault('config', {'debug':args.debug})

            # Initialization of configuration
            opse_config = get_default_config()

            # Import tools
            Tool.lst_available_tools = import_subclasses(Tool, "tools")

            # Exit without plugin
            if len(Tool.lst_available_tools) == 0:
                print_error(" No plugin was loaded.")
                exit(1)

            # Load tools configurations
            opse_config["config"]["tools"] = Tool.get_tool_config()
            Config.update_config(opse_config)

            init_log_path()
            log_level = logging.DEBUG if Config.get()["config"]["debug"] else logging.INFO
            log_path = str(Config.get()["config"]["log_path"]) + "/" + str(get_today_date("%Y%m%d")) + "_opse.log"
            logging.basicConfig(format='%(asctime)s - %(message)s', level=log_level, filename=log_path, filemode='w')
            clear()

            if args.debug in YES:
                Config.set_debug(True)         

            __api: Api = None
            if args.api in YES:
                __api = Api.get()
                __api.daemon = True
                __api.start()
                
                # access webview
                index_path = 'file://' + os.path.realpath("webview/index.html")
                try:
                    webbrowser.open(index_path)
                except:
                    print_sucess("Access webview from this link: " + index_path)

                while True:
                    time.sleep(0.1)
            
            else:
                main_menu(make_research(
                    args.firstname,
                    args.middlename,
                    args.lastname,
                    args.gender,
                    args.birthdate,
                    args.age,
                    args.address,
                    args.phone,
                    args.email,
                    args.username)
                )
        
        except PreviousException:
            print('\n' + Colors.ITALIC + "Exit" + Colors.ENDC)
            pass

        except Exception as e:
            print_error(" " + str(e) + "\n" + (traceback.format_exc() if Config.is_debug() else ""))

if __name__ == "__main__":
    try:
        OPSE.main()
    except PreviousException:
        exit(1)
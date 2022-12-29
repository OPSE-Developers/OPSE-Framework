#!/usr/bin/python3
# author : OPSE Developpers
# date   : 2022-12-24
VERSION = "1.0.0"

import argparse
import textwrap
import os
import sys
from datetime import datetime

def verify_date(input_date):
  try:
    datetime.strptime(input_date, '%Y%m%d')
    return True
  except ValueError:
    return False

def check_py_version():
    if not sys.version_info >= (3,8):
        print("Python 3.8 or higher is required.")
        print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
        sys.exit(1)

def args_parser():
    # Creating main argument parser
    parser = argparse.ArgumentParser(
        prog='Opse.py', 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Simple commands to deploy OPSE containers.', 
        epilog=textwrap.dedent(f'''\
        Implementation:
          Version      Opse.py {VERSION}
          Authors      OPSE Developpers
          Copyright    Copyright (c) OPSE 2021-2022
          License      OPSE License  
        ''')
    )
    # Script Options
    parser.add_argument('-D', '--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-V', '--version', action='store_true', help='Print script version and exit')
    parser.add_argument('-S', '--strict', action='store_true', help='Strict mode, input are case sensitive')

    # Creating sub argument parser
    sub_parsers = parser.add_subparsers(help='OPSE mode', required=True, dest='mode')

    # Creating parser for cli mode
    parser_cli = sub_parsers.add_parser('cli', help='Launch the CLI') 
    parser_cli.add_argument('-f', '--firstname', type=str, help='Specify target\'s firstname')
    parser_cli.add_argument('-l', '--lastname', type=str, help='Specify target\'s lastname')
    parser_cli.add_argument('-g', '--gender',type=str, choices=['female', 'male'],help='Specify target\'s gender.')
    parser_cli.add_argument('-a', '--age', type=str, help='Specify target\'s age')
    parser_cli.add_argument('-b', '--birthdate', type=str, help='Specify target\'s date of birth. Format: <YYYYMMDD>')
    parser_cli.add_argument('-d', '--address', type=str, help='Specify target\'s address')
    parser_cli.add_argument('-m', '--middlename', type=str, help='Specify target\'s middlename', nargs="+")
    parser_cli.add_argument('-e', '--email', type=str, help='Specify target\'s email address', nargs="+")
    parser_cli.add_argument('-p', '--phone', type=str, help='Specify target\'s phone number. Format: <+33XXXXXXXXX>', nargs="+")
    parser_cli.add_argument('-u', '--username', type=str, help='Specify target\'s username', nargs="+")

    # Creating parser for gui mode
    parser_gui = sub_parsers.add_parser('gui', help='Launch the GUI')

    args = parser.parse_args()
    return args

def launch_OPSE(args):
    # Print version & exit 
    if args.version:
        print(f"OPSE {VERSION}")
        exit()

    #----- Args control -----
    try:

        # Determine OS
        OS_NAME = sys.platform
        if OS_NAME == "linux":
            OPSE_CMD = "python3 core/Opse.py"
        elif OS_NAME == "win32":
            OPSE_CMD = "python .\core\Opse.py"
        elif OS_NAME == "darwin":
            OPSE_CMD = "python3 core/Opse.py"
        else:
            print("Exiting... Wrong OS !")
            exit()

        # CLI mode
        if args.mode == "cli":
            OPSE_CMD += " -R" # research launch option 
            
            # Opse.py specific args
            if args.debug:
                OPSE_CMD += " -D" # research debug option 
            if args.strict:
                OPSE_CMD += " -S" # research strict option 

            # mono input args
            if args.firstname:
                OPSE_CMD += f" --firstname {args.firstname}"
            if args.lastname:
                OPSE_CMD += f" --lastname {args.lastname}"
            if args.gender:
                OPSE_CMD += f" --gender {args.gender}"
            if args.age:
                OPSE_CMD += f" --age {args.age}"
            if args.birthdate:
                if verify_date(args.birthdate):
                    OPSE_CMD += f" --birthdate {args.birthdate}"
                else:
                    print("[*] ERROR: Please provide a valid date. Format: <YYYYMMDD>")
                    exit()
            if args.address:
                OPSE_CMD += f" --address {args.address}"
            
            # multi input args
            if args.middlename:
                OPSE_CMD += " --middlename"
                for middlename in args.middlename:
                    OPSE_CMD += f" {middlename}"
            if args.email:
                OPSE_CMD += f" --email"
                for email in args.email:
                    OPSE_CMD += f" {email}"
            if args.phone:
                OPSE_CMD += f" --phone"
                for phone in args.phone:
                    OPSE_CMD += f" {phone}"
            if args.username:
                OPSE_CMD += f" --username"
                for username in args.username:
                    OPSE_CMD += f" {username}"

            os.system(OPSE_CMD)

        # GUI mode
        elif args.mode == "gui":
            OPSE_CMD += " -A"

            if args.debug:
                OPSE_CMD += " -D"
            if args.strict:
                OPSE_CMD += " -S"

            os.system(OPSE_CMD)
    
    except Exception as e:
        print(str(e))
        exit()

if __name__ == '__main__':
    # check if python version is >=3.8
    check_py_version()

    args = args_parser()
    launch_OPSE(args)

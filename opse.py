#!/usr/bin/python3
# author : OPSE Developpers
# date   : 2022-12-24
VERSION = "1.0.0"

import argparse
import textwrap
import os

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
    parser_cli.add_argument('-a', '--age', type=str, help='Specify target\'s age')
    parser_cli.add_argument('-b', '--birthdate', type=str, help='Specify target\'s date of birth. Format: <YYYYMMDD>')
    parser_cli.add_argument('-d', '--address', type=str, help='Specify target\'s address')
    parser_cli.add_argument('-e', '--email', type=str, help='Specify target\'s email address')
    parser_cli.add_argument('-f', '--firstname', type=str, help='Specify target\'s firstname')
    parser_cli.add_argument('-g', '--gender', type=str, help='Specify target\'s gender. Possible values: <male|female>')
    parser_cli.add_argument('-l', '--lastname', type=str, help='Specify target\'s lastname')
    parser_cli.add_argument('-m', '--middlename', type=str, help='Specify target\'s middlename')
    parser_cli.add_argument('-p', '--phone', type=str, help='Specify target\'s phone number. Format: <+33XXXXXXXXX>')
    parser_cli.add_argument('-u', '--username', type=str, help='Specify target\'s username')

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
        # CLI mode
        if args.mode == "cli":
            OPSE_CMD = "./core/Opse.py -R"
            
            if args.debug:
                OPSE_CMD += " -D"
            if args.strict:
                OPSE_CMD += " -S"

            if args.age:
                OPSE_CMD += f" --age {args.age}"
            if args.birthdate:
                OPSE_CMD += f" --birthdate {args.birthdate}"
            if args.address:
                OPSE_CMD += f" --address {args.address}"
            if args.email:
                OPSE_CMD += f" --email {args.email}"
            if args.firstname:
                OPSE_CMD += f" --firstname {args.firstname}"
            if args.gender:
                OPSE_CMD += f" --gender {args.gender}"
            if args.lastname:
                OPSE_CMD += f" --lastname {args.lastname}"
            if args.middlename:
                OPSE_CMD += f" --middlename {args.middlename}"
            if args.phone:
                OPSE_CMD += f" --phone {args.phone}"
            if args.username:
                OPSE_CMD += f" --username {args.username}"

            os.system(OPSE_CMD)

        # GUI mode
        elif args.mode == "gui":
            OPSE_CMD = "./core/Opse.py -A"

            if args.debug:
                OPSE_CMD += " -D"
            if args.strict:
                OPSE_CMD += " -S"

            os.system(OPSE_CMD)
    
    except Exception as e:
        print(str(e))
        exit()

if __name__ == '__main__':
    args = args_parser()
    launch_OPSE(args)

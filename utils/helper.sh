#!/bin/bash
#===============================================================================
#% SYNOPSIS
#+    ${SCRIPT_NAME} <subcommand> [OPTIONS...]
#%
#% DESCRIPTION
#%    Simple commands to deploy OPSE containers.
#%
#% SUBCOMMANDS
#%    cli [OPTIONS...]        Launch the CLI
#%    gui [OPTIONS...]        Launch the GUI
#%    help <CMD|OPT>          Print a specific help about CMD or OPT
#%
#% CLI SUBCOMMAND OPTIONS
#%    -a, --age string        Specify target's age
#%    -b, --birthdate string  Specify target's date of birth. Format: <YYYYMMDD>
#%    -d, --address string    Specify target's address
#%    -e, --email string      Specify target's email address
#%    -f, --firstname string  Specify target's firstname
#%    -g, --gender string     Specify target's gender. Possible values: <male|female>
#%    -l, --lastname string   Specify target's lastname
#%    -n, --name string       Specify target's name
#%    -p, --phone string      Specify target's phone number. Format: <+33XXXXXXXXX>
#%    -u, --username string   Specify target's username
#%
#% SCRIPT OPTIONS
#%    -F, --dockercompose     Path to docker-compose file
#%    -C, --clear             Clear Docker containers
#%    -D, --debug             Enable debug
#%    -h, --help              Print this help and exit
#%    -v, --version           Print script version and exit
#%
#-
#- IMPLEMENTATION
#-    Version                 ${SCRIPT_NAME} ${VERSION}
#-    Authors                 OPSE Developpers
#-    Copyright               Copyright (c) OPSE 2021-2022
#-    License                 OPSE License
#===============================================================================


#===================================
#     GENERAL HELP
#===================================
usage() { printf "Usage: "; head -38 "./utils/helper.sh" | grep "^#+" | sed -e "s/^#+[ ]*//g" -e "s/\${SCRIPT_NAME}/${SCRIPT_NAME}/g" ; }
usage_full() { head -38 "./utils/helper.sh" | grep -e "^#[%+-]" | sed -e "s/^#[%+-]//g" -e "s/\${SCRIPT_NAME}/${SCRIPT_NAME}/g" -e "s/\${VERSION}/${VERSION}/g" ; }


#===================================
#     SPECIFIC HELP
#===================================

# Subcommand executed when word 'help' is used
# Print help about a specific command or option passed as next parameter
help() {
  case "$1" in
    cli)
      echo -e "\nUsage: bash opse.sh cli [OPTIONS...]
      \nLaunch the command line interface
      \nOptions:
        -a, --age string        Specify target's age
        -b, --birthday string   Specify target's date of birth. Format: <YYYYMMDD>
        -d, --address string    Specify target's address
        -e, --email string      Specify target's email address
        -f, --firstname string  Specify target's firstname
        -g, --gender string     Specify target's gender. Possible values: <male|female>
        -n, --name string       Specify target's name
        -p, --phone string      Specify target's phone number. Format: <+33XXXXXXXXX>
        -s, --pseudo string     Specify target's pseudo"
      ;;
    gui)
      echo -e "\nUsage: bash opse.sh gui [OPTIONS...]
      \nLaunch the graphical user interface
      \nOptions:
        -a, --age string        Specify target's age
        -b, --birthday string   Specify target's date of birth. Format: <YYYYMMDD>
        -d, --address string    Specify target's address
        -e, --email string      Specify target's email address
        -f, --firstname string  Specify target's firstname
        -g, --gender string     Specify target's gender. Possible values: <male|female>
        -n, --name string       Specify target's name
        -p, --phone string      Specify target's phone number. Format: <+33XXXXXXXXX>
        -s, --pseudo string     Specify target's pseudo"
      ;;
    help)
      echo -e "\nUsage: bash opse.sh help <CMD|OPT>
      \nShow a specific help page about a command or an option
      \nCommands and Options:
        cli
        gui
        help
        -a, --age
        -b, --birthday
        -d, --address
        -e, --email
        -f, --firstname
        -g, --gender
        -n, --name
        -p, --phone
        -s, --pseudo
        -F, --dockercompose
        -D, --debug
        -h, --help
        -v, --version"
      ;;
    -h|--help)
      echo -e "\nUsage: bash opse.sh $1
      \nPrint script usage"
      ;;
    -a|--age)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's age for the script"
      ;;
    -b|--birthday)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's date of birth for the script. Format: <YYYYMMDD>"
      ;;
    -d|--address)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's address for the script."
      ;;
    -e|--email)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's email for the script."
      ;;
    -f|--firstname)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's firstname for the script."
      ;;
    -g|--gender)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's gender for the script. Possible values: <male|female>"
      ;;
    -n|--name)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's name for the script."
      ;;
    -p|--phone)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's phone for the script. Format: <+33XXXXXXXXX>"
      ;;
    -s|--pseudo)
      echo -e "\nUsage: bash opse.sh <cli|gui> $1
      \nSpecify target's pseudo for the script."
      ;;
    -F|--dockercompose)
      echo -e "\nUsage: bash opse.sh $1
      \nSpecify path to docker-compose file"
      ;;
    -D|--debug)
      echo -e "\nUsage: bash opse.sh $1
      \nActivate debug mode"
      ;;
    -v|--version)
      echo -e "\nUsage: bash opse.sh $1
      \nPrint script version"
      ;;
    "") # no option
      echo "Error: help command requires an option" >&2 ;;
    *) # unsupported flags
      echo "Error: Unsupported option '$1'" >&2 ;;
  esac
  exit 13
}

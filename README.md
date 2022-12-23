# OPSE

OPSE stands for OSINT People Search Engine.

## Description

As its name suggests, OPSE is a search engine based on Open Source INTelligence. It is a semi-automatic tool that requieres at least one input data like a full name or an email address and displays all the informations it can find or interpret.

## Context

This project is carried out within the framework of graduate studies at the Ecole Nationale Supérieure d'Ingénieurs de Bretagne Sud.

## Installation

### Prerequisites

Before installing OPSE, your environment needs some prerequisites.

#### Python 3.X

```
sudo apt update -y && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
```

#### Git

```
sudo apt update -y && sudo apt upgrade -y
sudo apt install git -y
```

### Install OPSE

With Git, you can get OPSE repositories:
- opse-framework (the framework);
- opse-gui (the web interface).

```
mkdir opse; cd opse
git clone --recurse-submodules https://gitlab.com/opse-dev/opse-framework.git
git clone https://gitlab.com/opse-dev/opse-gui.git
```

Once you got the repositories, you have to launch the installation script `install.sh`.

The original script will install Linux requirements, get Docker repository and install Docker.

```
cd opse-framework
bash install.sh
```

If you want to use OPSE in your local environment (and not in a Docker container), just add the option `--local`.

## Start OPSE

Once the installation is complete, you can start OPSE.

## Usage

```
SYNOPSIS
    opse.sh <subcommand> [OPTIONS...]

 DESCRIPTION
    Simple commands to deploy OPSE containers.

 SUBCOMMANDS
    cli [OPTIONS...]        Launch the CLI
    gui [OPTIONS...]        Launch the GUI
    help <CMD|OPT>          Print a specific help about CMD or OPT

 CLI SUBCOMMAND OPTIONS
    -a, --age string        Specify target's age
    -b, --birthdate string  Specify target's date of birth. Format: <YYYYMMDD>
    -d, --address string    Specify target's address
    -e, --email string      Specify target's email address
    -f, --firstname string  Specify target's firstname
    -g, --gender string     Specify target's gender. Possible values: <male|female>
    -l, --lastname string   Specify target's lastname
    -n, --name string       Specify target's name
    -p, --phone string      Specify target's phone number. Format: <+33XXXXXXXXX>
    -u, --username string   Specify target's username

 SCRIPT OPTIONS
    -C, --clear             Clear Docker containers
    -D, --debug=TRUE|FALSE  Enable debug
    -S, --strict=TRUE|FALSE Enable strict mode
    -h, --help              Print this help and exit
    -v, --version           Print script version and exit


 IMPLEMENTATION
    Version                 opse.sh 0.0.0
    Authors                 OPSE Developpers
    Copyright               Copyright (c) OPSE 2021-2022
    License                 OPSE License
```

## License

[See __OPSE License__](LICENSE)

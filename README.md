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
git clone --recurse-submodules https://github.com/OPSE-Developers/OPSE-Framework.git
git clone https://github.com/OPSE-Developers/OPSE-Gui.git
```

Once you got the repositories, you have to install OPSE requirements.

```bash
python3 -m pip install -r requirements.txt
```

Once requirements are installed you can launch `./opse.py` launcher.

## Plugins

| Plugin Name                 | Link                                                            | State    |
| --------------------------- | --------------------------------------------------------------- | -------- |
| OPSE-Death-Plugin           | https://github.com/OPSE-Developers/OPSE-Death-Plugin            | OK ✅    |
| OPSE-Facebook-Plugin        | https://github.com/OPSE-Developers/OPSE-Facebook-Plugin         | OK ✅    |
| OPSE-Holehe-Plugin          | https://github.com/OPSE-Developers/OPSE-Holehe-Plugin           | OK ✅    |
| OPSE-Records-Plugin         | https://github.com/OPSE-Developers/OPSE-Records-Plugin          | OK ✅    |
| OPSE-Twitter-Plugin         | https://github.com/OPSE-Developers/OPSE-Twitter-Plugin          | OK ✅    |
| OPSE-InstantUsername-Plugin | https://github.com/OPSE-Developers/OPSE-InstantUsername-Plugin  | OK ✅    |

## Start OPSE

```bash
./opse.py <cli|gui> <options>
```

## Usage

```
usage: Opse.py [-h] [-D] [-V] [-S] {cli,gui} ...

Simple commands to deploy OPSE containers.

positional arguments:
  {cli,gui}      OPSE mode
    cli          Launch the CLI
    gui          Launch the GUI

optional arguments:
  -h, --help     show this help message and exit
  -D, --debug    Enable debug mode
  -V, --version  Print script version and exit
  -S, --strict   Strict mode, input are case sensitive

Implementation:
  Version      Opse.py 1.0.0
  Authors      OPSE Developpers
  Copyright    Copyright (c) OPSE 2021-2022
  License      OPSE License
```

### CLI Usage

```
usage: Opse.py cli [-h] [-a AGE] [-b BIRTHDATE] [-d ADDRESS] [-e EMAIL] [-f FIRSTNAME] [-g GENDER] [-l LASTNAME] 
                   [-m MIDDLENAME] [-p PHONE] [-u USERNAME]

optional arguments:
  -h, --help            show this help message and exit
  -a AGE, --age AGE     Specify target's age
  -b BIRTHDATE, --birthdate BIRTHDATE    Specify target's date of birth. Format: <YYYYMMDD>
  -d ADDRESS, --address ADDRESS          Specify target's address
  -e EMAIL, --email EMAIL                Specify target's email address
  -f FIRSTNAME, --firstname FIRSTNAME    Specify target's firstname
  -g GENDER, --gender GENDER             Specify target's gender. Possible values: <male|female>
  -l LASTNAME, --lastname LASTNAME       Specify target's lastname
  -m MIDDLENAME, --middlename MIDDLENAME Specify target's middlename
  -p PHONE, --phone PHONE                Specify target's phone number. Format: <+33XXXXXXXXX>
  -u USERNAME, --username USERNAME       Specify target's username

```

## License

[See __OPSE License__](LICENSE)

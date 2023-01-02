# OPSE

OPSE stands for OSINT People Search Engine.

## Description

As its name suggests, OPSE is a search engine based on Open Source INTelligence. It is a semi-automatic tool that requieres at least one input data like a full name or an email address and displays all the informations it can find or interpret.

## Context

This project is carried out within the framework of graduate studies at the Ecole Nationale Supérieure d'Ingénieurs de Bretagne Sud.

## Installation

### Prerequisites

Before installing OPSE, your environment needs some prerequisites.

#### Python >=3.8

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

With Git, you can get OPSE-Framework repository:

```
mkdir opse; cd opse
git clone --recurse-submodules https://github.com/OPSE-Developers/OPSE-Framework.git
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
./opse.py <options>
```

## Usage

```
$ ./opse.py --help
usage: opse.py [-h] [-D] [-V] [-S] [-G] [-f FIRSTNAME] [-l LASTNAME]
               [-g {female,male}] [-a AGE] [-b BIRTHDATE] [-d ADDRESS]
               [-m MIDDLENAME [MIDDLENAME ...]] [-e EMAIL [EMAIL ...]]
               [-p PHONE [PHONE ...]] [-u USERNAME [USERNAME ...]]

Simple commands to deploy OPSE containers.

options:
  -h, --help            show this help message and exit
  -D, --debug           Enable debug mode
  -V, --version         Print script version and exit
  -S, --strict          Disable strict mode
  -G, --gui             Launch OPSE in GUI mode

  -f FIRSTNAME, --firstname FIRSTNAME
                        Specify target's firstname
  -l LASTNAME, --lastname LASTNAME
                        Specify target's lastname
  -g {female,male}, --gender {female,male}
                        Specify target's gender.
  -a AGE, --age AGE     Specify target's age
  -b BIRTHDATE, --birthdate BIRTHDATE
                        Specify target's date of birth. Format: <YYYYMMDD>
  -d ADDRESS, --address ADDRESS
                        Specify target's address
  -m MIDDLENAME [MIDDLENAME ...], --middlename MIDDLENAME [MIDDLENAME ...]
                        Specify target's middlename
  -e EMAIL [EMAIL ...], --email EMAIL [EMAIL ...]
                        Specify target's email address
  -p PHONE [PHONE ...], --phone PHONE [PHONE ...]
                        Specify target's phone number. Format: <+33XXXXXXXXX>
  -u USERNAME [USERNAME ...], --username USERNAME [USERNAME ...]
                        Specify target's username

Implementation:
  Version      opse.py X.X.X
  Authors      OPSE Developpers
  Copyright    Copyright (c) OPSE 2021-2023
  License      OPSE License

```

## License

[See __OPSE License__](LICENSE)

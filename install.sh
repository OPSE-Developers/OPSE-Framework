#!/bin/bash
# author : OPSE Developpers
# date   : 2022-03-23
# version: 0.0.1


#== Set constants ==# 
typeset -r usage="[-] Usage: bash install.sh [OPTIONS...]
  Launch the install of OPSE requirements
[-] Options:
    -l, --local        Install python requirements on local machine (for local use only)
    -v, --version      Print script version
    -h, --help         Print this help"
typeset -r VERSION="0.0.1"
typeset -r SCRIPT_NAME="$0"
typeset -r CURRENT_USER="$USER"

# -----------------------------------------------------------------------------------------------------------------
# STEP-0: OPTION PARSING
# -----------------------------------------------------------------------------------------------------------------
# if no option print usage
# if (( $# == 0 )); then # check cmd execution
#   echo "$usage"
#   exit 1
# fi

# option parser
while (( "$#" )); do
  case "$1" in
    -l|--local)
      pLOCAL="TRUE"
      shift
      ;;
    -h|--help)
      echo "$usage"
      exit 1
      ;;
    -v|--version)
      echo "${SCRIPT_NAME} ${VERSION}"
      exit 2
      ;;
    *)
      echo "Error: Unknown argument '$1'" >&2
      exit 99
      ;;
  esac
done

# -----------------------------------------------------------------------------------------------------------------
# Control Argument

# -----------------------------------------------------------------------------------------------------------------
# STEP-1: Installation of OPSE
# -----------------------------------------------------------------------------------------------------------------
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    if [ "${pLOCAL}" == "TRUE" ]; then
        echo "[-] Install python requirements locally..."
        # python3 setup.py install # ToDo pip3 install OPSE
        # pushd opse-framework
        pip3 install -r core/requirements.txt > /dev/null
        echo "[-] You can now run OPSE script locally 'python3 core/Opse.py -h' to show usages"
        exit 10
    else
        # Install required package for docker install
        if [ -f "/usr/share/keyrings/docker-archive-keyring.gpg" ]; then
            echo "[-] Dockers official GPG key already imported."
        else
            echo "[-] Adding Docker official GPG key and repository..."
            sudo apt-get update 1> /dev/null
            sudo apt-get install -y \
                ca-certificates \
                curl \
                gnupg \
                lsb-release 1> /dev/null

            # get OS Informations
            OS_DISTR="$(lsb_release -is)"           # debian
            OS_VERSION="$(lsb_release -cs)"         # bullseye
            OS_ARCH="$(dpkg --print-architecture)"  # amd64

            # get docker gpg key
            curl -fsSL "https://download.docker.com/linux/${OS_DISTR,,}/gpg" | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
            # add docker repo to apt source.list
            echo \
                "deb [arch=${OS_ARCH} signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/${OS_DISTR,,} \
                ${OS_VERSION} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        fi

        # Install docker
        echo "[-] Installing docker packages..."
        sudo apt-get update 1> /dev/null
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin 1> /dev/null

        # Todo: check if user in group
        echo "[-] Add user to docker group..."
        sudo groupadd docker
        sudo usermod -aG docker ${CURRENT_USER}
        echo "[-] Need a restart to complete the installation"

    fi

elif [[ "$OSTYPE" == "msys" ]]; then
    # Windows
    if [ "${pLOCAL}" == "TRUE" ]; then
      echo "[-] Install python requirements locally..."
      # python3 setup.py install # ToDo
      # cd core
      pip3 install -r core/requirements.txt > /dev/null
      echo "[-] You can now run OPSE script locally 'python core/Opse.py -h' to show usages"
      exit 10
    else
      echo "[-] Please install docker from https://docs.docker.com/desktop/windows/install/"
    fi
# elif [[ "$OSTYPE" == "darwin"* ]]; then
#         # Mac OSX
# elif [[ "$OSTYPE" == "cygwin" ]]; then
# #         # POSIX compatibility layer and Linux environment emulation for Windows
# elif [[ "$OSTYPE" == "win32" ]]; then
#         # I'm not sure this can happen.
# elif [[ "$OSTYPE" == "freebsd"* ]]; then
#         # ...
else
        # Unknown.
        echo "[*] Error. Unknown exploitation system."
fi

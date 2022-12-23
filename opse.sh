#!/bin/bash
# author : OPSE Developpers
# date   : 2022-03-23
# version: 0.0.1
# -----------------------------------------------------------------------------------------------------------------
# Error codes:      1-      No arg
#                   10-13   Helps
#                   20-49   Opts error
#                   50-100  Ctrl args error
#                   99-     Unknown arg
# -----------------------------------------------------------------------------------------------------------------

#== Sources ==#
source utils/helper.sh

#== Set constants ==#
typeset -r SCRIPT_NAME="$0"
typeset -r VERSION="0.0.1"
typeset -r SCRIPT_ARGUMENTS="$*"

# -----------------------------------------------------------------------------------------------------------------
# STEP-0: OPTION PARSING
# -----------------------------------------------------------------------------------------------------------------
# if no option print usage
if (( $# == 0 )); then # check cmd execution
  usage
  exit 1
fi

# option parser
while (( "$#" )); do
  case "$1" in
    cli)
      pCLI="TRUE"
      shift
      ;;
    gui)
      pGUI="TRUE"
      shift
      ;;
    help)
      pHELP="TRUE"
      help "$2"
      ;;
    -l|--lastname)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pLASTNAME="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 20
      fi
      ;;
    -f|--firstname)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pFIRSTNAME="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 21
      fi
      ;;
    -g|--gender)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pGENDER="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 22
      fi
      ;;
    -b|--birthdate)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pBIRTHDATE="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 23
      fi
      ;;
    -a|--age)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pAGE="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 24
      fi
      ;;
    -d|--address)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pADDRESS="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 25
      fi
      ;;
    -p|--phone)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pPHONE="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 26
      fi
      ;;
    -e|--email)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pEMAIL="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 27
      fi
      ;;
    -u|--username)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pUSERNAME="$2"
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 28
      fi
      ;;
    -F|--dockercompose)
      if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
        pDOCKER_COMP="$2"
        shift 2
      else
        echo "-F not specified, taking default docker-compose file path..."
        pDOCKER_COMP="docker-compose.yaml"
      fi
      ;;
    -C|--clear)
      pCLEAR="TRUE"
      shift
      ;;
    -D|--debug)
      pDEBUG="TRUE"
      shift
      ;;
    -h|--help)
      usage_full
      exit 11
      ;;
    -v|--version)
      echo "${SCRIPT_NAME} ${VERSION}"
      exit 12
      ;;
    *)
      echo "Error: Unknown argument '$1'" >&2
      exit 99
      ;;
  esac
done

# -----------------------------------------------------------------------------------------------------------------
# Control Argument

if [ "${pCLI}" == "" ] && [ "${pGUI}" == "" ] && [ "${pHELP}" == "" ]; then
  echo " [*] ERROR: Please specify a mode 'gui' or 'cli' or ask for 'help'. Show usage with -h" >&2
  usage
  exit 50
fi
if [ "${pCLI}" == "TRUE" ] && [ "${pGUI}" == "TRUE" ]; then
  echo " [*] ERROR: 'cli' & 'gui' are incompatible" >&2
  usage
  exit 51
fi
if [ "${pGENDER}" ] && [ "${pGENDER}" != "male" ] && [ "${pGENDER}" != "female" ] && [ "${pGENDER}" != "None" ]; then
  echo " [*] ERROR: --gender option take value 'male' or 'female' only" >&2
  usage
  exit 52
fi
if [ "$pBIRTHDATE" ] && [[ "$pBIRTHDATE" != $(date -d "$pBIRTHDATE" "+%Y%m%d" 2>/dev/null) ]] && [ "${pGENDER}" != "None" ]; then
  echo " [*] ERROR: Please provide a valid date. Format: <YYYYMMDD>" >&2
  usage
  exit 53
fi

# check if docker-compose file exist
if [ ! -f "${pDOCKER_COMP}" ]; then
  echo " [*] ERROR: Docker file does not exist. Please specify it with -F" >&2
  usage
  exit 54
fi

CMD_LINE_SUMMARY="${SCRIPT_NAME} ${SCRIPT_ARGUMENTS}" # for log optionally
echo "Start - ${CMD_LINE_SUMMARY}"

# -----------------------------------------------------------------------------------------------------------------
# STEP-1: BUILD CORE COMMAND
# -----------------------------------------------------------------------------------------------------------------

# get project_name from path (direct parent directory name of docker-compose.yaml file)
# Docker image will be name according to this schema: '<project_name>_(gui|framework)'
typeset -r PROJECT_NAME=$(basename $(realpath ${pDOCKER_COMP} | xargs -I{} sh -c "dirname {}"))
typeset -r pFW_NAME="${PROJECT_NAME,,}_framework"
typeset -r pGUI_NAME="${PROJECT_NAME,,}_gui"

# -----------------------------------------------------------------------------------------------------------------
# Build options

args=()
if [[ -n $pLASTNAME ]] ; then args+=("--lastname $pLASTNAME") ; fi
if [[ -n $pFIRSTNAME ]] ; then args+=("--firstname $pFIRSTNAME") ; fi
if [[ -n $pGENDER ]] ; then args+=("--gender $pGENDER") ; fi
if [[ -n $pBIRTHDATE ]] ; then args+=("--birthdate $pBIRTHDATE") ; fi
if [[ -n $pAGE ]] ; then args+=("--age $pAGE") ; fi
if [[ -n $pADDRESS ]] ; then args+=("--address $pADDRESS") ; fi
if [[ -n $pPHONE ]] ; then args+=("--phone $pPHONE") ; fi
if [[ -n $pEMAIL ]] ; then args+=("--email $pEMAIL") ; fi
if [[ -n $pUSERNAME ]] ; then args+=("--username $pUSERNAME") ; fi

# -----------------------------------------------------------------------------------------------------------------
# Build command

OPSE_SCRIPT="python3 Opse.py"

# Debug mode
if [ "${pDEBUG}" == "TRUE" ]; then
  OPSE_SCRIPT="${OPSE_SCRIPT} -D"
fi

# CLI mode
if [ "${pCLI}" == "TRUE" ]; then
  OPSE_SCRIPT="${OPSE_SCRIPT} -R"

  # entry data
  OPSE_OPTIONS=$(
  for i in ${args[@]}; do
    printf "%q " "$i"
  done
  )

  OPSE_CMD="${OPSE_SCRIPT} ${OPSE_OPTIONS}"
fi

# GUI mode
if [ "${pGUI}" == "TRUE" ]; then
  OPSE_SCRIPT="${OPSE_SCRIPT} -A"
  OPSE_CMD="${OPSE_SCRIPT}"
fi

# -----------------------------------------------------------------------------------------------------------------
# STEP-2: DOCKER
# -----------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# STEP-2 Pre-stage - Stop already running image & clear image if asked

echo "[-] Stopping already running containers"
docker compose -f "${pDOCKER_COMP}" stop 2> /dev/null

# clear docker images 
if [ "${pCLEAR}" == "TRUE" ]; then
  echo "  [-] Clearing docker images..."
  if [[ "$(docker images -q ${pGUI_NAME} 2> /dev/null)" != "" ]]; then 
    docker image rm --force "${pGUI_NAME}" $1> /dev/null
  fi
  if [[ "$(docker images -q ${pGUI_NAME} 2> /dev/null)" != "" ]]; then 
    docker image rm --force "${pGUI_NAME}" $1> /dev/null
  fi
fi

# -----------------------------------------------------------------------------------------------------------------
# STEP-2.1: CLI MODE

if [ "${pCLI}" == "TRUE" ]; then
  echo "1-Entering CLI mode
  [-] Starting CORE..."

  # ----- BUILD CORE -----
  if [[ "$(docker images -q ${pGUI_NAME} 2> /dev/null)" == "" ]]; then 
    docker compose -f "${pDOCKER_COMP}" build --force-rm -q -- framework
  fi

  # ----- RUN CORE -----
  docker compose -f "${pDOCKER_COMP}" run framework ${OPSE_CMD}
fi

# -----------------------------------------------------------------------------------------------------------------
# STEP-2.2: GUI MODE

if [ "${pGUI}" == "TRUE" ]; then
  echo "1-Entering GUI mode
  [-] Starting CORE & WEBVIEW..."

  # ----- BUILD CORE & WEBVIEW -----
  list_images=$(docker images -q "${PROJECT_NAME}_*")
  declare -i images_count="${#list_images[@]}"
  if [[ "${images_count}" < "2" ]]; then 
    docker compose -f ${pDOCKER_COMP} build --force-rm -q
  fi

  # ----- RUN CORE -----
  docker compose -f ${pDOCKER_COMP} run -d framework ${OPSE_CMD}
  # ----- RUN WEBVIEW -----
  docker compose -f ${pDOCKER_COMP} up -d -- gui

  WEBSITE=http://localhost:8080/

  case "$OSTYPE" in
    # solaris*) echo "SOLARIS" ;;
    # darwin*)  echo "OSX" ;; 
    # linux*)   echo "LINUX" ;;
    # bsd*)     echo "BSD" ;;
    msys*)    explorer $WEBSITE ;;
    cygwin*)  explorer $WEBSITE ;;
    *)        open $WEBSITE ;;
  esac
fi

# -----------------------------------------------------------------------------------------------------------------
# STEP-X: DATA DELETION
# -----------------------------------x------------------------------------------------------------------------------
# sed -i "$(( $(wc -l <.env)-10+1 )),$ d" .env

# TODO: créer un moyen de stopper les dockers après les recherches
# truncate -s 0 .docker_names

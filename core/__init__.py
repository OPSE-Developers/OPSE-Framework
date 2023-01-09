import importlib.util
import os
import sys

ENDC = "\033[0m"
ERRO = "\033[91m"
GREE = "\033[92m"
WARN = "\033[93m"

YES = [True, 'Yes', 'yes', 'y', 'True', 'true', '1']
NOP = [False, 'No', 'no', 'n', 'False', 'false', '0']

# Check if python module pip is installed
pip_is_present: bool = importlib.util.find_spec('pip')
if not pip_is_present:
    print(ERRO + "[X] " + ENDC, end='')
    print("pip is not installed")
else:
    print(GREE + "[V] " + ENDC, end='')
    print("pip is installed")

# Check if python packages requirements are installed
# Get pip user's packages
import pkg_resources
installed_packages = pkg_resources.working_set
lst_available_packages = sorted(["%s" % (i.key) for i in installed_packages])

# Check if requirements are present
requirements_file = open("requirements.txt", "r")
data = requirements_file.read()
required_packages = data.split("\n")
requirements_file.close()

# Check if plugins' requirements are present
lst_requirements = []
lst_plugins_dir = os.scandir("./core/tools")
for plugin_dir in lst_plugins_dir:
    if os.path.isdir(plugin_dir):
        reqs_path = os.path.join(plugin_dir, "requirements.txt")
        if os.path.isfile(reqs_path):
            requirements_file = open(reqs_path, "r")
            data = requirements_file.read()
            sub_reqs = data.split("\n")
            requirements_file.close()
            for sub_r in sub_reqs:
                if sub_r not in lst_requirements:
                    lst_requirements.append(sub_r)

required_packages.extend(lst_requirements)

lst_missing_packages: list = []
for pkg in required_packages:
    if pkg not in lst_available_packages:
        print(ERRO + "[X] " + ENDC, end='')
        print(pkg +" is not installed")
        lst_missing_packages.append(pkg)
    else:
        print(GREE + "[V] " + ENDC, end='')
        print(pkg +" is installed")

lst_missing_packages.sort()

# If there are missing packages, ask to install them
if not pip_is_present or lst_missing_packages:
    print(ERRO + "\nRequirements are not met.\n" + ENDC)
    valid: bool = False
    while not valid:
        try:
            response = input("Would you like to install them? [y/N] ")
        except KeyboardInterrupt:
            print()
            exit()
        valid = (response in YES or response in NOP) or not (response == '\n')
    
    if response in YES:
        from subprocess import call, DEVNULL, STDOUT

        # Redirect stdout and stderr // avoid display
        old_stdout, old_stderr = sys.stdout, sys.stderr

        DCT_NUL_PTR: dict = {
            'linux': '/dev/null',
            'win32': 'nul',
            'darwin': '/dev/null'
        }
        nul_ptr: str = DCT_NUL_PTR.get(sys.platform)

        if nul_ptr is None:
            print(ERRO + "Please install requirements before running this script." + ENDC)
            exit(-1)

        sys.stdout, sys.stderr = open(nul_ptr, 'w'), open(nul_ptr, 'w')

        # === Install pip
        if not pip_is_present:
            import urllib.request
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
            call(["python3", "get-pip.py"], stdout=DEVNULL, stderr=STDOUT)
            # Clean up now...
            os.remove("get-pip.py")

        # === Install missing plugins
        if lst_missing_packages:
            from pip._internal.cli.main import main as pipmain
            args = ['install', '-q', '--disable-pip-version-check', '--no-python-version-warning']
            args.extend(lst_missing_packages)
            pipmain(args)

        # === Installation finished

        # Restore display
        sys.stdout, sys.stderr = old_stdout, old_stderr

        print(GREE + "Requirements installation succeed!" + ENDC)

    else:
        print(ERRO + "Can't run with missing packages." + ENDC)
        exit(-1)
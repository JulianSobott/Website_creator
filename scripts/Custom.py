"""
@author: Julian Sobott
@created: 18.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import sys
import subprocess

from Logging import logger
import Paths

from CMD import intersects, get_optional_parameter


DESCRIPTION = (
    "\n"
    "Custom.py Init:\n"
    "This script makes it possible to use custom scripts.\n"
    "Add your functionality to your Custom.py file.\n"
    "Append your additional arguments to this call.\n"
    "Only {additional_args} are forwarded to the custom script.\n"
    "  req -c {additional_args}"
    "\n"
    )


def handle_sys_arguments(all_args):
    help_arg = ["--help", "-h", "?"]
    if intersects(help_arg, all_args) or len(all_args) <= 1:
        print_help()
        exit(0)

    custom_args = [Paths.Website.ABS_CUSTOM_SCRIPT_PATH]
    custom_args += all_args[1:]
    print(custom_args)
    subprocess.run(custom_args, shell=True)




def print_help():
    print(DESCRIPTION)


if __name__ == "__main__":
    p_num_args = len(sys.argv) - 1
    p_all_args = []
    if p_num_args > 0:
        p_all_args = sys.argv[1:]
    handle_sys_arguments(p_all_args)

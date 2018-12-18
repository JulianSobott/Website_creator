"""
@author: Julian Sobott
@created: 18.12.2018
@brief: User interface, to process custom cmd inputs
@description:
This script only handles the first sys argument and forwards then all args to the corresponding script

@external_use:

@internal_use:

Add custom argument:
    Add to DESCRIPTION
    Add to handle_sys_arguments
    Handle on intersect

"""
import sys

DESCRIPTION = (
    "custom.py\n"
    "Following arguments are available:\n\n"
    "  --help, -h, ?: prints help.\n"
    "ADD CUSTOM ARGUMENTS HERE"
    "\n"
)


def handle_sys_arguments(all_args):
    help_arg = ["--help", "-h", "?"]
    # Add custom arguments here
    num_args = len(all_args)
    if num_args <= 1:
        print_help()
        exit(0)

    if intersects(help_arg, list(all_args[0])):
        print_help()
        exit(0)


def print_help():
    print(DESCRIPTION)


def intersects(l1, l2):
    return len(list(set(l1) & set(l2))) > 0


def get_optional_parameter(parameter_names: list, all_arguments: list):
    """optional parameters are arguments which are set with [parameter]=[value]"""
    for argument in all_arguments:
        for parameter_name in parameter_names:
            if parameter_name in argument:
                if "=" in argument:
                    return argument.split("=")[1]

    return None


if __name__ == "__main__":
    p_num_args = len(sys.argv) - 1
    p_all_args = []
    if p_num_args > 0:
        p_all_args = sys.argv[1:]
    handle_sys_arguments(p_all_args)


"""
@author: Julian Sobott
@created: 13.12.2018
@brief: User interface, to process cmd inputs
@description:
This script only handles the first sys argument and forwards then all args to the corresponding script

@external_use:

@internal_use:

"""
import sys

from Logging import logger
import Project_templates
import Template_parser
import Setup
import Data_parser
import Custom
import Release
import FileWatcher
from CMD import intersects, get_optional_parameter


DESCRIPTION = (
    "req.py\n"
    "This tool advances the workflow of creating websites.\n"
    "To view a more detailed description about the tools type: --[argument] --help\n" 
    "arguments inside '{}' are optional\n"
    "Following arguments are available:\n\n"
    "  --help, -h, ?: prints help.\n"
    "  init {template=[template_name]}: Initializes inside an empty folder a new project\n" 
    "  --templates name=[template_name] {r, repl_f=[replaceables]}: "
               "Create all files and folders defined in templates.json\n"
    "  --parse-data {path=[json_src_path]}: Parses all data to html, defined in json_src_path\n"
    "  --custom, -c {args}: Calls self defined functions in folder Scripts"
    "\n"
)


def print_help():
    print(DESCRIPTION)


if __name__ == "__main__":
    help_arg = ["--help", "-h", "?"]
    init_arg = ["init", "--init"]
    templates_arg = ["--templates"]
    parse_data_arg = ["--parse-data"]
    custom_arg = ["--custom", "-c"]
    release_arg = ["--release", "-r"]
    auto_release_arg = ["--auto-release", "-ar"]

    print("")

    num_args = len(sys.argv) - 1
    all_args = []
    if num_args > 0:
        all_args = sys.argv[1:]
    else:
        print_help()
        exit(0)

    if intersects(help_arg, list(all_args[0])):
        print_help()
        exit(0)

    if intersects(init_arg, all_args):
        Setup.handle_sys_arguments(all_args)

    elif intersects(parse_data_arg, all_args):
        Data_parser.handle_sys_arguments(all_args)

    elif intersects(templates_arg, all_args):
        Template_parser.handle_sys_arguments(all_args)
    elif intersects(custom_arg, all_args):
        Custom.handle_sys_arguments(all_args)
    elif intersects(release_arg, all_args):
        Release.handle_sys_arguments(all_args)
    elif intersects(auto_release_arg, all_args):
        FileWatcher.handle_sys_arguments(all_args)
    else:
        print_help()

    print("")


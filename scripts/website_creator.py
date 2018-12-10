"""
@author: Julian Sobott
@created: 09.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import sys

from Logging import logger
import Project_templates
import Template_parser
import Paths

DESCRIPTION = \
    __file__ + "\n"\
    "This tool advance the workflow of creating websites\n" \
    "Following arguments are available:\n\n"\
    "  --help, -h, ?:\tprints help.\n" \
    "  init [template=[template_name]]: Initializes inside an empty folder a new project\n" \
               "\t\toptionally name the template name\n" \
               "\t\t[template=?: To view all available project templates\n" \
    "  --templates [--help, -h, ?]: To get a more detailed description about templates\n" \
               "\t+ [template_name]: Create all files and folders defined in templates.json\n" \
               "\t+ [replacements]: Either a path to a .json file with replacements, or a string in json format\n"\
    \
    "\n"

"""Public functions"""


def init(template="default", website_name=None):
    Project_templates.create_from_template(template, website_name)


def templates(show_structure=False):
    Project_templates.print_templates(show_structure)
    print("Type --templates --structure to view also their structure")


""" Helper functions"""


def reset():
    import os
    import shutil
    reset_content = input("Do you really want to delete content of: %s (yes/no)" % Paths.Website.PROJECT_PATH)
    if reset_content == "yes":
        for the_file in os.listdir(Paths.Website.PROJECT_PATH):
            file_path = os.path.join(Paths.Website.PROJECT_PATH, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


def print_help():
    print(DESCRIPTION)


def print_init_help():
    pass    # TODO


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
    """DEBUG Area"""
    reset_arg = ["reset"]
    #init()

    #exit(0)
    """End"""
    help_arg = ["--help", "-h", "?"]
    init_arg = ["init", "--init"]
    opt_template_arg = ["template"]
    opt_website_name_arg = ["name"]
    templates_arg = ["--templates"]

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
        if intersects(help_arg, all_args):
            print_init_help()
            exit(0)
        p_template = get_optional_parameter(opt_template_arg, all_args)
        p_website_name = get_optional_parameter(opt_website_name_arg, all_args)
        opt_args = {}
        if p_template == "?":
            Project_templates.print_templates()
            exit(0)
        elif p_template:
            opt_args["template"] = p_template
        if p_website_name:
            opt_args["website_name"] = p_website_name
        init(**opt_args)

    if intersects(templates_arg, all_args):
        Template_parser.console_input(all_args)

    """DEBUG"""
    if intersects(reset_arg, all_args):
        reset()

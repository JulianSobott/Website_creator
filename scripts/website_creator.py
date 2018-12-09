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
import Paths

DESCRIPTION = \
    __file__ + "\n"\
    "This tool advance the workflow of creating websites\n" \
    "Following arguments are available:\n\n"\
    "  --help, -h, ?:\tprints help.\n" \
    "  init [template=[template_name]]: Initializes inside an empty folder a new project\n" \
               "\t\toptionally name the template name\n" \
               "\t\tTo view all available templates type --templates\n"\
    \
    "\n"

"""Public functions"""


def init(template="default", website_name=None):
    Project_templates.create_project_from_template(template, website_name)


def templates(show_structure=False):
    Project_templates.print_templates(show_structure)
    print("Type --templates --structure to view also their structure")


""" Helper functions"""


def reset(reset_all=False):
    import os
    import shutil
    if reset_all:
        reset_path = Paths.WEBSITE_PROJECT_PATH
    else:
        reset_path = Paths.WEBSITE_RELEASE_PATH
    reset_it = input("Do you really want to delete content of: %s (yes/no)" % reset_path)
    if reset_it == "yes":
        for the_file in os.listdir(reset_path):
            file_path = os.path.join(reset_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


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
    """DEBUG Area"""
    reset_arg = ["reset"]
    reset_all_arg = ["reset_all"]
    #init()

    #exit(0)
    """End"""
    help_arg = ["--help", "-h", "?"]
    init_arg = ["init", "--init"]
    opt_template_arg = ["template"]
    opt_website_name_arg = ["name"]
    templates_arg = ["--templates"]
    templates_structure_arg = ["--structure"]

    num_args = len(sys.argv) - 1
    if num_args > 0:
        all_args = sys.argv[1:]
    else:
        print_help()
        exit(0)

    if intersects(help_arg, all_args):
        print_help()
        exit(0)

    if intersects(init_arg, all_args):
        p_template = get_optional_parameter(opt_template_arg, all_args)
        p_website_name = get_optional_parameter(opt_website_name_arg, all_args)
        opt_args = {}
        if p_template:
            opt_args["template"] = p_template
        if p_website_name:
            opt_args["website_name"] = p_website_name
        init(**opt_args)

    if intersects(templates_arg, all_args):
        if intersects(templates_structure_arg, all_args):
            p_show_structure = True
        else:
            p_show_structure = False
        templates(p_show_structure)

    """DEBUG"""
    if intersects(reset_arg, all_args):
        reset()
    if intersects(reset_all_arg, all_args):
        reset(reset_all=True)

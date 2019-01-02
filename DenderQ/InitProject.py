"""
@author: Julian Sobott
@created: 09.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import sys
import os

from Logging import logger
import Project_templates
import Template_parser
import Paths
import Data_parser
from CMD import intersects, get_optional_parameter


DESCRIPTION = (
    "\n"
    "InitProject.py Init:\n"
    "This tool initializes the project folder.\n"
    "To init a new project follow these steps:\n"
    "  1. Create an empty folder and cd to it\n"
    "  2. Type:\n"
    "\tinit t=[template_name] {name=[website_name]}\n"
    "  3. When everything was created successfully go to your projects dev folder and start your website.\n\n"
               
    "Following additional arguments are available:\n"
    "  --help, -h, ?: prints help.\n"
    "  {template=[template_name]}: If you want another project structure than default, specify the name.\n"
    "\tSet template_name to '?' to view all available templates\n"
    "  {--structure}: Shows the detailed templates structures, when template_name is '?'\n"
    "  {name=[website_name]}: To set in some files automatically the website name"
    "  {root=[full_project_path]}: Sets, root folder of the project (folder should be empty or non existing)\n"
    "\n"
    )

"""Public functions"""


def init(template="default", website_name=None, root_path=None):
    if root_path:
        os.makedirs(root_path, exist_ok=True)
        os.chdir(root_path)
        Paths.update()
    Project_templates.create_from_template(template, website_name)


""" Helper functions"""


def handle_sys_arguments(all_args):
    help_arg = ["--help", "-h", "?"]
    templates_structure_arg = ["--structure"]
    opt_template_arg = ["template", "t"]
    opt_website_name_arg = ["name"]
    opt_root_path_arg = ["root"]
    if intersects(help_arg, all_args) or len(all_args) == 1:
        print_help()
        exit(0)

    p_template = get_optional_parameter(opt_template_arg, all_args)
    p_website_name = get_optional_parameter(opt_website_name_arg, all_args)
    opt_args = {}
    if p_template == "?":
        if intersects(templates_structure_arg, all_args):
            structure = True
        else:
            structure = False
        Template_parser.print_templates(Paths.Tool.ABS_TEMPLATES_JSON_PATH, structure)
        exit(0)
    elif p_template:
        opt_args["template"] = p_template
    if p_website_name:
        opt_args["website_name"] = p_website_name
    p_root_path = get_optional_parameter(opt_root_path_arg, all_args)
    if p_root_path:
        p_root_path = p_root_path.replace("\\", "/")
        opt_args["root_path"] = p_root_path
    init(**opt_args)


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


if __name__ == "__main__":
    help_arg = ["--help", "-h", "?"]
    num_args = len(sys.argv) - 1
    all_args = []
    if num_args > 0:
        all_args = sys.argv[1:]
    else:
        print_help()
        exit(0)

    if intersects(help_arg, all_args) or len(all_args) == 0:
        print_help()
        exit(0)

    else:
        all_args.append("--init")
        handle_sys_arguments(all_args)

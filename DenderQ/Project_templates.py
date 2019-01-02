"""
@author: Julian Sobott
@created: 09.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import os

from Logging import logger
import Paths
import Template_parser


def create_from_template(template_name, website_name):
    templates = Template_parser.get_all_templates(Paths.Tool.ABS_TEMPLATES_JSON_PATH)
    template = templates[template_name]
    if len(os.listdir(Paths.Website.PROJECT_PATH)) > 0:
        logger.debug("Dir is not empty: (%s)", Paths.Website.PROJECT_PATH)
        # continue_input = input("WARNING: The folder you are currently in is not empty!\n"
        #                       "Continue anyway (No files are deleted)? (y/n)\n")
        # if continue_input != 'y':
        #    exit(-1)
    replacements = {"website_name": website_name, "project_path": Paths.Website.PROJECT_PATH}
    Template_parser.create_recursively(template, Paths.Website.PROJECT_PATH, replacements,
                                       "", Paths.Tool.ABS_TEMPLATES_PATH)
    print("Successfully created new project.")

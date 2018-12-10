"""
@author: Julian Sobott
@created: 09.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import json
import os
import shutil

from Logging import logger
import Paths


def create_from_template(template_name, website_name):
    templates = get_all_templates()
    template = templates[template_name]
    create_recursively(template, Paths.Website.PROJECT_PATH)


def create_recursively(json_data, root_path):
    """Creates recursively all files and folders defined in json data
    json data structure:
        keys are folder_name or file_name
        values are either:
            src_file_path (when key is file)
            child folder names
    """
    for entry in json_data.keys():
        name, extension = os.path.splitext(entry)
        if len(extension) == 0:
            dir_path = os.path.join(root_path, name)
            try:
                os.mkdir(dir_path)
            except FileExistsError as e:
                logger.warning(e)
            create_recursively(json_data[entry], dir_path)
        else:
            src_path = json_data[entry]
            abs_dest_path = os.path.join(root_path, entry)
            if len(src_path) > 0:
                abs_src_path = os.path.join(Paths.Tool.ABS_TEMPLATES_PATH, src_path)
                try:
                    shutil.copy2(abs_src_path, abs_dest_path)
                except FileNotFoundError as e:
                    logger.warning(e)
            else:
                with open(abs_dest_path, "w+"):
                    pass


def get_all_templates():
    with open(Paths.Tool.ABS_TEMPLATES_JSON_PATH, "r") as templates_file:
        templates = json.load(templates_file)
    return templates


def print_templates(show_structure=False):
    if show_structure:
        with open(Paths.Tool.ABS_TEMPLATES_JSON_PATH, "r") as templates_file:
            print(templates_file.read())
    else:
        templates = get_all_templates()
        print(list(templates.keys()))



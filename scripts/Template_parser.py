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
import re

import Paths
from Logging import logger

__all__ = ["create_from_template"]


def create_from_template(template_name, replacements={}):
    template = get_template(template_name)
    root_path = Paths.Website.ABS_DEV_PATH
    create_recursively(template["Structure"], root_path, replacements, template_name)


def create_recursively(json_data, root_path, replacements, template_name):
    logger.debug("%s\n%s\n%s", str(json_data), root_path, str(replacements))

    for entry in json_data.keys():
        name, extension = os.path.splitext(entry)
        name = replace_placeholders(name, replacements)
        if len(extension) == 0:
            dir_path = os.path.join(root_path, name)
            try:
                os.mkdir(dir_path)
            except FileExistsError as e:
                logger.warning(e)
            create_recursively(json_data[entry], dir_path, replacements, template_name)
        else:
            src_path = json_data[entry]
            abs_dest_path = os.path.join(root_path, name + extension)
            if len(src_path) > 0:
                abs_src_path = os.path.join(Paths.Website.ABS_TEMPLATES_PATH, template_name, src_path)
                try:
                    shutil.copy2(abs_src_path, abs_dest_path)   # TODO: replace replacements
                except FileNotFoundError as e:
                    logger.warning(e)
            else:
                with open(abs_dest_path, "w+"):
                    pass


def replace_placeholders(text, replacements):
    final_text = text
    for search_rex, replacer in replacements.items():
        final_text = re.sub(search_rex, replacer, final_text)
    logger.debug(final_text)
    return final_text


def get_template(name):
    all_templates = get_all_templates()
    return all_templates[name]


def get_all_templates():
    with open(Paths.Website.ABS_TEMPLATES_JSON_PATH, "r") as templates_file:
        templates = json.load(templates_file)
    return templates


if __name__ == '__main__':
    """DEBUG"""
    create_from_template("t1", {"site_name": "First_site"})

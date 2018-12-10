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
    templates_src_path = Paths.Website.ABS_TEMPLATES_PATH
    create_recursively(template["Structure"], root_path, replacements, template_name, templates_src_path)


def create_recursively(json_data: dict, root_path: str, replacements: dict, template_name: str, templates_src_path):
    for entry in json_data.keys():
        name, extension = os.path.splitext(entry)
        name = replace_placeholders(name, replacements, is_file_name=True)
        if len(extension) == 0:
            dir_path = os.path.join(root_path, name)
            try:
                os.mkdir(dir_path)
            except FileExistsError as e:
                logger.warning(e)
            create_recursively(json_data[entry], dir_path, replacements, template_name, templates_src_path)
        else:
            src_path = json_data[entry]
            abs_dest_path = os.path.join(root_path, name + extension)
            if len(src_path) > 0:
                abs_src_path = os.path.join(templates_src_path, template_name, src_path)
                try:
                    if len(replacements) > 0:
                        with open(abs_src_path, "r") as src_file:
                            src_text = src_file.read()
                        final_text = replace_placeholders(src_text, replacements)
                        with open(abs_dest_path, "w+") as dest_file:
                            dest_file.write(final_text)
                    else:
                        shutil.copy2(abs_src_path, abs_dest_path)
                except FileNotFoundError as e:
                    logger.warning(e)
            else:
                with open(abs_dest_path, "w+"):
                    pass


def replace_placeholders(text, replacements, is_file_name=False):
    """
    :param text
    :param replacements: dict with keys as search regex and values as replacements
    :param is_file_name: True replaces keys by values
                        False: replaces {key} by value (only occurrences with {key})"""
    final_text = text
    for search_rex, replacer in replacements.items():
        if not is_file_name:
            search_rex = "{" + search_rex + "}"
        final_text = re.sub(search_rex, replacer, final_text)
    return final_text


def get_template(name):
    all_templates = get_all_templates(Paths.Website.ABS_TEMPLATES_JSON_PATH)
    return all_templates[name]


def get_all_templates(full_json_path):
    with open(full_json_path, "r") as templates_file:
        templates = json.load(templates_file)
    return templates


def read_replacements_file(file_path):
    try:
        with open(file_path, "r") as replacements_file:
            replacements = json.load(replacements_file)
    except FileNotFoundError:
        return {}
    return replacements


def print_templates(full_json_path, show_structure=False):
    if show_structure:
        with open(full_json_path, "r") as templates_file:
            print(templates_file.read())
    else:
        templates = get_all_templates(full_json_path)
        print(list(templates.keys()))


def print_templates_help():
    help_text = ("Templates are an easy way to fasten your creation of file structures.\n"
                 "You can define a new template in templates.json\n"
                 "For more information about creating templates view the docs.\n"
                 "To create from an existing: Type --templates with following arguments:\n"
                 "\tname, t =[template_name]: Where [template_name] is the name defined in templates.json\n"
                 "\trepl_f, replace_file=[json_file_path]: [json_file_path] "
                 "is a path to a json file with the replacements\n"
                 "\tr, repl_s, replace_string=[replace_string]: [replace_string] is a json formatted string\n"
                 "\tNOTE: the replacement argument is optional\n\n"
                 "Following templates are available:")
    print(help_text)
    print_templates(Paths.Website.ABS_TEMPLATES_JSON_PATH)
    print("Type --templates --structure: To view the detailed structure of all templates")


def console_input(all_args):
    help_arg = ["--help", "-h", "?"]
    opt_template_name_arg = ["name", "t"]
    opt_template_replacements_file_arg = ["repl_f", "replace_file"]
    opt_template_replacements_string_arg = ["r", "repl_s", "replace_string"]
    templates_structure_arg = ["--structure"]

    if intersects(help_arg, all_args) or len(all_args) == 1:
        print_templates_help()
        exit(0)

    if intersects(templates_structure_arg, all_args):
        print_templates(Paths.Website.ABS_TEMPLATES_JSON_PATH, True)
        exit(0)
    p_template_name = get_optional_parameter(opt_template_name_arg, all_args)

    all_templates = get_all_templates()
    if p_template_name not in all_templates.keys():
        print("ERROR: Please enter a valid template name! (name=...)")
        print("Choose one of the following: ", end="")
        print_templates(Paths.Website.ABS_TEMPLATES_JSON_PATH)
        exit(0)

    p_template_replacements_string = get_optional_parameter(opt_template_replacements_string_arg, all_args)
    p_template_replacements_file = get_optional_parameter(opt_template_replacements_file_arg, all_args)

    replacements = {}
    if p_template_replacements_file:
        replacements = read_replacements_file(p_template_replacements_file)
    elif p_template_replacements_string:
        json_valid_string = p_template_replacements_string.replace("'", "\"")
        try:
            replacements = json.loads(json_valid_string)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            replacements = ""

    if not isinstance(replacements, dict) and p_template_replacements_string is not None:
        print("ERROR: Please enter a valid replacement string or a file with valid json! (r=..., repl_f=...)")
        print("String must be in json format. Keys are the replace regex and values are the replacements")
        exit(0)

    create_from_template(p_template_name, replacements)


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


if __name__ == '__main__':
    """DEBUG"""
    create_from_template("t2", {"tutorial_name": "Python"})

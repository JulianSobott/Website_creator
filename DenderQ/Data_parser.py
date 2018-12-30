"""
@author: Julian Sobott
@created: 13.12.2018
@brief: Parses Data to HTML
@description:

@external_use:

@internal_use:

"""
import json
import os
import sys
import shutil

from Logging import logger
import Paths
from CMD import intersects, get_optional_parameter

DESCRIPTION = (
    "\nData_parser.py Parses data to html:\n"
    "This tool is used to separate data from html.\n"
    "To do so define your data in a json file. "
    "Where each key is the name of the string that is replaced by its value.\n"
    "e.g. html: <h1>{String1}</h1> + json: {\"String1\": \"Replaced String1\"} ==> <h1>Replaced String1</h1>\n"
    "When you added already all paths to parse in the file: '" + Paths.Website.ABS_DEFAULT_SRC_JSON_PATH + "'\n"
    "no further arguments are needed.\n"
    "If you have another file_path add:\n"
    "  {path=[file_path]}\n"
)


def parse_json_to_html(json_file_path, template_html_path, html_file_path):
    """JSON data: Key is the string that is replaced by its Value
    e.g. html: <h1>{String1}</h1> + json: {"String1": "Replaced String1"} ==> <h1>Replaced String1</h1>"""
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    with open(template_html_path, "r") as gen_html_file:
        gen_html_text = "".join(gen_html_file.readlines())

    filled_html_text = create_final_html(gen_html_text, data)
    #filled_html_text = gen_html_text.format(**data)

    directory = os.path.split(html_file_path)[0]
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(html_file_path, "w+") as filled_html_file:
        filled_html_file.write(filled_html_text)
    print("New file created: " + html_file_path)


def create_final_html(gen_html, replaceables):
    from HTML_compiler.EXE_HTML import parse_executable_html
    html = parse_executable_html(gen_html, replaceables)
    return html


def parse_executable_html(code, replaceables):
    pass

def execute_parser(src_json_file_path):
    """File structure: (All paths are relative to dev folder)
    {
        "python_tutorial": ["json file path", "html template path", "destination html file"],
        "...": ["...", "...", "..."]
    }
    """
    try:
        with open(src_json_file_path, "r") as src_json_file:
            logger.debug(src_json_file_path)
            data = json.load(src_json_file)
    except FileNotFoundError:
        print("ERROR: File %s does not exist! Please create this file or specify a path: path=..." % src_json_file_path)
        exit(-1)

    for parse_name, parse_paths in data.items():
        p_json_file_path = os.path.join(Paths.Website.ABS_DEV_PATH, parse_paths[0])
        p_template_html_path = os.path.join(Paths.Website.ABS_DEV_PATH, parse_paths[1])
        p_html_file_path = os.path.join(Paths.Website.ABS_DEV_PATH, parse_paths[2])
        parse_json_to_html(p_json_file_path, p_template_html_path, p_html_file_path)


def print_help():
    print(DESCRIPTION)


def handle_sys_arguments(all_args):
    opt_parse_data_path_arg = ["path", "--path"]
    help_arg = ["--help", "-h", "?"]
    if intersects(help_arg, all_args):
        print_help()
        exit(0)

    json_src_path = get_optional_parameter(opt_parse_data_path_arg, all_args)
    if json_src_path is None:
        json_src_path = Paths.Website.ABS_DEFAULT_SRC_JSON_PATH
    execute_parser(json_src_path)


if __name__ == '__main__':
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
        all_args.append("--parse-data")
        handle_sys_arguments(all_args)

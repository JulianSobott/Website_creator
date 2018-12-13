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

from Logging import logger
import Paths


def parse_json_to_html(json_file_path, template_html_path, html_file_path):
    """JSON data: Key is the string that is replaced by its Value
    e.g. html: <h1>{String1}</h1> + json: {"String1": "Replaced String1"} ==> <h1>Replaced String1</h1>"""
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    with open(template_html_path, "r") as gen_html_file:
        gen_html_text = "".join(gen_html_file.readlines())

    filled_html_text = gen_html_text.format(**data)

    with open(html_file_path, "w+") as filled_html_file:
        filled_html_file.write(filled_html_text)
    print("New file created: " + html_file_path)


def execute_parser(src_json_file_path):
    try:
        with open(src_json_file_path, "r") as src_json_file:
            data = json.load(src_json_file)
    except FileNotFoundError:
        print("ERROR: File %s does not exist! Please create this file or specify a path: path=..." % src_json_file_path)
        exit(-1)

    for parse_name, parse_paths in data.items():
        p_json_file_path = os.path.join(Paths.Website.ABS_DEV_PATH, parse_paths[0])
        p_template_html_path = os.path.join(Paths.Website.ABS_DEV_PATH, parse_paths[1])
        p_html_file_path = os.path.join(Paths.Website.ABS_DEV_PATH, parse_paths[2])
        parse_json_to_html(p_json_file_path, p_template_html_path, p_html_file_path)


if __name__ == '__main__':
    p_src_json_file_path = "E:\Programmieren\Websites\modular_website/TEST/dev/DATA/src_json.json"
    execute_parser(p_src_json_file_path)

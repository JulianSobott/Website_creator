"""
@author: Julian Sobott
@created: 21.12.2018
@brief: Build project to release
@description:
create_release() is the relevant method.
    copy all files except html and ignored files
    html files: check if export
    True: -> include all includes -> export
    False: -> ignore

@external_use:

To INCLUDE a html file add the following element inside your main html file
<include "[relative file path]">
(regex: <include\s\"([\w_\\\/.-]*.html)\">)
e.g.
<include "includes/navbar.html">

To add your html_file to the release add the following at the very top of your html file:
<export>

To INCLUDE a js file add the following element inside your main js file
#include "[relative file path]"
(regex: #include\s\"([\w_\\\/.-]*.js)\")
e.g.
#include "includes/navbar.js"

To add your js file to the release add the following at the very top of your js file:
#export

@internal_use:

"""
import os
import re
import sys
import shutil
import requests

from Logging import logger
from CMD import *
import Paths
import HTML_compiler.EXE_HTML

ENCODING = "utf-8"

DESCRIPTION = (
    "Release.py\n"
    "This script creates/copies all relevant files into the release folder.\n" 
    "Following arguments are optional:\n\n"
    "  {src=[src_path]}: You can add a path relative to the dev path. Only files inside this paths are handled.\n"
    "\n\nIncluding and exporting js/html files:\n"
    "Note: Paths are by default relative to the dev folder!\n"
    "\tTo make them relative to the current file prepend './' to the path.\n"
    "\tPaths may not contain whitespaces!\n\n"
    "To INCLUDE a HTML file add the following element inside your main html file:\n"
    "\t<include \"[relative file path]\">\n"
    "To add your HTML file to the release add the following at the very top of your html file:\n"
    "\t<export>\n"
    "\n"
    "To INCLUDE a JS file add the following element inside your main js file:\n"
    "\t#include \"[relative file path]\"\n"
    "To add your JS file to the release add the following at the very top of your js file:\n"
    "\t#export")


include_html_rex = "<include\\s\"([\\w_\\\\\\/.-]*.html)\">"
export_html_rex = "<export>"
include_js_rex = "#include\\s\"([\\w_\\\\\\/.-]*.js)\""
export_js_rex = "#export"

IGNORE_EXTENSIONS = [".sass", ".bat"]
HTML_EXTENSIONS = [".html", ".htm"]
JS_EXTENSIONS = [".js"]
IMPORT_EXTENSIONS = HTML_EXTENSIONS + JS_EXTENSIONS

js_minimize_level = 0

error_occurred = False


def create_release(just_imports=False, clear_release_first=False, optimized_code=False, src_path=None):
    """
    copy all files except html and ignored files
    html files: check if export True: -> include_all_includes -> export
    False: ignore all other html files
    """
    if clear_release_first:
        clear_release()
    if optimized_code:
        global js_minimize_level
        js_minimize_level = 1

    root_folder = Paths.Website.ABS_DEV_PATH
    if src_path:
        root_folder = os.path.join(root_folder, src_path)

    for root, folders, files in os.walk(root_folder):
        for file_name in files:
            extension = os.path.splitext(file_name)[1]
            if extension not in IGNORE_EXTENSIONS and (not just_imports or extension in IMPORT_EXTENSIONS):
                file_path = os.path.join(root, file_name)
                handle_file(file_path, Paths.Website.PROJECT_PATH, extension)

    if not error_occurred:
        logger.info("Successfully released!")
    else:
        logger.info("Release may be incorrect! Check the error log.")


def clear_release():
    for the_file in os.listdir(Paths.Website.ABS_RELEASE_PATH):
        file_path = os.path.join(Paths.Website.ABS_RELEASE_PATH, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def handle_file(full_path, project_path, file_extension):
    destination_folder_path = os.path.split(dev_to_release_path(full_path, project_path))[0]
    if file_extension in IMPORT_EXTENSIONS:
        if is_export_file(full_path):
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)
            create_export_file(full_path, destination_folder_path, file_extension)
    else:
        copy_non_html_file(full_path, destination_folder_path)


def copy_non_html_file(full_path, destination_folder_path):
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)
    try:
        shutil.copy2(full_path, destination_folder_path)
    except shutil.SameFileError:
        pass


def is_export_file(full_file_path):
    """is export_rex at top of file"""
    export = False
    with open(full_file_path, "r", encoding=ENCODING) as file:
        first_line = file.readline()
        rex = export_html_rex if os.path.splitext(full_file_path)[1] in [".html", ".htm"] else export_js_rex
        if re.search(rex, first_line):
            export = True
    return export


def create_export_file(abs_file_path, destination_folder_path, file_extension):
    """Insert all includes and write the final content to the release file"""
    global error_occurred
    final_text = include_all_includes(abs_file_path)
    if file_extension in JS_EXTENSIONS:
        final_minimized_text = minimize_js(final_text, level=js_minimize_level)
        if not final_minimized_text:
            logger.warning("Compilation error in your js. Check your js file: %s", abs_file_path)
            error_occurred = True
            final_minimized_text = final_text
    else:
        final_minimized_text = final_text
        if file_extension in HTML_EXTENSIONS:
            final_minimized_text = HTML_compiler.EXE_HTML.parse_executable_html(final_minimized_text, {})
    file_name = os.path.split(abs_file_path)[1]
    final_file_path = os.path.join(destination_folder_path, file_name)
    try:
        with open(final_file_path, "w+", encoding=ENCODING) as final_file:
            final_file.write(final_minimized_text)
    except PermissionError:
        logger.error("Error writing file: %s\n\tEnsure that the file is nowhere else open", final_file_path)
        error_occurred = True


def include_all_includes(rel_file_path):
    global error_occurred
    if not os.path.isfile(rel_file_path):
        logger.error("ERROR: Included File does not exist: " + str(rel_file_path))
        error_occurred = True
        return ""

    final_text = ""
    folder_path = os.path.split(rel_file_path)[0]
    export_rex = export_html_rex if os.path.splitext(rel_file_path)[1] in [".html", ".htm"] else export_js_rex
    include_rex = include_html_rex if os.path.splitext(rel_file_path)[1] in [".html", ".htm"] else include_js_rex
    with open(rel_file_path, "r", encoding=ENCODING) as file:
        for line in file.readlines():
            if not re.search(export_rex, line):
                idx_start_line = 0
                occurrences = re.finditer(include_rex, line)
                for occurrence in occurrences:
                    idx_start_reg = occurrence.regs[0][0]
                    idx_end_reg = occurrence.regs[0][1]
                    final_text += line[idx_start_line:idx_start_reg]
                    idx_start_file = occurrence.regs[1][0]
                    idx_end_file = occurrence.regs[1][1]
                    include_file_path = line[idx_start_file:idx_end_file]
                    if include_file_path.startswith("./"):      # path is relative to file
                        include_file_path = include_file_path[2:]
                        os.chdir(os.path.join(Paths.Website.ABS_DEV_PATH, folder_path))
                        full_include_file_path = os.path.realpath(include_file_path)
                        os.chdir(Paths.Website.PROJECT_PATH)
                    else:       # path is relative to dev folder
                        full_include_file_path = os.path.join(Paths.Website.ABS_DEV_PATH, include_file_path)
                    final_text += include_all_includes(full_include_file_path)
                    idx_start_line = idx_end_reg
                final_text += line[idx_start_line:]
    return final_text


def dev_to_release_path(full_path, project_path):
    rel_file_path = os.path.relpath(full_path, Paths.Website.ABS_DEV_PATH)
    return os.path.join(Paths.Website.ABS_RELEASE_PATH, rel_file_path)


def minimize_js(js_text, level=0):
    """:param level
    0: simple fastest, but only removes whitespace and comments,
    1: medium simple + renames variables,
    2: advanced (could destroy code) medium + changes code (very slow)
    API link: https://developers.google.com/closure/compiler/docs/gettingstarted_api"""
    compression = ["WHITESPACE_ONLY", "SIMPLE_OPTIMIZATIONS", "ADVANCED_OPTIMIZATIONS"][level]
    url = "https://closure-compiler.appspot.com/compile"
    request = requests.post(url, data={"js_code": js_text, 'compilation_level': compression,
                                       'output_format': 'text', 'output_info': 'compiled_code'})
    minimized_text = request.text.rstrip('\n')
    if len(minimized_text) == 0:
        return False
    else:
        return minimized_text


def print_help():
    print(DESCRIPTION)


def handle_sys_arguments(all_args):
    help_arg = ["--help", "-h", "?"]
    named_src_folder_arg = ["src"]

    if intersects(help_arg, all_args):
        print_help()
        exit(0)

    src_folder = get_optional_parameter(named_src_folder_arg, all_args)
    create_release(src_path=src_folder)


if __name__ == "__main__":
    all_args = ["src=Web"]
    handle_sys_arguments(all_args)

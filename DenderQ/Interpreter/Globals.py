"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
import os

current_file_path = ""


def get_current_file_name():
    try:
        return os.path.split(current_file_path)[1]
    except IndexError:
        return current_file_path

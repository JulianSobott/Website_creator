"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
import os

from Error_handler import UndefinedIdentifier, add_error

current_file_path = ""


def get_current_file_name():
    try:
        return os.path.split(current_file_path)[1]
    except IndexError:
        return current_file_path


class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def add(self, identifier, var_type="default"):
        self.symbols[identifier.value] = None

    def set(self, identifier, value):
        self.symbols[identifier.value] = value

    def get(self, identifier):
        name = identifier.value
        try:
            return self.symbols[name]
        except KeyError:
            add_error(UndefinedIdentifier(name, get_current_file_name(), identifier.line, identifier.idx_start))

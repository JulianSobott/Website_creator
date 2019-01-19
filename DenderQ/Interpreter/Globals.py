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
from Logging import logger

current_file_path = ""
_file_write_buffer = ""


def get_current_file_name():
    try:
        return os.path.split(current_file_path)[1]
    except IndexError:
        return current_file_path


class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def add(self, identifier, value=None, var_type="default"):
        self.symbols[identifier.value] = value

    def set(self, identifier, value):
        self.symbols[identifier.value] = value

    def get(self, identifier):
        name = identifier.value
        try:
            return self.symbols[name]
        except KeyError:
            add_error(UndefinedIdentifier(name, get_current_file_name(), identifier.line, identifier.idx_start))

    def get_recursive(self, identifier):
        try:
            name = identifier.value
            try:
                return self.get_recursive(self.symbols[name])
            except KeyError:
                return identifier
        except AttributeError:
            return identifier

    def log_symbols(self):
        logger.debug(self.symbols)


symbolTable = SymbolTable()


def buffer_to_file(text):
    global _file_write_buffer   # FIXME: Remove globals
    _file_write_buffer += text


def write_buffer_to_file(file_path):
    with open(file_path, "w+") as file:
        file.write(_file_write_buffer)

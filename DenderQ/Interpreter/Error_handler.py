"""
@author: Julian Sobott
@created: 10.01.2019
@brief: Displays and handles parse errors
@description:

@external_use:

@internal_use:

"""

__all__ = ["add_error", "UnknownCharacterSequence", "MissingCharacter", "UndefinedIdentifier"]


class Error:

    def __init__(self, file_name, line, idx):
        self.file_name = file_name
        self.line = line
        self.idx = idx
        self.message = ""

    def print_(self):
        print("Error: " + self.message + f" In {self.file_name} Line: {self.line}:{self.idx}")


class UnknownCharacterSequence(Error):
    NAME = "UnknownCharacterSequence"

    def __init__(self, char_seq, file_name, line, idx):
        super().__init__(file_name, line, idx)
        self.char_seq = char_seq
        self.message = f"{self.NAME}: '{self.char_seq}' "


class MissingCharacter(Error):
    NAME = "MissingCharacter"

    def __init__(self, missing_char, file_name, line, idx):
        super().__init__(file_name, line, idx)
        self.missing_char = missing_char
        self.message = f"{self.NAME}: '{self.missing_char}' "


class UndefinedIdentifier(Error):
    NAME = "UndefinedVariable"

    def __init__(self, identifier_name, file_name, line, idx):
        super().__init__(file_name, line, idx)
        self.undefined_identifier = identifier_name
        self.message = f"{self.NAME}: '{self.undefined_identifier}'"


class Errors:

    errors = []

    @staticmethod
    def add(error: Error):
        Errors.errors.append(error)


def add_error(error: Error):
    Errors.add(error)
    error.print_()

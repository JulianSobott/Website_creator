"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
from . import Globals
from . import Tokenizer
from .Logging import logger
from . import Parser
from . import MathExpressions

__all__ = ["parse_file"]


def parse_file(in_file_path, out_file_path):
    Globals.current_file_path = in_file_path
    text = get_file_content(in_file_path)
    tokens = Tokenizer.create_tokens(text)
    code_block = Parser.create_abstract_code(tokens)
    code_block.execute()
    Globals.write_buffer_to_file()
    logger.debug(code_block)


def get_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()

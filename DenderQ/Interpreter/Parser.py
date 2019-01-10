"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
from .Logging import logger
from .Streams import TokenStream

__all__ = ["create_abstract_code"]


class CodeBlock:

    def __init__(self, token_stream: TokenStream):
        self.elements = []


class Constants:

    def __init__(self, tokens):
        pass

    def is_valid(self, tokens):
        pass


def create_abstract_code(tokens):
    token_stream = TokenStream(tokens)
    code_block = CodeBlock(token_stream)
    return code_block

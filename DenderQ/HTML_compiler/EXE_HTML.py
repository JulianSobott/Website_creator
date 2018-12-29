"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
from Logging import logger
from Token_generator import generate_tokens, tokens_2_str, example_code_01


def parse_executable_html(code, replaceables):
    tokens = generate_tokens(code)


if __name__ == '__main__':
    p_repl = {"children": ["1", "2"]}
    parse_executable_html(example_code_01, p_repl)

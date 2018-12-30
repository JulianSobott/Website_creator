"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
from Logging import logger
from Token_generator import generate_tokens, tokens_2_str, example_code_02
from Commands import tokens_2_commands


example_code_03 = (
    "\\{children\\}\n"
    "}\n"
)


def parse_executable_html(code, replaceables):
    tokens = generate_tokens(code)
    code_block = tokens_2_commands(tokens)
    html = code_block.to_html(replaceables)
    logger.debug(html)


if __name__ == '__main__':
    p_repl = {"children": ["Tom", "Anna"]}
    parse_executable_html(example_code_03, p_repl)

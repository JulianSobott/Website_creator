"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
from Logging import logger
from .Token_generator import generate_tokens
from .Commands import tokens_2_commands


example_code_04 = (
    "for i=0 to 99 {\n"
    "pass\n"
    "}\n"
)
example_code_03 = (
"""
var {i} = 0
<p>{i}</p>
"""
)


def parse_executable_html(code, replaceables):
    tokens = generate_tokens(code)
    code_block = tokens_2_commands(tokens)
    html = code_block.to_html(replaceables)
    # logger.debug(html)
    return html


if __name__ == '__main__':
    p_repl = {"children": ["Tom", "Anna"]}
    p_repl = {}
    parse_executable_html(example_code_03, p_repl)

"""
@author: Julian Sobott
@created: 29.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import re

from Logging import logger
from Token_generator import Token


class ForInLoop:

    def __init__(self, header_tokens, body_code_block):
        if header_tokens[2].type == Token.SIGN:
            self.has_counter = True
            self.counter_name = header_tokens[1].value
        else:
            self.has_counter = False
        if self.has_counter:
            self.object_name = header_tokens[3].value
        else:
            self.object_name = header_tokens[1].value
        self.list = header_tokens[-1]

        self.code_block = body_code_block

        self._current_idx = 0

    @staticmethod
    def is_valid_block(tokens):
        """Is valid (header): for {i}, object in list"""
        order_long = [(Token.KEYWORD, "for"), (Token.VARIABLE, "\\S*"), (Token.SIGN, ","), (Token.VARIABLE, "\\S*"),
                      (Token.KEYWORD, "in"), (Token.REPLACEABLE, "\\{\\S*\\}")]
        order_short = [(Token.KEYWORD, "for"), (Token.VARIABLE, "\\S*"), (Token.KEYWORD, "in"),
                       (Token.REPLACEABLE, "\\{\\S*\\}")]
        orders = [order_long, order_short]
        for order in orders:
            idx = 0
            is_valid = True
            for match in order:
                try:
                    token = tokens[idx]
                except IndexError:
                    break
                if not token.type == match[0] or not re.match(match[1], token.value):
                    is_valid = False
                    break
                idx += 1
            if is_valid:
                return True

    def to_html(self, replacements):
        html = ""
        if self.list.type == Token.REPLACEABLE:
            self.list = replacements[self.list.value[1:-1]]
        else:
            pass
        idx = 0
        for i in self.list:
            temp_replacements = replacements.copy()
            temp_replacements[self.object_name] = str(i)
            if self.has_counter:
                temp_replacements[self.counter_name] = str(idx)
            html += self.code_block.to_html(temp_replacements)
            idx += 1
        return html


class ForToLoop:
    pass


class IfStatement:
    pass


class Write:

    def __init__(self, tokens):
        self.tokens = tokens

    def to_html(self, replacements):
        html = ""
        idx_last_end = 0
        tokens_start = 0
        if self.tokens[0].value == ">>":
            tokens_start = 1
            idx_last_end = self.tokens[0].idx_columns[1] + 1
        for token in self.tokens[tokens_start:]:
            idx_start = token.idx_columns[0]
            fill_spaces = idx_start - idx_last_end - 1
            idx_last_end = token.idx_columns[1]
            for i in range(fill_spaces):
                html += " "
            if token.type == Token.REPLACEABLE:
                try:
                    key = token.value[1:-1]
                    html += replacements[key]
                except KeyError:
                    logger.error("Replacement not found!")
            elif token.type == Token.END_OF_LINE:
                html += "\n"
            else:
                html += str(token.value).replace("\\{", "{").replace("\\}", "}")
        html += "\n"
        return html

    @staticmethod
    def is_valid_block(tokens):
        """Is valid: No keywords or "<<" at beginning"""
        if len(tokens) == 0:
            return False
        if tokens[0].type == Token.SIGN and tokens[0].value == "<<":
            return True
        else:
            for token in tokens:
                if token.type == Token.END_OF_LINE:
                    break
                if token.type == Token.KEYWORD:
                    return False
        return True     # TODO: find way to validate?




class CodeBlock:
    def __init__(self, tokens):
        self.elements = []
        tokens = cut_outer_eols(tokens)
        first_token = tokens[0]
        if first_token.type == Token.KEYWORD:
            header_tokens, idx_end = get_header_tokens(tokens)
            body_tokens = get_body_tokens(tokens[idx_end:])
            body_code_block = CodeBlock(body_tokens)
            if ForInLoop.is_valid_block(header_tokens):
                for_in_block = ForInLoop(header_tokens, body_code_block)
                self.elements.append(for_in_block)
        else:
            code_block = get_body_tokens(tokens)
            if Write.is_valid_block(code_block):
                writer = Write(code_block)
                self.elements.append(writer)
                logger.debug(writer)

    def to_html(self, replacements):
        html = ""
        for element in self.elements:
            html += element.to_html(replacements)
        return html


def cut_outer_eols(tokens):
    if len(tokens) == 0:
        return tokens
    if tokens[0].type == Token.END_OF_LINE:
        tokens = tokens[1:]
    if tokens[-1].type == Token.END_OF_LINE:
        tokens = tokens[:-1]
    return tokens


def get_proper_for_loop_class(tokens):
    """Starting at the first token in tokens. Checks whether, there is a "in" or "to" keyword"""
    for token in tokens:
        if token.type == Token.END_OF_LINE:
            break
        if token.value == "in":
            return ForInLoop
        if token.value == "to":
            return ForToLoop


def get_body_tokens(tokens):
    """Returns a list with all tokens, that belongs to the current block"""
    num_open_brackets = 0
    block_tokens = []
    tokens = cut_outer_eols(tokens)
    if tokens[0].value == "{":
        is_in_brackets = True
    else:
        is_in_brackets = False
    for token in tokens:
        ignore_token = False
        if token.value == "{":
            if not is_in_brackets:
                break
            if num_open_brackets == 0:
                ignore_token = True
            num_open_brackets += 1
        if token.value == "}":
            num_open_brackets -= 1
            if num_open_brackets == 0:
                ignore_token = True
        if not ignore_token:
            block_tokens.append(token)
        if num_open_brackets == 0 and is_in_brackets:
            break
    clean_block_tokens = cut_outer_eols(block_tokens)
    return clean_block_tokens


def get_header_tokens(tokens):
    header_tokens = []
    idx = 0
    for token in tokens:
        if token.value == "{":
            return header_tokens, idx
        else:
            header_tokens.append(token)
        idx += 1
    return header_tokens, idx


def tokens_2_commands(tokens):
    code_block = CodeBlock(tokens)
    return code_block

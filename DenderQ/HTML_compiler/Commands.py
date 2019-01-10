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
from .Token_generator import Token, tokens_2_code


def is_valid_grammar(order, tokens):
    if len(order) != len(tokens):
        return False
    idx = 0
    for match in order:
        try:
            token = tokens[idx]
        except IndexError:
            return False
        if not token.type == match[0]:
            return False
        re_match = re.match(match[1], token.value)
        if not re_match or re_match.endpos < len(token.value):
            return False
        idx += 1
    return True


class ForInLoop:
    """
    for i, object in list {...}/
    for object in list {...}
    """
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
            if is_valid_grammar(order, tokens):
                return True
        return False

    def to_html(self, replacements):
        html = ""
        if self.list.type == Token.REPLACEABLE:
            try:
                self.list = replacements[self.list.value[1:-1]]
            except KeyError:
                key = str(self.list.value[1:-1])
                error_text = f"Key error! unknown key: '{key}' in replacements\n"
                logger.error(key)
                return error_text
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
    """for i=start to end {...}"""
    def __init__(self, header_tokens, body_code_block):
        self.counter_name = header_tokens[1].value
        self.start_value = int(header_tokens[3].value)
        self.end_value = int(header_tokens[5].value)

        self.code_block = body_code_block

    @staticmethod
    def is_valid_block(tokens):
        order = [(Token.KEYWORD, "for"), (Token.VARIABLE, "\\S*"), (Token.SIGN, "="), (Token.VARIABLE, "\\S*"),
                 (Token.KEYWORD, "to"), (Token.VARIABLE, "[0-9]*")]
        return is_valid_grammar(order, tokens)

    def to_html(self, replacements):
        html = ""
        for i in range(self.start_value, self.end_value):
            temp_replacements = replacements.copy()
            temp_replacements[self.counter_name] = str(i)
            html += self.code_block.to_html(temp_replacements)
        return html


class IfStatement:
    """if expression {...}"""
    pass


class Assignment:

    def __init__(self, tokens):
        self.variable_name = tokens[1]
        self.variable_value = tokens[3]

    @staticmethod
    def is_valid_block(tokens):
        order_int = [(Token.KEYWORD, "var"), (Token.REPLACEABLE, "\\{\\S*\\}"), (Token.SIGN, "="),
                     (Token.VARIABLE, "[0-9]*")]
        order_text = [(Token.KEYWORD, "var"), (Token.REPLACEABLE, "\\{\\S*\\}"), (Token.SIGN, "="),
                     (Token.VARIABLE, "\\\"[a-zA-Z_]+[a-zA-Z0-9_]*\\\"")]
        orders = [order_int, order_text]
        for order in orders:
            if is_valid_grammar(order, tokens):
                return True
        return False


class Variable:
    """Variable is REPLACEABLE in Token"""

    STRING = (0, "string", "\\\".*\\\"")
    INT = (1, "integer", "[0-9]*")
    FLOAT = (2, "float", "[0-9]+.{1}[0-9]*")
    BOOLEAN = (3, "boolean", "true|false")
    VARIABLE = (4, "variable", "\\{[a-zA-Z_]+[a-zA-Z0-9_]*\\}")

    def __init__(self, code_line):
        self.name = code_line[1]
        if len(code_line) > 2:
            self.value = code_line[3]

    def assign(self, value):
        pass

    @staticmethod
    def is_valid_block(tokens):
        order_definition = [(Token.KEYWORD, "var"), (Token.REPLACEABLE, "\\{\\S*\\}")]
        order_assignment = [(Token.KEYWORD, "var"), (Token.REPLACEABLE, "\\{\\S*\\}"), (Token.SIGN, "="),
                            (Token.VARIABLE, "|".join([Variable.STRING[2], Variable.INT[2],
                                                       Variable.FLOAT[2], Variable.BOOLEAN[2], Variable.VARIABLE[2]]))]
        orders = [order_definition, order_assignment]
        for order in orders:
            if is_valid_grammar(order, tokens):
                return True
        return False


class Write:

    def __init__(self, tokens):
        self.tokens = tokens

    def to_html(self, replacements):
        html = ""
        idx_last_end = 0
        tokens_start = 0
        if self.tokens[0].value == "<<":
            tokens_start = 1
            idx_last_end = self.tokens[0].idx_columns[1] + 1
        for token in self.tokens[tokens_start:]:
            idx_start = token.idx_columns[0]
            fill_spaces = idx_start - idx_last_end - 1
            idx_last_end = token.idx_columns[1]
            for i in range(fill_spaces):
                html += " "
            if token.type == Token.REPLACEABLE:
                key = ""
                try:
                    key = token.value[1:-1]
                    html += str(replacements[key])
                except KeyError:
                    logger.warning("Replacement not found! (%s)", key)
                    html += "{" + str(key) + "}"
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
        self.variables = []
        while len(tokens) > 0:
            tokens, cut = cut_outer_eols(tokens)
            first_token = tokens[0]
            if first_token.type == Token.KEYWORD:
                next_line, idx_token_next_line = get_next_line(tokens)
                if Assignment.is_valid_block(next_line):
                    assignment = Assignment(tokens)
                    self.elements.append(assignment)
                    self.variables
                    idx_token_end = idx_token_next_line
                else:
                    header_tokens, idx_end = get_header_tokens(tokens)
                    body_tokens, idx_token_end = get_body_tokens(tokens[idx_end:])
                    idx_token_end += idx_end - 1
                    body_code_block = CodeBlock(body_tokens)
                    if ForInLoop.is_valid_block(header_tokens):
                        for_in_block = ForInLoop(header_tokens, body_code_block)
                        self.elements.append(for_in_block)
                    elif ForToLoop.is_valid_block(tokens):
                        for_to_block = ForToLoop(header_tokens, body_code_block)
                        self.elements.append(for_to_block)
                    else:
                        idx_token_end = idx_token_next_line
                        logger.error("No suitable definition for Code line found! (" + tokens_2_code(next_line) + ")")
            else:
                next_line, idx_token_end = get_next_line(tokens)
                if Write.is_valid_block(next_line):
                    writer = Write(next_line)
                    self.elements.append(writer)
            tokens = tokens[idx_token_end + 1:]

    def to_html(self, replacements):
        html = ""
        for element in self.elements:
            html += element.to_html(replacements)
        return html


def cut_outer_eols(tokens):
    if len(tokens) == 0:
        return tokens, 0
    cut = 0
    try:
        if tokens[0].type == Token.END_OF_LINE:
            tokens = tokens[1:]
            cut += 1
    except IndexError:
        pass
    try:
        if tokens[-1].type == Token.END_OF_LINE:
            tokens = tokens[:-1]
            cut += 1
    except IndexError:
        pass
    return tokens, cut


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
    if len(tokens) == 0:
        return "", 0
    num_open_brackets = 0
    idx_token_end = 0
    block_tokens = []
    tokens, cut = cut_outer_eols(tokens)
    idx_token_end += cut
    is_in_brackets = False
    if tokens[0].value == "{":
        is_in_brackets = True
    new_line = True
    write_block = False
    for token in tokens:
        if new_line and token.value == "<<":
            write_block = True
            new_line = False
        ignore_token = False
        if token.value == "{" and not write_block:
            if not is_in_brackets:
                break
            if num_open_brackets == 0:
                ignore_token = True
            num_open_brackets += 1
        if token.value == "}" and not write_block:
            num_open_brackets -= 1
            if num_open_brackets == 0:
                ignore_token = True
        if not ignore_token:
            block_tokens.append(token)
        if not write_block and num_open_brackets == 0 and is_in_brackets:
            break
        if token.type == Token.END_OF_LINE:
            write_block = False
            new_line = True
        idx_token_end += 1
    clean_block_tokens, cut = cut_outer_eols(block_tokens)
    idx_token_end += cut
    return clean_block_tokens, idx_token_end


def get_next_line(tokens):
    ret_tokens = []
    tokens, idx_end = cut_outer_eols(tokens)
    for token in tokens:
        if token.type == Token.END_OF_LINE:
            break
        else:
            ret_tokens.append(token)
        idx_end += 1
    return ret_tokens, idx_end


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

"""
@author: Julian Sobott
@created: 10.01.2019
@brief: Takes in a stream of chars and generates tokens
@description:

@external_use:

@internal_use:

"""

from Constants import KEYWORDS, SIGNS, OPERATORS
from Error_handler import *
from Globals import get_current_file_name
from Streams import CharStream


def create_tokens(chars: str):
    char_stream = CharStream(chars)
    tokens = []
    for char in char_stream:
        if char.isspace():
            if char in "\n\r":
                token = Token(Token.EOL, char, char_stream.idx - 1, char_stream.idx - 1)
                try:
                    if tokens[-1].type != Token.EOL:
                        tokens.append(token)
                except IndexError:
                    tokens.append(token)
        elif char in [SIGNS["D_QUOTE"], SIGNS["S_QUOTE"]]:
            string = get_string(char, char_stream)
            if string:
                tokens.append(string)
        elif char == OPERATORS["SLASH"]:
            comment = get_comment(char, char_stream)
            if comment:
                tokens.append(comment)
            else:
                tokens.append(get_sign(char, char_stream, OPERATORS.values(), is_operator=True))
        elif char in SIGNS.values():
            tokens.append(get_sign(char, char_stream, SIGNS.values(), is_operator=False))
        elif char in OPERATORS.values():
            tokens.append(get_sign(char, char_stream, OPERATORS.values(), is_operator=True))
        elif char.isdigit() or char == SIGNS["POINT"]:
            tokens.append(get_number(char, char_stream))
        elif char.isalpha() or char == SIGNS["UNDERSCORE"]:
            tokens.append(get_identifier(char, char_stream))
        else:
            add_error(UnknownCharacterSequence(char, get_current_file_name(), *char_stream.get_pos()))
    return tokens


def get_string(char, char_stream):
    string = ""
    idx_start = char_stream.idx - 1
    idx_end = idx_start
    is_escaped = False
    closed = False
    for next_char in char_stream:
        idx_end += 1
        if next_char == char:
            if not is_escaped:
                closed = True
                break
            else:
                string += "\""
                is_escaped = False
        else:
            if next_char == SIGNS["BACKSLASH"]:
                is_escaped = True
            elif next_char in "\n\r":
                char_stream.load_prev()
                break
            else:
                is_escaped = False
                string += next_char
    if closed:
        return Token(Token.STRING, string, idx_start, idx_end)
    else:
        add_error(MissingCharacter(char, get_current_file_name(), *char_stream.get_pos()))
        return None


def get_comment(char, char_stream):
    string = ""
    idx_start = char_stream.idx - 1
    idx_end = idx_start + 1
    next_char = char_stream.get_next()
    if next_char not in [OPERATORS["STAR"], OPERATORS["SLASH"]]:
        return None
    is_single_line = next_char == OPERATORS["SLASH"]
    closed = False

    for next_char in char_stream:
        idx_end += 1
        if is_single_line:
            if next_char in "\r\n":
                closed = True
                break
            else:
                string += next_char
        else:
            if next_char == OPERATORS["STAR"]:
                if char_stream.get_current() == OPERATORS["SLASH"]:
                    char_stream.get_next()
                    closed = True
                    break
                else:
                    string += next_char
            else:
                string += next_char

    return Token(Token.COMMENT, string, idx_start, idx_end)


def get_sign(char, char_stream, allowed_signs, is_operator):
    signs = char
    idx_start = char_stream.idx - 1
    idx_end = idx_start
    try:
        next_char = char_stream.get_next()
        signs += next_char
        if signs not in allowed_signs:
            signs = char
            char_stream.load_prev()
        else:
            idx_end = idx_start + 1
    except StopIteration:
            signs = char
    finally:
        if is_operator:
            token_type = Token.OPERATOR
        else:
            token_type = Token.SIGN
        return Token(token_type, signs, idx_start, idx_end)


def get_number(char, char_stream):
    number = char
    idx_start = char_stream.idx - 1
    idx_end = idx_start
    while True:
        next_char = char_stream.get_next()
        if len(next_char) == 0:
            char_stream.load_prev()
            break
        if next_char in "\n\r\t ":
            char_stream.load_prev()
            break
        try:
            float(number + next_char)
            number += next_char
            idx_end += 1
        except ValueError:
            char_stream.load_prev()
            break

    return Token(Token.NUMBER, number, idx_start, idx_end)


def get_identifier(char, char_stream):
    identifier = char
    idx_start = char_stream.idx - 1
    idx_end = idx_start
    while True:
        next_char = char_stream.get_next()
        if len(next_char) == 0:
            char_stream.load_prev()
            break
        elif next_char.isalpha() or next_char == SIGNS["UNDERSCORE"]:
            identifier += next_char
            idx_end += 1
        else:
            char_stream.load_prev()
            break

    if identifier in KEYWORDS:
        token_type = Token.KEYWORD
    else:
        token_type = Token.IDENTIFIER
    return Token(token_type, identifier, idx_start, idx_end)


class Token:
    SIGN = (0, "SIGN")
    NUMBER = (1, "NUMBER")
    IDENTIFIER = (2, "IDENTIFIER")
    KEYWORD = (3, "KEYWORD")
    OPERATOR = (4, "OPERATOR")
    STRING = (5, "STRING")
    COMMENT = (6, "COMMENT")
    EOL = (7, "END_OF_LINE")

    def __init__(self, token_type, value, idx_start, idx_end):
        self.type = token_type
        self.value = value
        self.idx_start = idx_start
        self.idx_end = idx_end

    def __repr__(self):
        return f"{self.type[1]}: {self.value}"


if __name__ == '__main__':
    chars_ = """ var x = 10
    {y: "Hello\\"" """
    create_tokens(chars_)

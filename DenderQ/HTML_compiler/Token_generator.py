"""
@author: Julian Sobott
@created: 29.12.2018
@brief: Generates a token list from HTML_EXE Code
@description:

@external_use:

@internal_use:

"""
from Logging import logger
from Keywords import KEYWORDS, SIGNS

__all__ = ["generate_tokens", "tokens_2_str"]

example_code = (
    "for i, child in {children}{\n"
    "if i == 0 {\n"
    "<li {i}>{child}</li>\n"
    "}else{\n"
    "<li i>{child}</li>\n"
    "}\n"
    "}\n")

example_code_01 = (
    "for i, child in {children}{\n"
    "<< <li {i}>{child}</li>\n"
    "}\n")


class Text:
    new_line_c = ["\n", "\r", "\r\n"]

    def __init__(self, text):
        self.text = text
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        c = ""
        line = ""
        while c not in self.new_line_c and self.idx < len(self.text):
            c = self.text[self.idx]
            self.idx += 1
            if c not in self.new_line_c:
                line += c
        if len(line) == 0:
            raise StopIteration
        return line


class Line:
    comma = ","
    open_curly_bracket = "{"
    closed_curly_bracket = "}"
    tokens = [comma]

    def __init__(self, text):
        self.text = text
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        c = ""
        element = ""
        working_text = self.text[self.idx:].lstrip()
        working_idx = 0
        self.idx = self.idx + (len(self.text[self.idx:]) - len(working_text))
        if len(working_text) == 0:
            raise StopIteration
        start_replaceable = False
        while not c.isspace() and working_idx < len(working_text):
            c = working_text[working_idx]
            self.idx += 1
            working_idx += 1
            if not c.isspace():
                if c == self.comma:
                    if len(element) > 0:
                        self.idx -= 1
                        return element
                    else:
                        return c
                if c == self.open_curly_bracket:
                    if len(element) > 0:
                        self.idx -= 1
                        return element
                    else:
                        if len(working_text) <= working_idx + 1 or working_text[working_idx + 1].isspace():
                            if len(element) > 0:
                                self.idx -= 1
                                return element
                            else:
                                return c
                    start_replaceable = True
                elif c == self.closed_curly_bracket:
                    if working_idx <= 0 or working_text[working_idx - 1].isspace():
                        if len(element) > 0:
                            self.idx -= 1
                            return element
                        else:
                            return c
                    elif start_replaceable:
                        return element + c
                element += c
        return element


class Token:
    CONSTANT = 0
    VARIABLE = 2
    KEYWORD = 3
    SIGN = 4
    END_OF_LINE = 5
    REPLACEABLE = 6

    def __init__(self, word, token_type=None):
        self.value = word
        if token_type and self.CONSTANT <= token_type <= self.REPLACEABLE:
            self.type = token_type
        elif word in KEYWORDS:
            self.type = self.KEYWORD
        elif self.is_constant(word):
            self.type = self.CONSTANT
        elif word in SIGNS:
            self.type = self.SIGN
        elif word == "\n":
            self.type = self.END_OF_LINE
        elif word[0] == "{" and word[:-1] == "}":
            self.type = self.REPLACEABLE
        else:
            self.type = self.VARIABLE

    @staticmethod
    def is_constant(word):
        if "\"" in word or "'" in word:
            return True
        if isinstance(word, int) or isinstance(word, float):#
            return True

    def __str__(self):
        types = {Token.CONSTANT: "Constant", Token.VARIABLE: "Variable", Token.KEYWORD: "Keyword", Token.SIGN: "Sign",
                 Token.END_OF_LINE: "End of line", Token.REPLACEABLE: "Replaceable"}
        return types[self.type] + ": " + str(self.value)


def generate_tokens(code):
    text = Text(code)
    tokens = []
    for line in text:
        for word in Line(line):
            token = Token(word)
            tokens.append(token)
        tokens.append(Token("EOL", Token.END_OF_LINE))
    logger.debug(tokens_2_str(tokens))
    return tokens


def tokens_2_str(tokens):
    return '[|%s]' % '| |'.join(map(str, tokens))


if __name__ == '__main__':
    generate_tokens(example_code_01)

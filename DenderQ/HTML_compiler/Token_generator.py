"""
@author: Julian Sobott
@created: 29.12.2018
@brief: Generates a token list from HTML_EXE Code
@description:

@external_use:

@internal_use:

"""
from Logging import logger
from .Keywords import KEYWORDS, SIGNS

__all__ = ["generate_tokens", "tokens_2_str", "tokens_2_code"]

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
    ">> <li {i}>{child}</li>\n"
    "}\n")

example_code_02 = (
    "<p>{children}</p>"
)


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
        working_text = self.text[self.idx:].lstrip()
        working_idx = 0
        self.idx = self.idx + (len(self.text[self.idx:]) - len(working_text))

        while c not in self.new_line_c and working_idx < len(working_text):
            c = working_text[working_idx]
            self.idx += 1
            working_idx += 1
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
        idx_start = self.idx
        idx_end = self.idx - 1
        if len(working_text) == 0:
            raise StopIteration
        start_replaceable = False

        while not c.isspace() and working_idx < len(working_text):
            c = working_text[working_idx]
            self.idx += 1
            working_idx += 1
            if not c.isspace():
                idx_end += 1
                if c == self.open_curly_bracket:
                    if len(element) > 0 and element != "\\":
                        self.idx -= 1
                        return element, (idx_start, idx_end - 1)
                    else:
                        if len(working_text) <= working_idx + 1 or working_text[working_idx + 1].isspace():
                            if len(element) > 0:
                                self.idx -= 1
                                return element, (idx_start, idx_end - 1)
                            else:
                                return c, (idx_start, idx_end)
                    start_replaceable = True
                elif c == self.closed_curly_bracket:
                    if working_idx <= 0 or working_text[working_idx - 1].isspace():
                        if len(element) > 0:
                            self.idx -= 1
                            return element, (idx_start, idx_end - 1)
                        else:
                            return c, (idx_start, idx_end)
                    elif start_replaceable:
                        return element + c, (idx_start, idx_end)
                elif c in SIGNS:
                    if len(element) > 0:
                        self.idx -= 1
                        return element, (idx_start, idx_end - 1)
                    else:
                        try:
                            c_comb = c + working_text[working_idx ]
                            if c_comb in SIGNS:
                                self.idx += 1
                                return c_comb, (idx_start, idx_end + 1)
                        except IndexError:
                            pass
                        return c, (idx_start, idx_end)
                element += c
        return element, (idx_start, idx_end)


class Token:
    CONSTANT = 0
    VARIABLE = 2
    KEYWORD = 3
    SIGN = 4
    END_OF_LINE = 5
    REPLACEABLE = 6

    def __init__(self, word, line_number, idx_columns, token_type=None):
        self.value = word
        self.line_number = line_number
        self.idx_columns = idx_columns  # tuple: (idx_start, idx_end)
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
        elif word[0] == "{" and word[-1] == "}":
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
        return types[self.type] + ": " + str(self.value) + " " + str(self.idx_columns)

    def __repr__(self):
        return self.__str__()


def generate_tokens(code):
    text = Text(code)
    tokens = []
    idx_line = 1
    for line in text:
        for word, columns in Line(line):
            token = Token(word, idx_line, columns)
            tokens.append(token)
        tokens.append(Token("EOL", idx_line, (-1, -1), token_type=Token.END_OF_LINE))
        idx_line += 1
    return tokens


def tokens_2_str(tokens):
    return '[|%s]' % '| |'.join(map(str, tokens))


def tokens_2_code(tokens):
    return '%s' % ' '.join(map(str, list(token.value for token in tokens)))


if __name__ == '__main__':
    generate_tokens(example_code_01)

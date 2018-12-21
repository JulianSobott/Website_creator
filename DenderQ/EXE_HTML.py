"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
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
    "<li {i}>{child}</li>\n"
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
    whitespace = [" ", "\t", "\n", "\r", "\r\n"]
    comma = ","
    open_curly_bracket = "{"
    closed_curly_bracket = "}"
    tokens = [comma, open_curly_bracket, closed_curly_bracket]

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
        while c not in self.whitespace and working_idx < len(working_text):
            c = working_text[working_idx]
            self.idx += 1
            working_idx += 1
            if c not in self.whitespace:
                if c in self.tokens:
                    if len(element) > 0:
                        self.idx -= 1
                        return element
                    else:
                        return c
                element += c
        return element


class For:

    def __init__(self, line):
        pass


class ForIn:
    def __init__(self):
        pass


class ForTo:
    def __init__(self):
        pass


KEYWORD_CLASSES = {"for": For}


def parse_executable_html(code, replaceables):
    text = Text(code)
    for line in text:
        for word in Line(line):
            try:
                key_class = KEYWORD_CLASSES[word]
            except KeyError:
                pass


if __name__ == '__main__':
    p_repl = {"children": ["1", "2"]}
    parse_executable_html(example_code_01, p_repl)

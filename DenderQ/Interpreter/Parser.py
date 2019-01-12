"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""

from Logging import logger
from Streams import TokenStream, CodeElementStream, GrammarStream
from Tokenizer import Token
from Constants import *


__all__ = ["create_abstract_code"]

Optional = 0
Single = 1
Multiple = float("inf")


class CodeElement:

    def __init__(self, *args):
        self.grammars = []

    def parse_possible(self, code_stream: CodeElementStream):
        """Try to apply this class to all fitting elements"""
        for grammar in self.grammars:
            grammar_stream = GrammarStream(grammar)
            code_stream.branch()
            is_possible = True

            while is_possible:
                token_fits_element = True
                element = grammar_stream.get_current()
                token = code_stream.get_current()
                if element is None:
                    code_stream.merge(self)
                    break
                if token is None:
                    break
                element_type = element[0]
                element_specification = element[1]
                if not isinstance(element_specification, list):
                    element_specification = [element_specification]
                if len(element) == 3:
                    element_counts = element[2]
                else:
                    element_counts = Single

                if element_type is Coherency:
                    element_class = element_specification[0]
                    if isinstance(token, CodeElement):
                        token_fits_element = element_class().parse_possible(code_stream)
                elif element_type is Token:
                    try:
                        if token.type not in element_specification:
                            token_fits_element = False
                    except AttributeError:
                        token_fits_element = False
                elif element_type is SIGNS:
                    try:
                        if token.value not in element_specification:
                            token_fits_element = False
                    except AttributeError:
                        token_fits_element = False
                elif element_type is OPERATORS:
                    if token.value not in element_specification:
                        token_fits_element = False

                if element_counts == Optional:
                    if token_fits_element:
                        code_stream.inc()
                        grammar_stream.inc()
                        # next token next element
                    else:
                        grammar_stream.inc()
                        # next element
                elif element_counts == Single:
                    if token_fits_element:
                        code_stream.inc()
                        grammar_stream.inc()
                        # next token next element
                    else:
                        is_possible = False
                        code_stream.pop()
                        # Stop (wrong grammar)
                elif element_counts == Multiple:
                    if token_fits_element:
                        code_stream.inc()
                        # next token
                    else:
                        grammar_stream.inc()
                        # next element
        return is_possible

    def __call__(self, *args, **kwargs):
        cls = self.__class__
        logger.debug(args)
        logger.debug(kwargs)
        obj = self.__new__(cls)
        if obj is not None and issubclass(obj.__class__, cls):
            obj.__init__(*args)
        return obj


class CodeBlock:

    def __init__(self, code_stream):
        self.elements = []
        Calculation().parse_possible(code_stream)
        self.elements = code_stream.elements[:code_stream.idx + 1]


class Coherency:
    pass


class Constant:

    def __init__(self):
        self.grammar = [[(Token, Token.IDENTIFIER), (SIGNS, SIGNS["COLON"]), (Coherency, Expression)]]


class Constants:
    grammar = [
        [
            (Token, Token.IDENTIFIER), (SIGNS, SIGNS["COLON"]), (Token, Token.IDENTIFIER), (Token, Token.EOL),
            (Coherency, "self")
        ],
        [
            (None,)
        ]
               ]


class ConstantsBlock:
    grammar = [[(Token, Token.IDENTIFIER, Optional), (SIGNS, SIGNS["L_BRACES"]), (Token, Token.EOL, Optional),
                (Coherency, Constants), (Token, Token.EOL, Optional), (SIGNS, SIGNS["R_BRACES"])]]


class Expression:
    pass


class Calculation(CodeElement):

    valid_operations = [OPERATORS["PLUS"], OPERATORS["STAR"], OPERATORS["SLASH"], OPERATORS["MINUS"], OPERATORS["AND"],
                        OPERATORS["OR"], OPERATORS["GT"], OPERATORS["GE"], OPERATORS["EEQ"],
                        OPERATORS["NE"], OPERATORS["LT"], OPERATORS["LE"]]

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.grammars = [[(Coherency, Number)],
                         [(SIGNS, SIGNS["L_PARENTHESES"], Optional), (Coherency, self.__class__),
                          (OPERATORS, self.valid_operations), (Coherency, self.__class__),
                          (SIGNS, SIGNS["L_PARENTHESES"], Optional)]
                         ]
        self.l_value = 0
        self.r_value = None
        self.sign = None
        if len(args) > 0:
            tokens = args[0]
            if len(tokens) >= 1:
                self.l_value = tokens[0]
            if len(tokens) > 1:
                self.sign = tokens[1]
                self.r_value = tokens[2]

    def __repr__(self):
        if self.r_value:
            return "(" + str(self.l_value) + str(self.sign.value) + str(self.r_value) + ")"
        else:
            return str(self.l_value)


class Number(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(Token, Token.NUMBER)]]
        if len(args) > 0:
            token = args[0][0]
            self.value = token.value

    def __repr__(self):
        return self.value


def create_abstract_code(tokens):
    token_stream = TokenStream(tokens)
    code_stream = CodeElementStream(token_stream)
    code_block = CodeBlock(code_stream)
    return code_block

"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:
implemented:
    + ConstantsBlock
    + Assignment
    + Calculation (only with keyword var)
missing:
    - html block
    - Calculations (without keyword var. Another keyword or function)
    - for loops
    - if condition
    - conditions
    - includes
    - functions

@external_use:

@internal_use:


"""

from Logging import logger
from .Streams import TokenStream, CodeElementStream, GrammarStream
from .Tokenizer import Token
from .Constants import *
from .MathExpressions import shunting_yard_algorithm, reverse_polish
from .Globals import SymbolTable, buffer_to_file


__all__ = ["create_abstract_code"]

Optional = 0
Single = 1
MinSingle = 2
Multiple = float("inf")


class CodeElement:

    def __init__(self, *args):
        self.grammars = []

    def parse_possible(self, code_stream: CodeElementStream):
        """Try to apply this class to all fitting elements"""
        was_successful = False
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
                    was_successful = True
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
                elif element_type is KEYWORDS:
                    if token.value not in element_specification:
                        token_fits_element = False

                if element_counts == Optional:
                    if token_fits_element:
                        code_stream.inc()
                        grammar_stream.inc()
                    else:
                        grammar_stream.inc()
                elif element_counts == Single:
                    if token_fits_element:
                        code_stream.inc()
                        grammar_stream.inc()
                    else:
                        is_possible = False
                        code_stream.pop()
                elif element_counts == MinSingle:
                    if token_fits_element:
                        code_stream.inc()
                        hit_once = True
                    else:
                        stop = False
                        try:
                            if hit_once:
                                grammar_stream.inc()
                            else:
                                stop = True
                        except NameError:
                            stop = True
                        if stop:
                            is_possible = False
                            code_stream.pop()
                        else:
                            grammar_stream.inc()
                elif element_counts == Multiple:
                    if token_fits_element:
                        code_stream.inc()
                    else:
                        grammar_stream.inc()
        return was_successful

    def __call__(self, *args, **kwargs):
        cls = self.__class__
        obj = self.__new__(cls)
        if obj is not None and issubclass(obj.__class__, cls):
            obj.__init__(*args)
        return obj


class CodeBlock:

    def __init__(self, code_stream: CodeElementStream):
        token = code_stream.get_current()
        while token:
            if isinstance(token, Token):
                while token and token.type == Token.EOL:
                    token = code_stream.get_current()
                    if token and token.type == Token.EOL:
                        code_stream.idx += 1
                if token is None:
                    break
                if token.type == Token.KEYWORD:
                    if token.value == "var":
                        Assignment().parse_possible(code_stream)
                else:
                    parsed = ConstantsBlock().parse_possible(code_stream)
                    if not parsed:
                        parsed = Write().parse_possible(code_stream)
            token = code_stream.get_next()
        self.elements = code_stream.elements[:code_stream.idx + 1]

    def remove_eols(self):
        temp_elements = []
        for element in self.elements:
            if not(isinstance(element, Token) and element.type == Token.EOL):
                temp_elements.append(element)
        self.elements = temp_elements

    def execute(self):
        for element in self.elements:
            element.execute()

    def __repr__(self):
        return str(self.elements)


class Coherency:
    pass


class Constant(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(Token, Token.IDENTIFIER), (SIGNS, SIGNS["COLON"]), (Coherency, Calculation),
                         (Token, Token.EOL)],
                        [(Token, Token.IDENTIFIER), (SIGNS, SIGNS["COLON"]), (Token, Token.IDENTIFIER, MinSingle),
                         (Token, Token.EOL)]
                        ]
        self.args = args
        if len(args) > 0:
            tokens = args[0]
            self.identifier = tokens[0]
            self.value = tokens[2]

    def __repr__(self):
        try:
            return str(self.identifier.value) + ": " + str(self.value) + "\n"
        except Exception:
            return str(self.identifier.value) + ": " + str(self.value) + "\n"


class Constants(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(Token, Token.EOL, Optional), (Coherency, Constant, MinSingle)]]
        if len(args) > 0:
            tokens = args[0]
            self.constants = tokens

    def __repr__(self):
        return "".join(str(c) for c in self.constants)


class ConstantsBlock(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(Token, Token.IDENTIFIER, Optional), (SIGNS, SIGNS["L_BRACES"]), (Token, Token.EOL, Optional),
                (Coherency, Constants), (Token, Token.EOL, Optional), (SIGNS, SIGNS["R_BRACES"])]]
        if len(args) > 0:
            tokens = args[0]
            with_identifier = 0
            if isinstance(tokens[0], Token) and tokens[0].type == Token.IDENTIFIER:
                self.global_identifier = tokens[0]
                with_identifier = 1
            if isinstance(tokens[1 + with_identifier], Token) and tokens[1 + with_identifier].type == Token.EOL:
                self.constants = tokens[2 + with_identifier]
            else:
                self.constants = tokens[1 + with_identifier]

    def __repr__(self):
        try:
            return str(self.global_identifier.value) + "{ " + str(self.constants) + " }"
        except AttributeError:
            return "{ " + str(self.constants) + " }"


class Assignment(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(KEYWORDS, "var"), (Token, Token.IDENTIFIER), (OPERATORS, OPERATORS["EQ"]), (Coherency, Expression)]]
        if len(args) > 0:
            tokens = args[0]
            self.identifier = tokens[1]
            self.r_value = tokens[3]

    def __repr__(self):
        return str(self.identifier) + " = " + str(self.r_value)


class Expression(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(Coherency, Calculation)]]
        if len(args) > 0:
            tokens = args[0]
            self.value = tokens[0]

    def __repr__(self):
        return str(self.value)


class Calculation(CodeElement):

    valid_operations = [OPERATORS["PLUS"], OPERATORS["STAR"], OPERATORS["SLASH"], OPERATORS["MINUS"], OPERATORS["AND"],
                        OPERATORS["OR"], OPERATORS["GT"], OPERATORS["GE"], OPERATORS["EEQ"],
                        OPERATORS["NE"], OPERATORS["LT"], OPERATORS["LE"]]

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) > 0:
            self.intermediate_format = args[0]

    def parse_possible(self, code_stream: CodeElementStream):
        is_valid = True
        code_stream.branch()
        calculation_tokens = []
        token = code_stream.get_current()
        while token and (not isinstance(token, Token) or (token.type != Token.EOL and token.value != SIGNS["R_BRACES"])):
            calculation_tokens.append(token)
            token = code_stream.inc()
        ordered_tokens = shunting_yard_algorithm(calculation_tokens)
        code_stream.replace_branched_tokens(ordered_tokens)
        code_stream.merge(self)
        return is_valid

    def get_result(self) -> Token:
        return reverse_polish(self.intermediate_format)

    def __repr__(self):
        try:
            return "Calculation: Result = " + str(self.get_result())
        except IndexError:
            return f"Calculation: {str(self.intermediate_format)}"


class Number(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(Token, Token.NUMBER)]]
        if len(args) > 0:
            token = args[0][0]
            self.value = token.value

    def __repr__(self):
        return self.value


class Write(CodeElement):

    def __init__(self, *args):
        super().__init__()
        if len(args) > 0:
            self.args = args[0]

    def parse_possible(self, code_stream: CodeElementStream):
        is_valid = True
        code_stream.branch()
        write_tokens = []
        token = code_stream.get_current()
        if not isinstance(token, Token):
            code_stream.pop()
            return False
        while token and token.type != Token.EOL:
            if token.type == Token.SIGN and token.value == SIGNS["L_BRACES"]:
                parsed = Replaceable().parse_possible(code_stream)
                if not parsed:
                    write_tokens.append(token)
            else:
                write_tokens.append(token)
            token = code_stream.inc()
        code_stream.merge(self)
        return is_valid

    def __repr__(self):
        return "Write: " + "".join(str(c) for c in self.args)

    def execute(self):
        text = ""
        idx_last_end = 0
        for arg in self.args:
            if isinstance(arg, Token):
                value = str(arg.value)
                fill_spaces = max(arg.idx_start - idx_last_end - 1, 0)
                text += value.rjust(len(value) + fill_spaces)
                idx_last_end = arg.idx_end
            else:
                temp_text = arg.execute()
                if temp_text:
                    text += str(temp_text)
        buffer_to_file(text)


class Replaceable(CodeElement):

    def __init__(self, *args):
        super().__init__()
        self.grammars = [[(SIGNS, SIGNS["L_BRACES"]), (Coherency, Expression), (SIGNS, SIGNS["R_BRACES"])]]
        if len(args) > 0:
            tokens = args[0]
            self.value = tokens[1:-1]

    def __repr__(self):
        return "Replaceable: " + "".join(str(c) for c in self.value)


def create_abstract_code(tokens):
    token_stream = TokenStream(tokens)
    code_stream = CodeElementStream(token_stream)
    code_block = CodeBlock(code_stream)
    code_block.remove_eols()
    return code_block

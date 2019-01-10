"""
@author: Julian Sobott
@created: 10.01.2019
@brief: All keywords, signs
@description:

@external_use:

@internal_use:

"""
KEYWORDS = []
OPERATORS = {}
SIGNS = {}


__all__ = ["KEYWORDS", "SIGNS", "OPERATORS"]


def add_keyword(word):
    KEYWORDS.append(word)


def add_operator(word, name):
    OPERATORS[name] = word


def add_sign(word, name):
    SIGNS[name] = word

# Keywords


add_keyword("for")
add_keyword("in")
add_keyword("to")
add_keyword("if")
add_keyword("var")

# Signs
add_sign(",", "COMMA")
add_sign(".", "POINT")
add_sign("(", "L_PARENTHESES")
add_sign(")", "R_PARENTHESES")
add_sign("{", "L_BRACES")
add_sign("}", "R_BRACES")
add_sign("[", "L_BRACKET")
add_sign("]", "R_BRACKET")
add_sign("#", "HASH")
add_sign("\"", "D_QUOTE")
add_sign("'", "S_QUOTE")
add_sign("_", "UNDERSCORE")
add_sign("\\", "BACKSLASH")
add_sign(":", "COLON")

#add_sign("<<")      # Write line


# operators
add_operator("!", "NOT")
add_operator("-", "MINUS")
add_operator("+", "PLUS")
add_operator("*", "STAR")
add_operator("/", "SLASH")
add_operator("=", "EQ")
add_operator("&", "AND")
add_operator("&&", "")
add_operator("%", "PERCENT")
add_operator(">", "GT")
add_operator(">=", "GE")
add_operator("==", "EEQ")
add_operator("!=", "NE")
add_operator("<", "LT")
add_operator("<=", "LE")
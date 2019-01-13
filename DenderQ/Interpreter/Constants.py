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
PRECEDENCES = {}
SIGNS = {}


__all__ = ["KEYWORDS", "SIGNS", "OPERATORS", "PRECEDENCES", "get_by_value"]

unary = 1 << 0
binary = 1 << 1


def add_keyword(word):
    KEYWORDS.append(word)


def add_operator(word, name, precedence):
    OPERATORS[name] = word
    PRECEDENCES[name] = precedence


def add_sign(word, name):
    SIGNS[name] = word


def get_by_value(dict_, value):
    for key in dict_:
        if dict_[key] == value:
            return key
    return None

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
# precedence: 0 = low -- 20 high
add_operator("!", "NOT", 20)
# add_operator("++", "INCREMENT", )
# add_operator("--", "DECREMENT")
add_operator("*", "STAR", 18)
add_operator("/", "SLASH", 18)
add_operator("%", "PERCENT", 18)
add_operator("-", "MINUS", 15)
add_operator("+", "PLUS", 15)
add_operator("<", "LT", 10)
add_operator("<=", "LE", 10)
add_operator(">", "GT", 10)
add_operator(">=", "GE", 10)
add_operator("==", "EEQ", 9)
add_operator("!=", "NE", 9)
add_operator("&", "AND", 8)
add_operator("|", "OR", 6)
add_operator("=", "EQ", 2)

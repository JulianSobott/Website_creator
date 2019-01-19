"""
@author: Julian Sobott
@created: 13.01.2019
@brief: Algorithms to compute mathematical expressions
@description:
shunting_yard_algorithm:
    Reorders the tokens so that they appear in an intermediate format

reverse_polish:
    Takes the intermediate format and computes the result

@external_use:

@internal_use:

"""
from .Tokenizer import Token
from Constants import OPERATORS, get_by_value, PRECEDENCES
from Constants import SIGNS
from Logging import logger
from .Globals import symbolTable


def shunting_yard_algorithm(tokens: list):
    token_list = tokens.copy()
    operator_stack = []
    output_queue = []

    while len(token_list) > 0:
        token: Token = token_list.pop(0)
        if token.type == Token.NUMBER:
            output_queue.append(token)
        elif token.type == Token.IDENTIFIER:
            output_queue.append(token)
        elif token.type == Token.OPERATOR:
            try:
                top_operator = operator_stack[-1]
                while top_operator.type == Token.OPERATOR and \
                        PRECEDENCES[top_operator.sign_name] > PRECEDENCES[token.sign_name]:
                    operator = operator_stack.pop()
                    output_queue.append(operator)
                    top_operator = operator_stack[-1]
            except IndexError:
                pass
            operator_stack.append(token)
        elif token.type == Token.SIGN:
            if token.value == SIGNS["L_PARENTHESES"]:
                operator_stack.append(token)
            elif token.value == SIGNS["R_PARENTHESES"]:
                try:
                    top_operator = operator_stack[-1]
                    while top_operator.value != SIGNS["L_PARENTHESES"]:
                        operator = operator_stack.pop()
                        output_queue.append(operator)
                        top_operator = operator_stack[-1]
                except IndexError:
                    pass
                l_paren = operator_stack.pop()

    while len(operator_stack) > 0:
        operator = operator_stack.pop()
        output_queue.append(operator)
    return output_queue


def reverse_polish(ordered_tokens):
    """
    Pure Math:          (7 + 3)             @return: Number(10)
    Math + Identifiers: (7 + var_three)     @return: Number(10) if var_three is initialized
    Identifier:         x                   @return: value of x if set else String(x)
    """
    from .Parser import Number, String
    stack = []
    for token in ordered_tokens:
        if token.type == Token.NUMBER:
            stack.append(token)
        elif token.type == Token.OPERATOR:
            v1 = stack.pop()
            v2 = stack.pop()
            num1 = v1.value
            num2 = v2.value
            operator = token.value
            res = eval(str(num2) + str(operator) + str(num1))
            stack.append(Number(res))
        elif token.type == Token.IDENTIFIER:
            value = symbolTable.get_recursive(token)
            stack.append(value)
    if isinstance(stack[0], Token):
        return String(stack[0].value)
    return stack[0]

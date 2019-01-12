"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""

class CharStream:

    def __init__(self, chars: str):
        self.chars = chars
        self.idx = 0
        self.line = 0
        self.idx_col = 0
        self.end_flag = False

    def load_prev(self):
        self.idx -= 1
        if self.chars[self.idx] in "\n\r":
            self.idx_col = 0
            self.line -= 1
        else:
            self.idx_col -= 1

    def get_next(self):
        try:
            return self.__next__()
        except StopIteration:
            return ""

    def get_current(self):
        try:
            return self.chars[self.idx]
        except IndexError:
            return ""

    def get_pos(self):
        return self.line, self.idx_col

    def __iter__(self):
        return self

    def __next__(self):
        try:
            char = self.chars[self.idx]
            if char in "\n\r":
                self.line += 1
                self.idx_col = 0
            return char
        except IndexError:
            self.end_flag = True
            raise StopIteration
        finally:
            if not self.end_flag:
                self.idx += 1
                self.idx_col += 1


class TokenStream:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.idx = 0
        self.idx_last_end = 0
        self.end_flag = False

    def remove_comments(self):
        from Tokenizer import Token
        new_tokens = []
        for token in self.tokens:
            if token.type != Token.COMMENT:
                new_tokens.append(token)
        self.tokens = new_tokens

    def load_prev(self):
        self.idx = self.idx_last_end

    def get_next(self):
        try:
            return self.__next__()
        except StopIteration:
            return None

    def get_current(self):
        try:
            return self.tokens[self.idx]
        except IndexError:
            return None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            token = self.tokens[self.idx]
            return token
        except IndexError:
            self.end_flag = True
            raise StopIteration
        finally:
            if not self.end_flag:
                self.idx += 1


class CodeElementStream:

    def __init__(self, tokens: TokenStream):

        tokens.remove_comments()
        self.elements = tokens.tokens
        self.branched_tokens = []
        self.branched_indices = []
        self.idx = 0

    def branch(self):
        self.branched_tokens.append([])
        self.branched_indices.append(self.idx)

    def merge(self, code_element_class):
        code_element = code_element_class.__call__(self.branched_tokens.pop())
        idx_prev = self.branched_indices.pop()
        self.elements = self.elements[:idx_prev] + \
                        [code_element] +\
                        self.elements[self.idx:]
        self.idx = idx_prev
        pass

    def pop(self):
        branched_tokens = self.branched_tokens.pop()
        self.idx = self.branched_indices.pop()
        return branched_tokens

    def get_current(self):
        try:
            return self.elements[self.idx]
        except IndexError:
            return None

    def inc(self):
        self.branched_tokens[-1].append(self.get_current())
        self.idx += 1

    def __iter__(self):
        return self

    def __next__(self):
        try:
            element = self.elements[self.idx]
            return element
        except IndexError:
            raise StopIteration
        finally:
            self.idx += 1


class GrammarStream:

    def __init__(self, grammar):
        self.grammar = grammar
        self.idx = 0

    def get_current(self):
        try:
            return self.grammar[self.idx]
        except IndexError:
            return None

    def inc(self):
        self.idx += 1

    def __iter__(self):
        return self

    def __next__(self):
        try:
            element = self.grammar[self.idx]
            return element
        except IndexError:
            raise StopIteration
        finally:
            self.idx += 1

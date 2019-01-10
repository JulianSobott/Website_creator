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

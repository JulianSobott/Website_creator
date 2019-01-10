"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
import unittest

from Interpreter import Interpreter

class TestTokens(unittest.TestCase):

    def test_example_01(self):
        in_file = "tests/example.ley"
        out_file = ""
        Interpreter.parse_file(in_file, out_file)

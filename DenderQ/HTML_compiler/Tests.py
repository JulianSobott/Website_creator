"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import unittest

from Token_generator import generate_tokens
from EXE_HTML import parse_executable_html

example_long_for_in = (
            "for i, child in {children}{\n"
            "<li {i}>{child}</li>\n"
            "<p> {i}th child</p>\n"
            "}\n"
        )

example_short_for_in = (
            "for child in {children}{\n"
            "<< <li>{child}</li>\n"
            "}\n"
        )

example_for_to = (
    "for i=0 to 10{\n"
    "<p>{i}</p>\n"
    "}\n"
)


class TestTokens(unittest.TestCase):

    def test_long_for_in(self):
        tokens = generate_tokens(example_long_for_in)
        num_tokens = len(tokens)
        self.assertEqual(num_tokens, 31)

    def test_short_for_in(self):
        tokens = generate_tokens(example_short_for_in)
        num_tokens = len(tokens)
        self.assertEqual(num_tokens, 18)


class TestHTML(unittest.TestCase):

    def test_long_for_in(self):
        replaceables = {"children": ["Anna", "Tom"]}
        html = parse_executable_html(example_long_for_in, replaceables)
        correct_html = (
                "<li 0>Anna</li>\n"
                "<p> 0th child</p>\n"
                "<li 1>Tom</li>\n"
                "<p> 1th child</p>\n"
                "}\n")
        self.assertEqual(html, correct_html)

    def test_for_to(self):
        html = parse_executable_html(example_for_to, {})
        correct_html = (
            ""
        )


"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import unittest

from HTML_compiler.Token_generator import generate_tokens
from HTML_compiler.EXE_HTML import parse_executable_html

example_long_for_in = (
            "for i, child in {children}{\n"
            "<li {i}>{child}</li>\n"
            "<p> {i}th child</p>\n"
            ""
        )

example_short_for_in = (
            "for child in {children}{\n"
            "<< <li>{child}</li>\n"
            "}\n"
        )

example_for_to = (
    "for i=0 to 3{\n"
    "<p>{i}</p>\n"
    "\n"
)

example_real = (
    """
<export>
<ul>
    for i, child in {children}{
      <li {i}>{child}</li>
    }
</ul>
    """
)

example_variables = (
"""
var {i} = 0
<p>{i}</p>
"""
)


class TestTokens(unittest.TestCase):

    def test_long_for_in(self):
        tokens = generate_tokens(example_long_for_in)
        num_tokens = len(tokens)
        self.assertEqual(num_tokens, 29)

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
                "")
        self.assertEqual(html, correct_html)

    def test_for_to(self):
        html = parse_executable_html(example_for_to, {})
        correct_html = (
            "<p>0</p>\n"
            "<p>1</p>\n"
            "<p>2</p>\n"
        )
        self.assertEqual(html, correct_html)

    def test_real(self):
        replaceables = {"children": ["Anna", "Tom"]}
        html = parse_executable_html(example_real, replaceables)
        correct_html = (
            """<export>
<ul>
<li 0>Anna</li>
<li 1>Tom</li>
</ul>
"""
        )
        self.assertEqual(html, correct_html)

    def test_variables(self):
        replaceables = {}
        html = parse_executable_html(example_variables, replaceables)


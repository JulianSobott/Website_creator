"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
import unittest
import re

from Interpreter import Interpreter
from Logging import logger

test_file_path = "test_cases.ley"
result_path = "temp_result.ley"
temp_code_path = "temp_code.ley"


class TestTokens(unittest.TestCase):

    def test_example_01(self):
        in_file = "example.ley"
        out_file = ""
        Interpreter.parse_file(in_file, out_file)


def test_case(self, name):
    file_path = write_to_test_file(name)
    Interpreter.parse_file(file_path, result_path)
    actual_code, expected_code = get_results(result_path, test_file_path, name)
    self.assertEqual(actual_code, expected_code)


class TestParser(unittest.TestCase):

    def test_ConstantsBlock(self):
        test_case(self, "ConstantsBlock")

    def test_Assignment(self):
        pass

    def test_Calculation(self):
        pass

    def test_Write(self):
        pass

    def test_ForInLoop(self):
        pass

    def test_List(self):
        pass


def write_to_test_file(test_case_name):
    code = get_test_case_code(test_case_name)

    if len(code) == 0:
        logger.error("No Code found for test-case: %s", test_case_name)

    with open(temp_code_path, "w") as file:
        file.write(code)

    return temp_code_path


def get_results(actual_result_path, expeced_result_path, test_case_name):
    expected_result = get_test_case_code(f"{test_case_name}-expected")
    with open(actual_result_path, "r") as actual_file:
        actual_result = actual_file.read()

    clean_actual_result = actual_result.strip()
    clean_expected_result = expected_result.strip()
    return clean_actual_result, clean_expected_result


def get_test_case_code(test_case_name):
    code = ""
    with open(test_file_path, "r") as file:
        add_lines = False
        for line in file.readlines():
            match = re.match("###(\\S+)###", line)
            if match:
                if match.group(1) == test_case_name:
                    add_lines = True
                elif add_lines:
                    break

            elif add_lines:
                code += line
    return code


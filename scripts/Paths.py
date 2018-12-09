"""
@author: Julian Sobott
@created: 09.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import os

TOOL_PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE_PROJECT_PATH = os.getcwd()

REL_TEMPLATES_PATH = "Templates"
ABS_TEMPLATES_PATH = os.path.join(TOOL_PROJECT_PATH, REL_TEMPLATES_PATH)

REL_TEMPLATES_JSON_PATH = "Templates/templates.json"
ABS_TEMPLATES_JSON_PATH = os.path.join(TOOL_PROJECT_PATH, REL_TEMPLATES_JSON_PATH)

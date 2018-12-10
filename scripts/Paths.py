"""
@author: Julian Sobott
@created: 09.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
import os


class Tool:
    PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
    ABS_TEMPLATES_PATH = os.path.join(PROJECT_PATH, "Templates").replace('\\', '/')
    ABS_TEMPLATES_JSON_PATH = os.path.join(ABS_TEMPLATES_PATH, "templates.json").replace('\\', '/')


class Website:
    PROJECT_PATH = os.getcwd().replace('\\', '/')
    ABS_RELEASE_PATH = os.path.join(PROJECT_PATH, "release").replace('\\', '/')
    ABS_DEV_PATH = os.path.join(PROJECT_PATH, "dev").replace('\\', '/')

    ABS_TEMPLATES_PATH = os.path.join(ABS_DEV_PATH, "Templates").replace('\\', '/')
    ABS_TEMPLATES_JSON_PATH = os.path.join(ABS_TEMPLATES_PATH, "templates.json").replace('\\', '/')
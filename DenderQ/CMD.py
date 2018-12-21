"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""


def intersects(l1, l2):
    return len(list(set(l1) & set(l2))) > 0


def get_optional_parameter(parameter_names: list, all_arguments: list):
    """optional parameters are arguments which are set with [parameter]=[value]"""
    for argument in all_arguments:
        for parameter_name in parameter_names:
            if "=" in argument and parameter_name == argument.split("=")[0]:
                return argument.split("=")[1]

    return None

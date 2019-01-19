"""
@author: Julian Sobott
@created: 10.01.2019
@brief:
@description:

@external_use:

@internal_use:

"""
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(message)s \t\t(%(filename)s %(lineno)d)')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
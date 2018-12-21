"""
@author: Julian Sobott
@created: 21.12.2018
@brief:
@description:

@external_use:

@internal_use:

"""
from setuptools import setup, find_packages

setup(
    name='DenderQ',
    version='0.1',
    description='Advances the workflow of website creation',
    url='https://github.com/JulianSobott/Website_creator',
    author='Julian Sobott',
    author_email='julian.sobott@gmx.de',
    license='Apache',
    packages=find_packages(),
    install_requires=['watchdog>=0.8.2'],
    package_data={
        '': ['Templates/*.json', 'Templates/website_includes/*.json', 'Templates/website_includes/*.html',
             'Templates/website_includes/*.py', 'Templates/website_includes/*.css']
    },
    include_package_data=True,
    keywords='website html include template',
    project_urls={
        "Bug Tracker": "https://github.com/JulianSobott/Website_creator/issues",
        "Documentation": "https://github.com/JulianSobott/Website_creator/wiki",
        "Source Code": "https://github.com/JulianSobott/Website_creator",
    }
)
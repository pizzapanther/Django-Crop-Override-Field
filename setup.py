import sys

from setuptools import setup, find_packages

setup(
    name = "crop_override",
    version = '12.04.2',
    description = "Field for predefined crops that when empty, falls back to original.",
    url = "https://github.com/pizzapanther/Django-Crop-Override-Field",
    author = "Paul Bailey",
    author_email = "paul.m.bailey@gmail.com",
    license = "BSD",
    packages = ['crop_override', 'crop_override.templatetags'],
    include_package_data = True,
)

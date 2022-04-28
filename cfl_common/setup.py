# -*- coding: utf-8 -*-
import re

import os
from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "portal/__init__.py"), "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="cfl-common",
    packages=find_packages(),
    version=version,
    include_package_data=True,
    install_requires=[
        "django==3.2.12",
        "djangorestframework==3.13.1",
        "django-two-factor-auth==1.13.2",
        "django-countries==7.3.1",
    ],
    tests_require=[],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

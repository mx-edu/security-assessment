#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/__init__.py
"""

import subprocess  # run

from core.tools import *
from core.terminal import *
from core.interface import *

# Attempt to import/install required Python packages.
for python_package in [
    "requests"
]:
    try:
        __import__(python_package)
    except ImportError:
        std_warning(f"Couldn't import {python_package}! Installing", end="...")
        subprocess.run(["pip", "install", python_package])

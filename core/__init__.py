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

# Attempt to import/install required packages.
for package in [
    "pyshark", "hashlib", "pymetasploit3"
]:
    try:
        __import__(package)
    except ImportError:
        std_warning(f"Couldn't import {package}! Installing", end="...")
        subprocess.run(["pip", "install", package])

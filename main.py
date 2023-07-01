#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: main.py
"""

import os  # _exit

from core import *


if __name__ == "__main__":
    interface = Interface()

    # Continually display the program menu and handle user input.
    while True:
        try:
            interface.display_menu()
            interface.handle_input()
        except KeyboardInterrupt:
            std_warning("CTRL-C detected! Exiting", start="\n", end="...")
            os._exit(0)

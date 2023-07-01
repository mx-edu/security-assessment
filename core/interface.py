#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/interface.py
"""

from core.handler import *
from core.terminal import *
from core.tools.util import clear_screen


class Interface:
    def __init__(self):
        self.options = {
            "1": ("Host Pinger", handle_pinger),
            "2": ("Host Scanner", handle_scanner),
            "3": ("Packet Sniffer", handle_sniffer),
            "4": ("Integrity Check", handle_file_checker)
        }

    def display_menu(self):
        """
        Displays all formatted options and their indexes from self.options.
        """

        # Clear the console screen.
        clear_screen()

        # Display the progams title ASCII.
        print(Term.ASCII_TITLE)

        # Iterate through the options menu (self.options).
        for i, option in self.options.items():
            # Print each options index and its display name.
            print(f"\t[{i}] {option[0]}")

    def handle_input(self):
        """
        Gets the users input from the console and handles it appropriately
        based on the callable handle functions from self.options.
        """

        # Get the users input.
        _in = std_input("Input (ex. 1)", start="\n")

        # Attempt to get the users choice from the options.
        if option := self.options.get(_in):
            # Parse and call the options handle function.
            option_handler = option[1]
            option_handler()

            std_input("Press any key to continue", start="\n", end="...")

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/tools/util.py
"""

import os  # system
import csv  # DictWriter


def defer(stop_func: callable) -> callable:
    """
    Deferral function decorator allowing for secondary functions to be
    called after the execution of the decorated function.
    """

    def decorator(main_func) -> callable:
        def wrapper(self, *args, **kwargs):
            # Call the decorated function with the passed parameters.
            main_func(self, *args, **kwargs)

            # Call the passed stop_func function after the execution of the
            # main decorated function has finished.
            stop_func(self)

        return wrapper

    return decorator


def write_scan_output(objects: list, headers: list, output_file: str = ""):
    """
    Writes the dictionary values of each of the passed objects to the
    output CSV file.
    """

    # If the passed output file to write to is invalid, exit the function.
    if not output_file:
        return

    # Open and write to the CSV file.
    with open(output_file, "w") as file_obj:
        # Create the CSV file writer.
        writer = csv.DictWriter(file_obj, headers)
        writer.writeheader()

        # Write a row in the file for each port.
        for obj in objects:
            writer.writerow(
                # If the list item is a dictionary, we can just write it
                # normally, otherwise write the objects __dict__ value.
                obj if isinstance(obj, dict) else obj.__dict__
            )


def clear_screen():
    """
    Clears the screen of the console by executing the 'clear' command.

    Cross-compatibility could be implemented here for other operating systems,
    but this is not done anywhere else in the program as it is intended for
    Linux distributions only.
    """

    os.system('clear')

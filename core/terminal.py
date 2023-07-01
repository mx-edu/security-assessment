#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/terminal.py
"""


class Term:
    """
    Colors/Headers for the programs terminal interface.
    """

    ASCII_TITLE = f"""
        Assessment Interface
        --------------------
    """

    HEADER = '\033[95m'
    YELLOW = '\033[33m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_start(start_text: str) -> None:
    # If the passed text is valid.
    if start_text:
        # Display it without a line ending.
        print(start_text, end="")


def std_input(text: str, start: str = "", end: str = " -> ") -> str:
    print_start(start)

    return input(
        f"[{Term.YELLOW}?{Term.ENDC}] {text}{end}",
    )


def std_success(text: str, start: str = "", end: str = "!") -> None:
    print_start(start)

    print(
        f"[{Term.OKGREEN}+{Term.ENDC}] {text}",
        end=end+'\n'
    )


def std_info(text: str, start: str = "", end: str = "...") -> None:
    print_start(start)

    print(
        f"[{Term.OKCYAN}*{Term.ENDC}] {text}", end=end+'\n'
    )


def std_warning(text: str, start: str = "", end: str = "!") -> None:
    print_start(start)

    print(
        f"[{Term.FAIL}!{Term.ENDC}] {text}", end=end+'\n'
    )


def std_error(text: str, start: str = "", error: Exception = None) -> None:
    print_start(start)

    print(
        f"[{Term.FAIL}!{Term.ENDC}] {text}! (error: {error})"
    )

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/tools/file_checker.py
"""

import subprocess # Popen, PIPE, STDOUT, CalledProcessError

from core.util import defer
from core.terminal import *


class FileChecker:
    """Performs a file integrity check using the debsums Linux command.

    Attributes:
        process: The debsums process running the integrity checking (subprocess).
    """

    def __init__(self):
        self.process = None

    @defer(
        # Execute the stop_integrity_check command after the execution
        # of perform_integrity_check has concluded.
        lambda self: self.stop_integrity_check()
    )
    def perform_integrity_check(self, display: bool=False):
        """Performs an integrity check on the local file system using debsums.

        Args:
            display: Whether to display checked files live. Defaults to False.
        """

        # Default debsums command.
        command = ["sudo", "debsums"]

        # If the user disabled the option to display the checked files.
        if not display:
            # Add the silent flag to the debsums command.
            command.append("-s")

        try:
            # Execute the constructed debsums command.
            self.process = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True)

            # Iterate through the live processes output.
            for i, line in enumerate(iter(self.process.stdout.readline, b'')):
                try:
                    # Split the raw line output so that parsing its attributes is possible.
                    columns = line.strip().split() # Format: columns[0] (filepath)... columns[-1] (status)
                    filepath, status = columns[0], columns[-1]
                except IndexError:
                    # Encountered an error when parsing or formatting the current raw line output.
                    continue

                # Print every OK file written to the processes STDOUT.
                # This will result in all checked files being displayed.
                if status == "OK":
                    std_info(
                        # Display the index and filepath of the checked file.
                        f"File #{i+1}: {filepath}"
                    )

            std_success("Finished checking files", start="\n")

        except KeyboardInterrupt:
            # Stop checking files as CTRL-C was pressed.
            std_success("Stopped checking files", start="\n")
            return

    def stop_integrity_check(self):
        """
        Stops the debsums file checker process.
        """

        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

        self.process = None

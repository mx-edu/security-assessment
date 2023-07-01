#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/sniffer.py
"""

import subprocess  # Popen, PIPE, STDOUT

from core.terminal import *
from core.tools.util import defer


class PacketSniffer:
    """Captures network packets using the tcpdump Linux command.

    Attributes:
        output_file: Where to store the tcpdump scan (pcap format).
        process: The tcpdump process running the packet sniffing (subprocess).
    """

    def __init__(self, output_file: str = ""):
        self.output_file = output_file
        self.process = None

    def construct_command(self, interface: str) -> list:
        """Constructs and returns the tcpdump command to be executed.

        Args:
            interface (str): Network interface to capture packets on.

        Returns:
            list: The constructed tcpdump command as a list of strings.
        """

        command = ["sudo", "tcpdump"]

        # If the interface isn't blank, add it to the command.
        if interface:
            # Add the tcpdump command flag (-i <interface>) to specify
            # the passed interface as the only one to capture packets on.
            command.extend(["-i", interface])

        # If the output file isn't blank, add it to the command.
        if self.output_file:
            # Add the tcpdump command flag (-w <file>) to specify the output
            # file to write the packet capturing information to (pcap format).
            command.extend(["-w", self.output_file])

        return command

    @defer(
        # Execute the stop_packet_capture command after the execution
        # of capture_packets_by_interface has concluded.
        lambda self: self.stop_packet_capture()
    )
    def capture_packets_by_interface(self, *options, display: bool = False):
        """Captures packets on the specified network interface.

        Args:
            *options: Options to configure the packet capture (e.g., interface).
            display (bool, optional): Whether to display captured packets live. Defaults to False.
        """

        # Construct the tcpdump command to use based on the passed options.
        command = self.construct_command(*options)

        try:
            # Execute the constructed tcpdump command.
            self.process = subprocess.Popen(command,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True)

            # If the user wants the packets to be displayed live.
            # Note that if the user also supplied an output file to be written
            # that no packets will be displayed to the screen, as all output is
            # directed to the passed output file instead.
            if display:
                std_info("Live packet display", start="\n", end=":")
                # Print every line written to the processes STDOUT.
                # This will result in all incoming packets being displayed.
                for line in iter(self.process.stdout.readline, b''):
                    std_info(line.strip())

        except KeyboardInterrupt:
            # Stop capturing packets as CTRL-C was pressed.
            std_success("Stopped capturing packets", start="\n", end="...")
            return

    def stop_packet_capture(self):
        """
        Stops the tcpdump packet capture process.
        """

        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

        self.process = None

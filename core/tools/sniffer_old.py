#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/sniffer_old.py
"""

# This file is deprecated and no longer used.
# sniffer.py includes the new code utilizing the tcpdump command.

import pcapy

from typing import List

from dataclasses import dataclass


@dataclass
class Packet:
    type: str
    timestamp: float
    data: bytes


class PacketSniffer:
    def __init__(self, output_file: str):
        self.packets: List[Packet] = []

        # Where to store the packet sniffers scan output.
        self.output_file = output_file

    def output_packets_to_file(self):
        with open(self.output_file, "w") as output_f:
            for packet in self.packets:
                output_f.write(f"{packet.__dict__}\n")

    def process_packet(self, *args, header=None, data=None):
        # Process the raw packet header into usable information.
        packet_type, time_processed = header.getts()[:2]

        # Create a new Packet object with the processed packet information.
        packet = Packet(
            type=packet_type,
            timestamp=time_processed,
            data=data,
        )

        # Append the newly created Packet object to the self.packets list.
        self.packets.append(packet)

    def capture_packets_by_interface(self, interface: str):
        # Open the passed interface.
        cap = pcapy.open_live(
            interface,  # Network device to open and listen to.
            65536,  # Maximum number of bytes to capture.
            True,  # Whether to run in promisc mode or not.
            0  # The read timeout in milliseconds.
        )

        # Set each packet captured to be processed by process_packet.
        cap.loop(
            10,  # Maximum number of packets to process before returning.
            self.process_packet  # Specifies the callback routine to pass the
            # processed packets information to.
            # Data send to the callback:
            #   - A header instance describing the data passed.
            #   - The packets data itself.
        )


if __name__ == "__main__":
    interface = "wlan0"
    output_file = "packets.txt"

    sniffer = PacketSniffer(output_file=output_file)
    while True:
        try:
            sniffer.capture_packets_by_interface(interface=interface)
        except KeyboardInterrupt:
            print("[!] Exiting...")
            break
        except Exception as error:
            print(f"[!] Failed to capture packets! (error: {error})")

    sniffer.output_packets_to_file()

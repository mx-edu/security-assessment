#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/handler.py
"""

from core.tools import *


def handle_pinger():
    """
    Handle inputs required for calling the ping_host function.
    """

    # Get required host input from the user.
    host = std_input(
        "Host to ping (ex. 1.1.1.1 or www.google.com)", start="\n")

    # Validate host address.
    if not host:
        std_error("Invalid host", error="blank input", start="\n")
        return

    std_info(f"Pinging {host}", start="\n")

    # Ping the host and print its status.
    host_status = ping_host(host)
    std_success("Host is " +
                ("online" if host_status else "offline"))


def handle_scanner():
    """
    Handle inputs required for initializing a new Scanner object and
    calling its scan_in_range function.
    """

    # Get required scanner inputs from the user.
    host = std_input(
        "Host to scan (ex. 1.1.1.1 or www.google.com)", start="\n")
    range_start = std_input("Port range start (ex. 80)")
    range_end = std_input("Port range end (ex. 9000)")
    output_file = std_input(
        "CSV output file (ex. scan.csv) (leave blank for none)")

    # Validate the supplied start and end port range.
    try:
        # Attempt to convert the port range strings to integers.
        start = int(range_start)
        end = int(range_end)
    except:
        std_error("Invalid range", error="only int accepted", start="\n")
        return

    # Validate that the port ranges are valid.
    # (Scannable ports are in the range of 1-65535).
    if 1 > start < 65534 or 2 > end < 65535:
        std_error("Invalid range", error="only 1-65545 accepted", start="\n")
        return

    # Validate that the supplied host is up.
    if not ping_host(host):
        std_warning("Host is down! Cannot scan", start="\n", end="...")
        return

    std_info("Host is up! Starting scan", start="\n")

    try:
        # Create a new Scanner object with the host the user wants to scan and the
        # output file the scan results should be written to (default=scan.csv).
        scanner = Scanner(host, output_file)

        # Use the scan_in_range function with the passed user inputs to scan the range.
        scanner.scan_in_range(start, end)

        # Display the range of ports scanned.
        std_success(f"Finished scanning {end-start} ports", start="\n\n")

        # Display where the scan was saved if configured to.
        if output_file:
            std_info(f"Host scan written to {output_file}")

        # Give the user the option to display all open ports from the previous host scan.
        if std_input("Display open ports? (y/n)", start="\n") == "y":
            # Print the open port table header.
            std_info("Open ports table", end=":")
            print("ID\tPort\tStatus")

            # Enumerate through the scanned ports and display the ones
            # with an open status (Port.status).
            for i, port in enumerate(scanner.ports):
                if port.status:
                    print(f"{i+1}\t{port.port}\tOpen")

    except Exception as error:
        # Unknown error encountered.
        print(f"[!] Failed to scan host... (error: {error})")


def handle_sniffer():
    """
    Handle inputs required for initializing a new PacketSniffer object and
    calling its capture_packets_by_interface function.
    """

    # Get required scanner inputs from the user.
    interface = std_input(
        "Interface to capture (ex. wlan0) (leave blank for all)", start="\n")
    output_file = std_input(
        "PCAP output file (ex. output.pcap) (leave blank for none)")

    try:
        std_info("Attempting to capture packets", start="\n")
        std_info("Press CTRL-C to stop listening")

        # Create a new PacketSniffer object.
        sniffer = PacketSniffer(output_file)

        # Use the capture_packets_by_interface function with the passed user input
        # of the interface to scan.
        sniffer.capture_packets_by_interface(interface, display=True)

    # KeyboardInterrupt Exception is handled when capturing the packets.
    except Exception as error:
        # Unknown error encountered.
        std_error("Failed to capture packets", error=error)


def handle_report_generator():
    """
    Handle inputs required for calling the generate_report function.
    """

    # Get required report inputs from the user.
    output_file = std_input("Report file (ex. report.csv)", start="\n")

    std_error("This function is incomplete")

    return output_file

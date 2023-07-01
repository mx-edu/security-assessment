#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/tools/scanner.py
"""

import socket  # setdefaulttimeout, socket, connect_ex

from queue import Queue
from threading import Thread
from datetime import datetime

from core.terminal import *
from core.tools.util import write_scan_output

THREADS = 20  # Maximum number of threads to run similtaneously.
SOCKET_TIMEOUT = 0.1  # How long to wait before stopping the connection
# to one of the hosts ports (in seconds).


class Port:
    """Represents a network port to be scanned.

    Attributes:
        host: The parent host the port belongs to.
        port: The target port to be scanned on the host.
        time: The time (datetime) the port was scanned.
        status: Whether the port was open or not.
    """

    def __init__(
        self,
        host: str,
        port: int,
        time: datetime = datetime.now(),
        status: bool = False
    ):
        self.host = host
        self.port = port
        self._time = time
        self.status = status

    @property
    def time(self, format: str = "%H:%M:%S") -> str:
        """Returns the formatted version of the ports scanned time.

        Args:
            format: Formatting string to pass to datetime.strftime.

        Returns:
            str: The formatted datetime based on the specified format.
        """

        return self._time.strftime(format)

    @time.setter
    def time(self, new_time: datetime) -> str:
        """Sets a new scanned time for the port.

        Args:
            new_time: New datetime instance to replace the old one with.
        """

        # Verify that the new time is a valid datetime object.
        if isinstance(new_time, datetime):
            self._time = new_time


class Scanner:
    """Scans a host for open ports using multiple threads and queues.

    Attributes:
        ports: Storage for the scanned ports (Port objects).
        total_open: A counter to store the amount of open ports.
        host: The host to scan the ports of.
        output_file: Where to write the scanned ports (if not blank).
        queue: The queue to manage the latest ports for threads to use.
    """

    def __init__(self, host: str, output_file: str):
        """Initializes a Scanner object."""

        self.ports = []
        self.formatted_ports = [{}]
        self.total_open = 0

        self.host = host
        self.output_file = output_file

        self.queue = Queue()

    @staticmethod
    def get_sock_connection() -> socket.socket:
        """Creates, configures and returns a socket connection used for scanning.

        Returns:
            socket.socket: The socket to use when scanning a host.
        """

        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def format_ports(self) -> list:
        """Formats the list of ports into a list of dictionaries.
           This is only used for passing the list of ports to the CSV writer.

        Returns:
            list: A list of dictionaries containing the formatted port data.
        """

        return [
            {
                # Removes the port._time/time attribute.
                "host": port.host,
                "port": port.port,
                "status": port.status
            }
            for port in self.ports
        ]

    def scan_port(self, port: Port) -> Port:
        """Uses a socket connection to test if the passed hosts port is open
           by attempting to connect to it with a set timeout to stop invalid connections.

        Args:
            Port: The Port object to scan, modify and return.

        Returns:
            Port: The modified Port object (changed whether it was open or not).
        """

        # Set the time that the port was scanned to the current time.
        port.time = datetime.now()

        # Create and configure the socket connection with a timeout to stop
        # any ports that it failed to connect to in SOCKET_TIMEOUT seconds (default=0.5).
        sock = self.get_sock_connection()
        sock.settimeout(SOCKET_TIMEOUT)

        try:
            # Attempt to connect to the host through the Port object's port.
            conn_result = sock.connect_ex((port.host, port.port))

            # socket.connect_ex success code is 0.
            if conn_result == 0:
                # The port is open, and the Port object's status can be set to True.
                port.status = True

        except socket.error:
            # Handle socket errors (e.g., connection refused).
            # Assume that the port is closed.
            port.status = False
        finally:
            sock.close()  # Close the opened socket.

            # Return the modified or unmodified Port object.
            return port

    def worker(self):
        """
        Worker function executed by each thread to continually scan the latest
        ports from the queue, automatically exits when there are no more ports to scan.
        """

        # Continually scan and append the latest port in the queue.
        while True:
            # Retrieve the latest available port in the queue.
            latest_port = self.queue.get()

            # Append the scanned port to the self.ports array.
            self.ports.append(
                result := self.scan_port(latest_port)
            )

            if result.status:
                # If the previously scanned port was open,
                # increment the self.total_open counter.
                self.total_open += 1

            # Display the port in a table format.
            print(
                f"{result.time}\t{result.port}\t{result.status}\t{self.total_open}", end='\r')

            # Tell the queue that this task has completed.
            self.queue.task_done()

    def scan_in_range(self, start: int, end: int):
        """Scans the predefined host between the passed range of ports (start-end).

        Args:
            start (int): The port to begin the port scanning.
            end (int): The port to stop the port scanning.
        """

        # Display the table headers for the ports to be scanned.
        std_info("Live Scan Table", start="\n", end=":")
        print("Time Scanned\tPort\tStatus\tTotal Open")

        # Create and start THREADS amount of threads for self.worker.
        for i in range(THREADS):
            thread = Thread(target=self.worker)
            thread.daemon = True
            thread.start()

        # Iterate through the passed range of ports.
        for i in range(start, end + 1):
            # Create a Port object containing the current ports attributes
            port = Port(self.host, i)

            # Add the created port to the queue for it to be scanned.
            self.queue.put(port)

        # Wait for all tasks in the queue to complete.
        self.queue.join()

        # Sort the scanned ports in the order of their ids.
        # This is required as using threading doesn't scan them in their original order.
        self.formatted_ports = sorted(
            self.format_ports(),
            # Sort the ports by their port number.
            key=lambda port: port.get('port')
        )

        # Write the sorted scanned ports list to the output file.
        write_scan_output(objects=self.formatted_ports,  # List of objects to write to the CSV file.
                          # Headers to use in the CSV file.
                          headers=["host", "port", "status"],
                          output_file=self.output_file)  # File path to write to.

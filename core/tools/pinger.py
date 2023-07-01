#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  Max
    @package: core/tools/pinger.py
"""

import subprocess  # run, PIPE


def ping_host(host: str) -> bool:
    """Sends a ping request to the passed host address using subprocess.

    Args:
        host: The host to send the ping request to.

    Returns:
        bool: Whether the host responded to the ping request (True) or not (False).
    """

    # Create and execute the constructed subprocess command.
    ping = subprocess.run(
        ["ping", "-c", "1", host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Return whether the host replied to the request or not (0 = success code).
    return ping.returncode == 0

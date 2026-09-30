#!/usr/bin/env python3
"""Supervisor-owned, one-shot FD mapper that immediately execs Bubblewrap."""
from __future__ import annotations

import fcntl
import os
import sys


CHANNEL_TARGETS = (3, 4, 5, 6)
ARGUMENT_TARGET = 7
TEMP_FD_MINIMUM = 64


def main() -> int:
    if len(sys.argv) < 4:
        os.write(2, b"observer exec helper: expected channel fds, args fd, and Bubblewrap argv\n")
        return 126

    try:
        channel_fds = tuple(int(item) for item in sys.argv[1].split(","))
        argument_fd = int(sys.argv[2])
        bubblewrap_argv = sys.argv[3:]
        if (len(channel_fds) != len(CHANNEL_TARGETS) or len(set(channel_fds)) != len(channel_fds)
                or argument_fd in channel_fds or argument_fd < 0
                or not bubblewrap_argv or bubblewrap_argv[1:3] != ["--args", str(ARGUMENT_TARGET)]):
            raise ValueError("descriptor mapping does not match the reviewed observer launch")

        sources = (*channel_fds, argument_fd)
        copies = [fcntl.fcntl(fd, fcntl.F_DUPFD_CLOEXEC, TEMP_FD_MINIMUM) for fd in sources]
        for copied, target in zip(copies[:len(CHANNEL_TARGETS)], CHANNEL_TARGETS):
            os.dup2(copied, target, inheritable=True)
        os.dup2(copies[-1], ARGUMENT_TARGET, inheritable=True)

        for copied in copies:
            os.close(copied)
        target_fds = set(CHANNEL_TARGETS) | {ARGUMENT_TARGET}
        for fd in set(sources):
            if fd not in target_fds:
                os.close(fd)

        os.execv(bubblewrap_argv[0], bubblewrap_argv)
    except (OSError, ValueError) as exc:
        os.write(2, f"observer exec helper failed: {type(exc).__name__}: {exc}\n".encode())
        return 126

    return 126


if __name__ == "__main__":
    raise SystemExit(main())

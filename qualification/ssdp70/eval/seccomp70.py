#!/usr/bin/env python3
"""Seccomp-BPF filters for the Stage F OMP subject and provider observer (x86-64).

Defense in depth for the descriptor-bound transport: the relay's non-dumpable memory and the
OMP process are protected from sibling sandbox processes by Yama ptrace scope AND by this
filter, so the isolation does not depend on a host sysctl. It denies the syscalls a sibling
process would use to read another process's memory or duplicate its descriptors, plus kernel
attack surface the qualification workload never needs. The subject filter also refuses creation
of AF_UNIX sockets while preserving the two authorized loopback TCP endpoints. The observer
filter is installed after it acquires one provider-route socket capability, then refuses new
sockets/connections and addressed sends. These filters complement, but do not replace, the
namespace, explicit filesystem view, and descriptor-bound transport.
"""
from __future__ import annotations

import struct

AUDIT_ARCH_X86_64 = 0xC000003E
SECCOMP_RET_ALLOW = 0x7FFF0000
SECCOMP_RET_KILL_PROCESS = 0x80000000
SECCOMP_RET_ERRNO = 0x00050000
EPERM = 1

BPF_LD, BPF_W, BPF_ABS, BPF_JMP, BPF_JEQ, BPF_K, BPF_RET = 0x00, 0x00, 0x20, 0x05, 0x10, 0x00, 0x06
SECCOMP_DATA_NR = 0
SECCOMP_DATA_ARCH = 4
SECCOMP_DATA_ARGS = 16
AF_UNIX = 1

# x86-64 syscall numbers
DENIED_SYSCALLS = {
    "ptrace": 101,
    "process_vm_readv": 310,
    "process_vm_writev": 311,
    "kcmp": 312,
    "pidfd_open": 434,
    "pidfd_getfd": 438,
    "userfaultfd": 323,
    "perf_event_open": 298,
    "bpf": 321,
    "add_key": 248,
    "request_key": 249,
    "keyctl": 250,
    "kexec_load": 246,
    "kexec_file_load": 320,
    "init_module": 175,
    "finit_module": 313,
    "delete_module": 176,
    "reboot": 169,
    "swapon": 167,
    "swapoff": 168,
    "acct": 163,
    "open_by_handle_at": 304,
    "name_to_handle_at": 303,
    "mount": 165,
    "umount2": 166,
    "pivot_root": 155,
    "chroot": 161,
    "syslog": 103,
    "iopl": 172,
    "ioperm": 173,
}


def _insn(code: int, jt: int, jf: int, k: int) -> bytes:
    return struct.pack("HBBI", code, jt, jf, k)


def _header() -> list[bytes]:
    return [
        _insn(BPF_LD | BPF_W | BPF_ABS, 0, 0, SECCOMP_DATA_ARCH),
        _insn(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, AUDIT_ARCH_X86_64),
        _insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_KILL_PROCESS),
        _insn(BPF_LD | BPF_W | BPF_ABS, 0, 0, SECCOMP_DATA_NR),
    ]


def _deny_numbers(table: dict[str, int]) -> list[bytes]:
    program: list[bytes] = []
    for number in sorted(set(table.values())):
        program.extend((
            _insn(BPF_JMP | BPF_JEQ | BPF_K, 0, 1, number),
            _insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ERRNO | EPERM),
        ))
    return program


def build_deny_filter(names: dict[str, int] | None = None) -> bytes:
    """Deny process-inspection/privilege syscalls and AF_UNIX socket creation in OMP."""
    table = DENIED_SYSCALLS if names is None else names
    program = _header() + _deny_numbers(table)
    # socket(domain, type, protocol): AF_UNIX cannot reach host pathname or abstract sockets.
    # Other domains remain subject to the isolated loopback-only network namespace.
    program.extend((
        _insn(BPF_JMP | BPF_JEQ | BPF_K, 0, 3, 41),  # socket; non-socket -> final allow
        _insn(BPF_LD | BPF_W | BPF_ABS, 0, 0, SECCOMP_DATA_ARGS),
        _insn(BPF_JMP | BPF_JEQ | BPF_K, 0, 1, AF_UNIX),
        _insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ERRNO | EPERM),
        _insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ALLOW),
    ))
    return b"".join(program)


OBSERVER_DENIED_SYSCALLS = {
    **DENIED_SYSCALLS,
    "socket": 41,
    "connect": 42,
    "accept": 43,
    "bind": 49,
    "listen": 50,
    "socketpair": 53,
    "accept4": 288,
    "sendto": 44,
    "recvfrom": 45,
    "sendmsg": 46,
    "recvmsg": 47,
    "sendmmsg": 307,
    "recvmmsg": 299,
    "execve": 59,
    "execveat": 322,
    "kill": 62,
    "tkill": 200,
    "tgkill": 234,
    "pidfd_send_signal": 424,
    "io_uring_setup": 425,
    "io_uring_enter": 426,
    "io_uring_register": 427,
    "setns": 308,
    "unshare": 272,
}


def build_observer_filter() -> bytes:
    """Lock the observer to its already-connected route and evidence/pipe descriptors.

    Connected-stream send/receive use sendto/recvfrom with null address pointers on CPython.
    Those connected-stream forms are allowed; non-null address pointers and vectored network
    operations are denied so the socket cannot be retargeted as an egress path.
    """
    table = {name: number for name, number in OBSERVER_DENIED_SYSCALLS.items()
             if name not in ("sendto", "recvfrom")}
    program = _header() + _deny_numbers(table)
    # For sendto, sockaddr is argument 4. For recvfrom, both sockaddr and socklen pointers
    # (arguments 4 and 5) must be null. Each pointer is checked as both 32-bit words.
    for name, pointer_args in (("sendto", (4,)), ("recvfrom", (4, 5))):
        syscall = OBSERVER_DENIED_SYSCALLS[name]
        pointer_words = 2 * len(pointer_args)
        program.append(_insn(BPF_JMP | BPF_JEQ | BPF_K, 0, pointer_words * 3 + 1, syscall))
        for argument in pointer_args:
            for offset in (SECCOMP_DATA_ARGS + argument * 8, SECCOMP_DATA_ARGS + argument * 8 + 4):
                program.extend((
                    _insn(BPF_LD | BPF_W | BPF_ABS, 0, 0, offset),
                    _insn(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, 0),
                    _insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ERRNO | EPERM),
                ))
        program.append(_insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ALLOW))
    program.append(_insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ALLOW))
    return b"".join(program)

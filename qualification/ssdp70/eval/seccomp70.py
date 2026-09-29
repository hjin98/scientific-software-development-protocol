#!/usr/bin/env python3
"""Minimal seccomp-BPF deny filter for the subject sandbox (x86-64).

Defense in depth for the descriptor-bound transport: the relay's non-dumpable memory and the
OMP process are protected from sibling sandbox processes by Yama ptrace scope AND by this
filter, so the isolation does not depend on a host sysctl. It denies the syscalls a sibling
process would use to read another process's memory or duplicate its descriptors, plus kernel
attack surface the qualification workload never needs. All other syscalls stay allowed: this
is a hardening layer, not the containment boundary (namespaces, the empty filesystem view and
the descriptor-bound transport are).
"""
from __future__ import annotations

import struct

AUDIT_ARCH_X86_64 = 0xC000003E
SECCOMP_RET_ALLOW = 0x7FFF0000
SECCOMP_RET_KILL_PROCESS = 0x80000000
SECCOMP_RET_ERRNO = 0x00050000
EPERM = 1

BPF_LD, BPF_W, BPF_ABS, BPF_JMP, BPF_JEQ, BPF_K, BPF_RET = 0x00, 0x00, 0x20, 0x05, 0x10, 0x00, 0x06

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


def build_deny_filter(names: dict[str, int] | None = None) -> bytes:
    table = DENIED_SYSCALLS if names is None else names
    numbers = sorted(set(table.values()))
    program = [
        _insn(BPF_LD | BPF_W | BPF_ABS, 0, 0, 4),                       # arch
        _insn(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, AUDIT_ARCH_X86_64),
        _insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_KILL_PROCESS),
        _insn(BPF_LD | BPF_W | BPF_ABS, 0, 0, 0),                       # syscall nr
    ]
    for number in numbers:
        program.append(_insn(BPF_JMP | BPF_JEQ | BPF_K, 0, 1, number))
        program.append(_insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ERRNO | EPERM))
    program.append(_insn(BPF_RET | BPF_K, 0, 0, SECCOMP_RET_ALLOW))
    return b"".join(program)

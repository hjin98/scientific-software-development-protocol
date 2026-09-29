#!/usr/bin/env python3
"""Descriptor-bound request/response transport between the subject relay and a principal.

The subject/executor's only routes to the provider-control/observation principal and to the
qualification MCP bridge are two anonymous pipe pairs. Each pair is inherited by exactly one
supervisor-launched principal and by the in-sandbox launcher; there is no filesystem socket,
no TCP port on the host and no bearer token to steal, so authority is bound to the run
instance's inherited descriptors rather than to a path or an executable identity.

Framing is `>BII` (type, connection id, payload length) followed by the payload. One virtual
connection carries one HTTP/1.1 request and its (possibly streamed) response.
"""
from __future__ import annotations

import os
import queue
import struct
import threading
from typing import Callable

OPEN, DATA, CLOSE = 1, 2, 3
HEADER = struct.Struct(">BII")
MAX_PAYLOAD = 64 * 1024
MAX_HEADER_BYTES = 64 * 1024
MAX_BODY_BYTES = 256 * 1024 * 1024


class Conn:
    def __init__(self, mux: "Mux", cid: int):
        self.mux = mux
        self.cid = cid
        self._q: "queue.Queue[bytes | None]" = queue.Queue()
        self._buf = b""
        self._remote_closed = False
        self._closed = False

    # ---- receiving
    def _feed(self, data: bytes | None) -> None:
        self._q.put(data)

    def recv(self, timeout: float | None = None) -> bytes:
        if self._remote_closed:
            return b""
        try:
            data = self._q.get(timeout=timeout)
        except queue.Empty:
            raise TimeoutError("virtual connection read timed out")
        if data is None:
            self._remote_closed = True
            return b""
        return data

    def read_until(self, marker: bytes, limit: int) -> bytes | None:
        while marker not in self._buf:
            if len(self._buf) > limit:
                return None
            chunk = self.recv()
            if not chunk:
                return None
            self._buf += chunk
        head, _, rest = self._buf.partition(marker)
        self._buf = rest
        return head

    def read_exact(self, count: int) -> bytes | None:
        while len(self._buf) < count:
            chunk = self.recv()
            if not chunk:
                return None
            self._buf += chunk
        data, self._buf = self._buf[:count], self._buf[count:]
        return data

    def read_line(self) -> bytes | None:
        line = self.read_until(b"\r\n", MAX_HEADER_BYTES)
        return line

    # ---- sending
    def sendall(self, data: bytes) -> None:
        for start in range(0, len(data), MAX_PAYLOAD):
            self.mux._send(DATA, self.cid, data[start:start + MAX_PAYLOAD])

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self.mux._send(CLOSE, self.cid)


class Mux:
    def __init__(self, read_fd: int, write_fd: int, on_open: Callable[[Conn], None] | None = None):
        self._rfile = os.fdopen(read_fd, "rb", buffering=0)
        self._wfd = write_fd
        self._wlock = threading.Lock()
        self._conns: dict[int, Conn] = {}
        self._clock = threading.Lock()
        self._next = 1
        self._on_open = on_open
        self.alive = True

    def start(self) -> None:
        threading.Thread(target=self._reader, daemon=True).start()

    def _send(self, ftype: int, cid: int, payload: bytes = b"") -> None:
        frame = HEADER.pack(ftype, cid, len(payload)) + payload
        with self._wlock:
            view = memoryview(frame)
            try:
                while view:
                    view = view[os.write(self._wfd, view):]
            except OSError:
                self.alive = False

    def _read_exact(self, count: int) -> bytes | None:
        chunks = []
        remaining = count
        while remaining:
            chunk = self._rfile.read(remaining)
            if not chunk:
                return None
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def _reader(self) -> None:
        while True:
            header = self._read_exact(HEADER.size)
            if header is None:
                break
            ftype, cid, length = HEADER.unpack(header)
            payload = self._read_exact(length) if length else b""
            if payload is None or length > MAX_PAYLOAD:
                break
            if ftype == OPEN:
                conn = Conn(self, cid)
                with self._clock:
                    self._conns[cid] = conn
                if self._on_open is not None:
                    threading.Thread(target=self._on_open, args=(conn,), daemon=True).start()
            elif ftype == DATA:
                conn = self._conns.get(cid)
                if conn is not None:
                    conn._feed(payload)
            elif ftype == CLOSE:
                with self._clock:
                    conn = self._conns.pop(cid, None)
                if conn is not None:
                    conn._feed(None)
        self.alive = False
        with self._clock:
            conns = list(self._conns.values())
            self._conns.clear()
        for conn in conns:
            conn._feed(None)

    def open(self) -> Conn:
        with self._clock:
            cid = self._next
            self._next += 1
            conn = Conn(self, cid)
            self._conns[cid] = conn
        self._send(OPEN, cid)
        return conn


# --------------------------------------------------------------------------- HTTP subset

class Request:
    def __init__(self, method: str, target: str, headers: dict[str, str], body: bytes, raw_head: bytes):
        self.method = method
        self.target = target
        self.headers = headers
        self.body = body
        self.raw_head = raw_head

    @property
    def path(self) -> str:
        return self.target.split("?", 1)[0]


def read_request(conn: Conn) -> Request | None:
    head = conn.read_until(b"\r\n\r\n", MAX_HEADER_BYTES)
    if head is None:
        return None
    lines = head.decode("latin-1").split("\r\n")
    try:
        method, target, _version = lines[0].split(" ", 2)
    except ValueError:
        return None
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            return None
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()
    body = b""
    if headers.get("transfer-encoding", "").lower() == "chunked":
        parts = []
        total = 0
        while True:
            size_line = conn.read_line()
            if size_line is None:
                return None
            try:
                size = int(size_line.split(b";")[0], 16)
            except ValueError:
                return None
            if size == 0:
                conn.read_until(b"\r\n", MAX_HEADER_BYTES)
                break
            total += size
            if total > MAX_BODY_BYTES:
                return None
            chunk = conn.read_exact(size)
            if chunk is None:
                return None
            parts.append(chunk)
            conn.read_exact(2)
        body = b"".join(parts)
    elif "content-length" in headers:
        if not headers["content-length"].isdigit() or int(headers["content-length"]) > MAX_BODY_BYTES:
            return None
        length = int(headers["content-length"])
        got = conn.read_exact(length) if length else b""
        if got is None:
            return None
        body = got
    return Request(method, target, headers, body, head)


REASONS = {200: "OK", 202: "Accepted", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found",
           405: "Method Not Allowed", 411: "Length Required", 500: "Internal Server Error",
           502: "Bad Gateway"}


def send_head(conn: Conn, status: int, headers: dict[str, str], content_length: int | None) -> None:
    lines = [f"HTTP/1.1 {status} {REASONS.get(status, 'Status')}"]
    for name, value in headers.items():
        lines.append(f"{name}: {value}")
    if content_length is not None:
        lines.append(f"content-length: {content_length}")
    lines.append("connection: close")
    conn.sendall(("\r\n".join(lines) + "\r\n\r\n").encode("latin-1"))


def send_simple(conn: Conn, status: int, body: bytes = b"", content_type: str | None = None,
                extra: dict[str, str] | None = None) -> None:
    headers = dict(extra or {})
    if content_type:
        headers["content-type"] = content_type
    send_head(conn, status, headers, len(body))
    if body:
        conn.sendall(body)

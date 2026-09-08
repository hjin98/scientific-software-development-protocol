"""Finite bounds applied to every externally influenced read.

Every limit here guards a surface where malformed or hostile input could otherwise
exhaust memory, file descriptors, or wall-clock time. Readers reject *before*
materializing an oversized payload rather than truncating it silently, because a
truncated document would produce a confident but wrong identity.
"""

from __future__ import annotations

# Configuration
MAX_CONFIG_BYTES = 1 << 20  # 1 MiB
MAX_CONFIG_PROJECTS = 512
MAX_CONFIG_EXTENSION_NAMESPACES = 256
MAX_CONFIG_EXTENSION_BYTES = 1 << 18  # per-namespace serialized bound
MAX_CONFIG_NESTING = 16

# Workplan catalog
MAX_WORKPLAN_BYTES = 4 << 20  # 4 MiB
MAX_WORKPLAN_FRONTMATTER_BYTES = 1 << 18
MAX_WORKPLAN_FRONTMATTER_TOKENS = 65536
MAX_WORKPLAN_FRONTMATTER_DEPTH = 12
MAX_WORKPLAN_FILES = 4096
MAX_WORKPLAN_DEPTH = 8
WORKPLAN_SUFFIXES = (".md", ".markdown", ".txt")

# Protocol source
MAX_PROTOCOL_SOURCE_BYTES = 8 << 20  # 8 MiB
MAX_PROTOCOL_PROFILE_BYTES = 1 << 20

# Git subprocess / remote query
GIT_TIMEOUT_SECONDS = 20.0
GIT_REMOTE_TIMEOUT_SECONDS = 30.0
MAX_GIT_OUTPUT_BYTES = 8 << 20
MAX_DIRTY_PATHS = 5000
MAX_DIRTY_FILE_BYTES = 32 << 20
MAX_DIRTY_CONTENT_BYTES = 128 << 20

# Remote protocol reads
MAX_REMOTE_READ_BYTES = 8 << 20
REMOTE_READ_TIMEOUT_SECONDS = 60.0

# Prompt input scalars
MAX_INPUT_VALUE_BYTES = 1 << 16  # 64 KiB per declared INPUT value
MAX_INPUT_OVERRIDES = 64

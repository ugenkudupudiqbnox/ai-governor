from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AuditSinkError(Exception):
    """Raised when an audit sink fails."""


class AuditSink(ABC):
    """
    Abstract base class for audit sinks.

    Sinks MUST be append-only and side-effect free
    with respect to enforcement logic.
    """

    @abstractmethod
    def write(self, event: Dict[str, Any]) -> None:
        pass


class StdoutSink(AuditSink):
    """
    Writes audit events to stdout.

    Failure behavior:
    - Exceptions propagate (fail-fast)
    """

    def write(self, event: Dict[str, Any]) -> None:
        print(json.dumps(event, sort_keys=True), flush=True)


class JsonFileSink(AuditSink):
    """
    Writes audit events as JSON Lines to a file.

    Guarantees:
    - One event per line
    - Append-only
    - Flush after every write (default)

    Failure behavior:
    - By default, raises AuditSinkError
    """

    def __init__(
        self,
        path: str,
        *,
        flush: bool = True,
        fsync: bool = False,
        fail_fast: bool = True,
    ):
        self.path = path
        self.flush = flush
        self.fsync = fsync
        self.fail_fast = fail_fast

    def write(self, event: Dict[str, Any]) -> None:
        try:
            line = json.dumps(event, sort_keys=True) + "\n"

            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line)

                if self.flush:
                    f.flush()

                if self.fsync:
                    os.fsync(f.fileno())

        except Exception as e:
            if self.fail_fast:
                raise AuditSinkError(
                    f"Failed to write audit event to {self.path}: {e}"
                )


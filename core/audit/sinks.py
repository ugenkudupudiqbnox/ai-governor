from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Dict


class AuditSink(ABC):
    """
    Abstract base class for audit sinks.
    """

    @abstractmethod
    def write(self, event: Dict[str, Any]) -> None:
        pass


class StdoutSink(AuditSink):
    """
    Writes audit events to stdout (default).
    """

    def write(self, event: Dict[str, Any]) -> None:
        print(json.dumps(event, sort_keys=True))


class JsonFileSink(AuditSink):
    """
    Writes audit events as JSON Lines to a file.

    One event per line, append-only.
    """

    def __init__(self, path: str):
        self.path = path

    def write(self, event: Dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")


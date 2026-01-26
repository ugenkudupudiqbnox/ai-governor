import tempfile
import os
import pytest

from core.audit.sinks import JsonFileSink, AuditSinkError


def test_file_sink_writes_and_flushes():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        path = f.name

    sink = JsonFileSink(path, flush=True)
    sink.write({"event": "test"})

    with open(path) as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert "test" in lines[0]

    os.remove(path)


def test_file_sink_fail_fast():
    sink = JsonFileSink("/invalid/path/audit.jsonl", fail_fast=True)

    with pytest.raises(AuditSinkError):
        sink.write({"event": "test"})


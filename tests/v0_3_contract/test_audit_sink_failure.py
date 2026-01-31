
from core.audit.emitter import AuditEventEmitter
from core.enforcement.orchestrator import EnforcementOrchestrator
import pytest

class FailingSink:
    def emit(self, event):
        raise RuntimeError("sink failure")

def test_audit_sink_failure_blocks_execution():
    emitter = AuditEventEmitter(sinks=[FailingSink()])
    orchestrator = EnforcementOrchestrator(audit_emitter=emitter)

    with pytest.raises(Exception):
        orchestrator.enforce(
            {"version": "0.1"},
            requested_model="gpt-4.1",
            text="hello"
        )

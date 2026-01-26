import json
import tempfile

from core.audit.emitter import AuditEventEmitter
from core.audit.sinks import JsonFileSink
from core.decision import Decision


def test_json_file_sink_writes_event():
    with tempfile.NamedTemporaryFile() as f:
        emitter = AuditEventEmitter(
            sinks=[JsonFileSink(f.name)]
        )

        decision = Decision.allow(
            reason="test",
            policy_section="model",
        )

        emitter.emit(decision)

        f.seek(0)
        line = f.readline().decode()
        data = json.loads(line)

        assert data["decision"] == "ALLOW"
        assert data["policy_section"] == "model"


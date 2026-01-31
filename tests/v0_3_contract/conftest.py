
import pytest
from core.enforcement.orchestrator import EnforcementOrchestrator

@pytest.fixture
def orchestrator():
    return EnforcementOrchestrator()

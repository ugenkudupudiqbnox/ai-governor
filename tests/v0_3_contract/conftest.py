# DO NOT MODIFY — v0.3 CONTRACT TEST

import pytest
from core.enforcement.orchestrator import EnforcementOrchestrator

@pytest.fixture
def orchestrator():
    return EnforcementOrchestrator()

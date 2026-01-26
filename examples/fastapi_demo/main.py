"""
FastAPI demo for ai-governor

This is an EXAMPLE ONLY.
No real LLM calls are made.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml

from core.enforcement.orchestrator import EnforcementOrchestrator
from core.decision import DecisionType

app = FastAPI(title="ai-governor FastAPI Demo")

# Load policy once (static for demo)
with open("policy.yaml") as f:
    POLICY = yaml.safe_load(f)

orchestrator = EnforcementOrchestrator()


class GenerateRequest(BaseModel):
    model: str
    region: str | None = None
    tool: str | None = None
    prompt: str


@app.post("/generate")
def generate(req: GenerateRequest):
    result = orchestrator.enforce(
        policy=POLICY,
        requested_model=req.model,
        region=req.region,
        tool_name=req.tool,
        text=req.prompt,
        context={
            "source": "fastapi-demo",
            "endpoint": "/generate",
        },
    )

    decision = result["final_decision"]

    if decision.decision == DecisionType.BLOCK:
        raise HTTPException(
            status_code=403,
            detail={
                "decision": decision.decision.value,
                "reason": decision.reason,
            },
        )

    if decision.decision == DecisionType.MODIFY:
        return {
            "decision": "MODIFY",
            "output": result["output_text"],
        }

    # ALLOW — simulate model output
    return {
        "decision": "ALLOW",
        "output": "Simulated LLM response (demo only)",
    }


# FastAPI Demo (Example Only)

This directory contains a **non-production FastAPI example**
showing how ai-governor can be integrated into an HTTP API.

## Important Notes

- This demo is NOT part of ai-governor’s stable API
- It is excluded from v0.3 stability guarantees
- No real LLM calls are made
- Governance happens BEFORE any model invocation

## Run the Demo

```bash
pip install fastapi uvicorn pyyaml
uvicorn main:app --reload

---

## Optional: REST Client Examples

### `examples/fastapi_demo/requests.http`

```http
POST http://127.0.0.1:8000/generate
Content-Type: application/json

{
  "model": "gpt-4.1",
  "region": "IN",
  "prompt": "Hello"
}


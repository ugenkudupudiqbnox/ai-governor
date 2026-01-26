curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "region": "IN",
    "prompt": "Email me at test@example.com"
  }'


#!/bin/bash
aws lambda invoke \
  --function-name TextHasherFunction \
  --payload "${1:-'{"text": "Hello, World!", "algorithm": "sha256"}'}" \
  response.json

cat response.json
rm response.json
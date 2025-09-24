#!/bin/bash
aws lambda invoke \
  --function-name LogFormatterFunction \
  --payload "${1:-'{"level": "ERROR", "message": "Connection failed", "service": "api"}'}" \
  response.json

cat response.json
rm response.json
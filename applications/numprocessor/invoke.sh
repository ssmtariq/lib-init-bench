#!/bin/bash
aws lambda invoke \
  --function-name NumProcessorFunction \
  --payload "${1:-'{\"operation\": \"multiply\", \"number\": 10}'}" \
  response.json

cat response.json
rm response.json
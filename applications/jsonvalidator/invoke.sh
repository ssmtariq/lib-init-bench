#!/bin/bash
aws lambda invoke \
  --function-name JsonValidatorFunction \
  --payload "${1:-'{\"data\": {\"name\": \"John Doe\", \"age\": 30, \"email\": \"john@example.com\"}}'}" \
  response.json

cat response.json
rm response.json
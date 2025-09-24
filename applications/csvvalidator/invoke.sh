#!/bin/bash
aws lambda invoke \
  --function-name CsvValidatorFunction \
  --payload "${1:-'{"data": "name,age\nJohn,30\nJane,25", "validate_schema": false}'}" \
  response.json

cat response.json
rm response.json
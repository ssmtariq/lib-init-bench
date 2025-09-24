#!/bin/bash
aws lambda invoke \
  --function-name StatsGeneratorFunction \
  --payload "${1:-'{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'}" \
  response.json

cat response.json
rm response.json
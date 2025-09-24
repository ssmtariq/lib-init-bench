#!/bin/bash
aws lambda invoke \
  --function-name DnaVisualizerFunction \
  --payload "${1:-'{"sequence": "ATCGATCG"}'}" \
  response.json

cat response.json
rm response.json
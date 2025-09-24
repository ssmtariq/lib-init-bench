#!/bin/bash
aws lambda invoke \
  --function-name TextAnalyzerFunction \
  --payload "${1:-'{\"text\": \"This is a simple sentence to analyze.\", \"analysis_type\": \"basic\"}'}" \
  response.json

cat response.json
rm response.json
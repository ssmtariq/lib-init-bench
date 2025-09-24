#!/bin/bash
aws lambda invoke \
  --function-name VersionReporterFunction \
  --payload "${1:-'{"package": "pip"}'}" \
  response.json

cat response.json
rm response.json
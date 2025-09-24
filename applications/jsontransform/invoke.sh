#!/bin/bash
aws lambda invoke \
  --function-name JsonTransformFunction \
  --payload "${1:-'{\"data\": {\"text\": \"Hello World\", \"number\": 42, \"list\": [1, 2, 3]}, \"transformations\": [\"uppercase\", \"reverse\"]}'}" \
  response.json

cat response.json
rm response.json
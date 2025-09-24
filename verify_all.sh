#!/bin/bash

# Application test payloads
declare -A payloads=(
  ["DnaVisualizerFunction"]='{"sequence": "ATCG"}'
  ["CsvValidatorFunction"]='{"data": "id,name\n1,test"}'
  ["VersionReporterFunction"]='{"check": true}'
  ["LogFormatterFunction"]='{"message": "test log"}'
  ["StatsGenFunction"]='{"numbers": [1,2,3,4,5]}'
  ["TextHasherFunction"]='{"text": "test text"}'
  ["JsonValidatorFunction"]='{"data": {"test": "value"}}'
  ["TextAnalyzerFunction"]='{"text": "analyze this text"}'
  ["JsonTransformFunction"]='{"data": {"text": "test"}, "transformations": ["uppercase"]}'
  ["NumProcessorFunction"]='{"operation": "multiply", "number": 10}'
)

echo "Starting verification of all applications..."

for app_dir in applications/*/; do
  app_name=$(basename "$app_dir")
  function_name="${app_name^}Function"  # Capitalize first letter and append Function
  
  echo -e "\n=== Testing $app_name ==="
  
  # Deploy the application
  echo "Deploying..."
  (cd "$app_dir" && ./deploy.sh)
  
  if [ $? -eq 0 ]; then
    echo "Deployment successful"
    
    # Get the payload for this function
    payload=${payloads[$function_name]}
    
    # Run benchmark with cold start
    echo "Running benchmark..."
    python bench/invoke_bench.py \
      --function "$function_name" \
      --count 3 \
      --force-cold \
      --payload "$payload"
    
    echo "----------------------------------------"
  else
    echo "Deployment failed"
    echo "----------------------------------------"
    continue
  fi
done

echo -e "\nVerification complete!"
#!/usr/bin/env python3
import argparse
import json
import time
import uuid
from typing import Dict, List, Optional

import boto3

def force_cold_start(lambda_client, function_name: str) -> None:
    """Force a cold start by updating an environment variable."""
    response = lambda_client.get_function_configuration(FunctionName=function_name)
    env_vars = response.get('Environment', {}).get('Variables', {})
    env_vars['COLD_START_TRIGGER'] = str(uuid.uuid4())
    
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Environment={'Variables': env_vars}
    )
    # Wait for update to complete
    time.sleep(5)

def invoke_function(
    lambda_client,
    function_name: str,
    payload: Dict,
    force_cold: bool = False
) -> tuple[float, Dict]:
    """Invoke Lambda function and return duration and response."""
    if force_cold:
        force_cold_start(lambda_client, function_name)
    
    start_time = time.perf_counter()
    response = lambda_client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(payload)
    )
    duration = time.perf_counter() - start_time
    
    result = json.loads(response['Payload'].read())
    return duration, result

def run_benchmark(
    function_name: str,
    count: int = 5,
    region: str = 'us-east-1',
    payload: Optional[Dict] = None,
    force_cold: bool = False
) -> List[tuple[float, Dict]]:
    """Run benchmark with specified number of invocations."""
    if payload is None:
        payload = {'x': 1}
    
    lambda_client = boto3.client('lambda', region_name=region)
    results = []
    
    for i in range(count):
        duration, result = invoke_function(
            lambda_client,
            function_name,
            payload,
            force_cold=force_cold and i == 0  # Only force cold on first if requested
        )
        results.append((duration, result))
        if i == 0:
            print(f"\nCold start duration: {duration:.3f}s")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"Warm invoke #{i}: {duration:.3f}s")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Benchmark Lambda function initialization')
    parser.add_argument('--function', required=True, help='Lambda function name')
    parser.add_argument('--count', type=int, default=5, help='Number of invocations')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--payload', type=str, help='JSON payload string')
    parser.add_argument('--force-cold', action='store_true', help='Force cold start')
    
    args = parser.parse_args()
    payload = json.loads(args.payload) if args.payload else None
    
    print(f"\nBenchmarking {args.function} ({args.count} invocations)")
    if args.force_cold:
        print("Forcing cold start for first invocation")
    
    results = run_benchmark(
        args.function,
        args.count,
        args.region,
        payload,
        args.force_cold
    )
    
    # Summary statistics
    durations = [r[0] for r in results]
    print(f"\nSummary:")
    print(f"  Cold start: {durations[0]:.3f}s")
    if len(durations) > 1:
        warm = durations[1:]
        print(f"  Warm p50: {sorted(warm)[len(warm)//2]:.3f}s")
        print(f"  Warm p90: {sorted(warm)[int(len(warm)*0.9)]:.3f}s")
        print(f"  Warm p99: {sorted(warm)[int(len(warm)*0.99)]:.3f}s")

if __name__ == '__main__':
    main()
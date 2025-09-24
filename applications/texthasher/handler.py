import time
start_time = time.perf_counter()

# Inefficient: Import boto3 which performs network/disk I/O at import time
import boto3
import hashlib

# Calculate import time
import_time = time.perf_counter() - start_time

def hash_text(text: str, algorithm: str = 'sha256') -> str:
    """
    Hash input text using the specified algorithm.
    Note: This function doesn't use AWS services at all,
    yet we imported boto3 which does expensive I/O at import.
    """
    if algorithm not in hashlib.algorithms_guaranteed:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def lambda_handler(event, context):
    """Hash the provided text using the specified algorithm."""
    text = event.get('text', '')
    algorithm = event.get('algorithm', 'sha256')
    
    if not text:
        return {
            'error': 'No text provided',
            'import_time': import_time
        }
    
    try:
        # Core functionality doesn't use boto3 at all!
        text_hash = hash_text(text, algorithm)
        
        result = {
            'text_hash': text_hash,
            'algorithm': algorithm,
            'text_length': len(text),
            'import_time': import_time
        }
        
        # Add metadata about the heavy I/O initialization
        try:
            # This triggers more I/O as boto3 loads service data
            s3 = boto3.client('s3')
            result['aws_region'] = s3.meta.region_name
        except Exception:
            pass
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'import_time': import_time
        }
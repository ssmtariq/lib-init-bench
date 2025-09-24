import time
start_time = time.perf_counter()

# Inefficient imports - these libraries are not actually used in the core functionality
import matplotlib.pyplot as plt
import pandas as pd

# Calculate import time
import_time = time.perf_counter() - start_time

def validate_dna(sequence: str) -> bool:
    """Validate that a sequence contains only valid DNA bases."""
    return all(base in 'ATCG' for base in sequence.upper())

def calculate_gc_content(sequence: str) -> float:
    """Calculate the GC content of a DNA sequence."""
    sequence = sequence.upper()
    gc_count = sequence.count('G') + sequence.count('C')
    return gc_count / len(sequence) if len(sequence) > 0 else 0

def lambda_handler(event, context):
    """Process a DNA sequence and return basic statistics."""
    sequence = event.get('sequence', '')
    
    if not sequence:
        return {
            'error': 'No sequence provided',
            'import_time': import_time
        }
    
    if not validate_dna(sequence):
        return {
            'error': 'Invalid DNA sequence',
            'import_time': import_time
        }
    
    result = {
        'sequence_length': len(sequence),
        'gc_content': calculate_gc_content(sequence),
        'import_time': import_time
    }
    
    return result
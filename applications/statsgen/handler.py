import time
start_time = time.perf_counter()

# Inefficient: matplotlib performs heavy initialization at import time
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, median, stdev

# Calculate import time
import_time = time.perf_counter() - start_time

def calculate_statistics(numbers: list[float]) -> dict:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        raise ValueError("Empty list provided")
    
    return {
        "mean": mean(numbers),
        "median": median(numbers),
        "std_dev": stdev(numbers) if len(numbers) > 1 else 0
    }

def generate_histogram(numbers: list[float]) -> None:
    """
    Generate a histogram using matplotlib.
    This is just to demonstrate the heavy import - we don't actually use it
    since Lambda can't display plots anyway.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(numbers, bins='auto')
    plt.title('Data Distribution')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    # We can't actually show or save this in Lambda
    plt.close()

def lambda_handler(event, context):
    """Calculate statistics for a list of numbers."""
    numbers = event.get('numbers', [])
    
    if not numbers:
        return {
            'error': 'No numbers provided',
            'import_time': import_time
        }
    
    try:
        # Even though we imported matplotlib (heavy!),
        # we only use basic statistics functions
        stats = calculate_statistics(numbers)
        stats['import_time'] = import_time
        
        # Add some metadata about the heavy initialization
        stats['matplotlib_backend'] = plt.get_backend()
        stats['numpy_version'] = np.__version__
        
        return stats
        
    except Exception as e:
        return {
            'error': str(e),
            'import_time': import_time
        }
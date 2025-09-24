# DNA Sequence Visualizer

A simple DNA sequence analysis tool that computes basic sequence statistics.

## Dependencies

```
matplotlib==3.8.*
pandas==2.2.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"sequence": "ATCGATCG"}'
```

Expected output:
```json
{
  "sequence_length": 8,
  "gc_content": 0.5,
  "import_time": 2.345  // Actual time will vary
}
```

## Local Testing

```bash
sam local invoke -e events/test.json
```

## Clean Up

```bash
sam delete
```

## Inefficiency Details

### Pattern: C1 – Importing Unused Libraries

This application demonstrates the inefficiency of importing heavy libraries that aren't actually used in the function's core logic. While the function only needs to compute basic sequence statistics (GC content, length, etc.), it imports matplotlib and pandas at the module level, significantly impacting cold start time.

### Why this exhibits the inefficiency

The application imports:
- `matplotlib`: A heavy visualization library (typically used for plotting DNA patterns)
- `pandas`: A data analysis framework (typically used for large sequence datasets)

However, the actual Lambda handler only:
1. Validates input DNA sequence
2. Computes basic statistics (GC content, length)
3. Returns JSON results

These operations use only built-in Python string operations, making the imported libraries completely unnecessary for the core functionality.

### Mitigation Notes

To fix this inefficiency:
1. Remove unnecessary imports of matplotlib and pandas
2. Move any visualization code to a separate function that's only imported when needed
3. Use built-in Python methods for simple string operations
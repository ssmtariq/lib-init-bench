# Data Statistics Generator

A serverless service that generates statistical summaries and visualizations of numeric data.

## Dependencies

```
matplotlib==3.8.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'
```

Expected output:
```json
{
  "mean": 5.5,
  "median": 5.5,
  "std_dev": 2.872281323269014,
  "import_time": 1.234  // Actual time will vary
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

### Pattern: C5 – Heavy Import-time Initialization

This application demonstrates the inefficiency of using libraries that perform heavy initialization tasks at import time. While the function only needs basic statistical calculations, importing matplotlib triggers extensive system probing and font cache initialization.

### Why this exhibits the inefficiency

The application loads matplotlib which performs on import:
1. Filesystem operations to:
   - Scan for available fonts
   - Build font cache
   - Probe for available backends
2. System configuration checks for:
   - Display server availability
   - Graphics capabilities
   - Cache directories
3. Module initialization for:
   - Default styling
   - Color maps
   - Backend selection

However, the actual Lambda handler only:
1. Calculates basic statistics (mean, median, std dev)
2. Returns JSON results
3. Never actually generates any plots

This creates significant cold-start overhead due to matplotlib's heavy import-time initialization.

### Mitigation Notes

To fix this inefficiency:
1. Use numpy or statistics module for basic calculations
2. Only import matplotlib when actually generating plots
3. Consider splitting visualization into a separate function or Lambda
4. Use lazy loading patterns for heavy initialization code
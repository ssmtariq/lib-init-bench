# App Version Reporter

A simple service that reports version information about installed packages.

## Dependencies

```
setuptools==70.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"package": "pip"}'
```

Expected output:
```json
{
  "package": "pip",
  "version": "23.2.1",
  "import_time": 0.987  // Actual time will vary
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

### Pattern: C3 – Library Misuse

This application demonstrates the inefficiency of using heavy legacy APIs when lighter alternatives exist. The function uses the heavyweight `pkg_resources` module from setuptools at module import time to read package versions, instead of the more efficient `importlib.metadata`.

### Why this exhibits the inefficiency

The application:
1. Uses `pkg_resources` for version lookups, which:
   - Scans all installed distributions at import time
   - Builds a complete working set of package metadata
   - Resolves dependencies between packages
2. Only needs simple version information that could be obtained from `importlib.metadata`
3. Performs heavy filesystem operations during module import

This creates significant cold-start overhead because `pkg_resources` does much more work than needed.

### Mitigation Notes

To fix this inefficiency:
1. Replace `pkg_resources` with `importlib.metadata`
2. Use `importlib.metadata.version(package_name)` for simple version lookups
3. Avoid building complete package metadata indexes when not needed
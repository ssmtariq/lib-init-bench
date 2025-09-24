# Log Formatter

A serverless service that formats and enhances log messages with color, timestamps, and structure.

## Dependencies

```
rich==13.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"level": "ERROR", "message": "Connection failed", "service": "api"}'
```

Expected output:
```json
{
  "formatted_log": "[2025-09-19 10:15:30] ERROR [api]: Connection failed",
  "import_time": 0.456  // Actual time will vary
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

### Pattern: C4 – Avoidable Library Usage

This application demonstrates the inefficiency of using heavy formatting libraries when simple string operations would suffice. The function imports the `rich` library at module level for basic log formatting that could be achieved with standard Python string methods.

### Why this exhibits the inefficiency

The application:
1. Imports `rich` at module level for:
   - Simple log message formatting
   - Basic color/style application
   - Timestamp addition
2. Only uses a tiny fraction of rich's capabilities
3. Could achieve the same output using:
   - f-strings
   - datetime.strftime()
   - Basic string concatenation

The `rich` library provides powerful features like:
- Complex terminal layouts
- Progress bars
- Syntax highlighting
- Tables and trees
But our simple log formatting doesn't need any of these features.

### Mitigation Notes

To fix this inefficiency:
1. Remove rich dependency
2. Use standard library:
   ```python
   from datetime import datetime
   formatted = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {level} [{service}]: {message}"
   ```
3. Consider moving to a lighter formatting library if needed
4. Only import rich when actually using its advanced features
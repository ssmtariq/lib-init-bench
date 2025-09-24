# JSON Transformer (Java)

A serverless service that transforms JSON data using various utilities from the Apache Commons and Jackson libraries.

## Dependencies

See `pom.xml` for full dependency tree. Main dependencies:
- Jackson (JSON processing)
- Apache Commons Lang3
- Apache Commons Text
- Apache Commons Collections4

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{
  "data": {
    "text": "Hello World",
    "number": 42,
    "list": [1, 2, 3]
  },
  "transformations": ["uppercase", "reverse"]
}'
```

Expected output:
```json
{
  "transformed": {
    "text": "DLROW OLLEH",
    "number": 42,
    "list": [3, 2, 1]
  },
  "importTime": 1.234  // Actual time will vary
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

### Pattern: C7 – Heavy Dependency Graph (Java)

This application demonstrates the inefficiency of pulling in a large dependency tree with heavy initialization costs, when only simple JSON transformation features are needed.

### Why this exhibits the inefficiency

The application dependencies include:
1. Jackson libraries:
   - Core annotations
   - Databind
   - Module scanning
2. Apache Commons:
   - Lang3 utilities
   - Text processing
   - Collections
3. Static initialization:
   - Jackson object mapper setup
   - Module registration
   - Type factories
   - Cached reflection data

However, the actual Lambda handler:
1. Performs simple JSON transformations:
   - String case conversion
   - Array reversing
   - Basic object manipulation
2. Could use basic Java functionality:
   - String methods
   - Collections methods
   - Simple JSON parsing

This creates significant cold-start overhead due to:
- Large JAR size
- Complex classpath scanning
- Heavy static initialization
- Excessive reflection usage

### Mitigation Notes

To fix this inefficiency:
1. Remove unnecessary dependencies:
   - Use built-in String methods instead of Commons Text
   - Use ArrayList instead of Commons Collections
2. Simplify JSON handling:
   - Use minimal Jackson configuration
   - Consider lighter alternatives (JsonP)
3. Optimize initialization:
   - Lazy load features
   - Minimize static blocks
   - Reduce reflection usage
4. Split functionality:
   - Basic transformer (fast startup)
   - Advanced transformer (accepts overhead)
# CSV Schema Validator

A serverless service that validates CSV data against predefined schemas.

## Dependencies

```
xmlschema==3.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"data": "name,age\nJohn,30\nJane,25", "validate_schema": false}'
```

Expected output:
```json
{
  "valid": true,
  "rows": 2,
  "columns": 2,
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

### Pattern: C2 – Default import of rarely used libs

This application demonstrates the inefficiency of importing libraries by default that are only needed in rare scenarios. The function primarily processes CSV data using string operations, but it imports `xmlschema` at module level even though XML schema validation is only used in a special case.

### Why this exhibits the inefficiency

The application imports:
- `xmlschema`: A heavy XML schema validation library that's only used when `validate_schema=true`

However, the actual Lambda handler:
1. Usually just parses CSV data using string operations
2. Only needs XML schema validation for special CSV-to-XML conversion cases
3. Most invocations never use the XML validation capability

This creates unnecessary cold-start overhead for the common case scenario.

### Mitigation Notes

To fix this inefficiency:
1. Move xmlschema import inside the validation function
2. Only import when `validate_schema=true`
3. Consider splitting XML validation into a separate function
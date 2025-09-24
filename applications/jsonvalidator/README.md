# JSON Schema Validator

A serverless service that validates JSON data against provided schemas using Pydantic.

## Dependencies

```
pydantic==2.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{
  "data": {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com"
  }
}'
```

Expected output:
```json
{
  "valid": true,
  "normalized_data": {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com"
  },
  "import_time": 0.567  // Actual time will vary
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

### Pattern: C7 – Heavy Dependencies

This application demonstrates the inefficiency of using a heavy validation framework (Pydantic) with extensive type checking and validation capabilities, when simpler validation would suffice.

### Why this exhibits the inefficiency

The application imports Pydantic which:
1. Sets up extensive typing machinery:
   - Type annotations processing
   - Runtime type checking
   - Validation decorators
2. Registers many validator types:
   - String validators
   - Number validators
   - Network types (URL, email)
   - Date/time types
3. Initializes validation infrastructure:
   - Schema compilation
   - Error handling
   - JSON serialization

However, the actual Lambda handler:
1. Only validates simple JSON structures
2. Could use basic dict access and type checks
3. Doesn't need most of Pydantic's features

This creates significant cold-start overhead due to importing and initializing the full validation framework.

### Mitigation Notes

To fix this inefficiency:
1. Replace Pydantic with basic validation:
   ```python
   def validate(data):
       return (
           isinstance(data.get('name'), str) and
           isinstance(data.get('age'), int) and
           isinstance(data.get('email'), str)
       )
   ```
2. Only import heavy validation when needed
3. Consider splitting complex validation into separate functions
4. Use lighter alternatives for simple cases
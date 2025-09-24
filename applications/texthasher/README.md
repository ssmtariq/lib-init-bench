# Text Hash Generator

A serverless service that generates cryptographic hashes for text data.

## Dependencies

```
boto3==1.*
```

## Deployment

```bash
./deploy.sh
```

## Testing

```bash
# Example payload
./invoke.sh '{"text": "Hello, World!", "algorithm": "sha256"}'
```

Expected output:
```json
{
  "text_hash": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
  "algorithm": "sha256",
  "import_time": 0.789  // Actual time will vary
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

### Pattern: C6 – Network/Disk I/O During Import

This application demonstrates the inefficiency of performing I/O operations during module import. The application imports boto3 at module level, which performs network and disk I/O operations to load configurations, even though the core hashing functionality doesn't require AWS services.

### Why this exhibits the inefficiency

The application imports `boto3` which performs on import:
1. Network I/O:
   - Fetches AWS metadata if running in EC2/Lambda
   - Checks for credentials from metadata service
2. Disk I/O:
   - Reads ~/.aws/config and ~/.aws/credentials
   - Scans for shared credential files
   - Loads service data from bundled files
3. Configuration lookup:
   - Environment variables
   - Credential providers
   - Region settings

However, the actual Lambda handler:
1. Only performs simple text hashing
2. Never uses any AWS services
3. Could operate entirely without boto3

This creates unnecessary cold-start overhead due to I/O operations during import.

### Mitigation Notes

To fix this inefficiency:
1. Remove unnecessary boto3 import
2. Use Python's built-in hashlib for hashing
3. Only import AWS SDK when actually needed
4. Consider moving AWS operations to a separate function
# Number Processor

This is a Go Lambda function that demonstrates inefficient I/O operations during initialization (C6 pattern).

## Description

The Number Processor is a simple Lambda function that performs basic numerical operations. However, it intentionally demonstrates inefficient practices by performing I/O operations during initialization:

1. Reads configuration from a YAML file during package initialization
2. Reads numbers from a text file during package initialization
3. Creates/writes to files in /tmp during initialization

These operations make the cold start slower than necessary, as they are performed every time the Lambda container initializes.

## Handler Operations

The handler supports two operations:

1. `multiply`: Multiplies the input number by a configured multiplier
2. `average`: Calculates the average of pre-loaded numbers

## Example Events

```json
{
    "operation": "multiply",
    "number": 10
}
```

```json
{
    "operation": "average"
}
```

## Deployment

To deploy the function:

```bash
./deploy.sh
```

## Testing

To test the function:

```bash
./invoke.sh
```

Or with a custom payload:

```bash
./invoke.sh '{"operation": "average"}'
```

## Inefficiency Pattern

This application demonstrates the C6 pattern (I/O operations during initialization) by:

- Reading configuration files during init()
- Loading data files during package initialization
- Writing to temporary files during startup

These operations should ideally be deferred until they are actually needed, or moved out of the initialization phase to improve cold start performance.
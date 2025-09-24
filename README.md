# lib-init-bench

A benchmarking tool for evaluating library-initialization inefficiencies in serverless applications.

## Overview

This repository contains a collection of AWS Lambda functions that demonstrate various library initialization inefficiencies. Each application is designed to showcase a specific inefficiency pattern commonly found in serverless applications.

## Prerequisites

Before running the benchmark applications, you need to install and configure the following tools:

### Required Tools
1. **AWS CLI**
   ```bash
   # For Ubuntu/Debian
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install

   # Configure AWS CLI with your credentials
   aws configure
   ```

2. **AWS SAM CLI**
   ```bash
   # For Ubuntu/Debian
   wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
   unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
   sudo ./sam-installation/install
   ```

3. **Python 3.11+**
   ```bash
   # For Ubuntu/Debian
   sudo apt update
   sudo apt install python3.11 python3.11-venv
   ```

4. **Java 17+ (for jsontransform)**
   ```bash
   # For Ubuntu/Debian
   sudo apt install openjdk-17-jdk
   ```

5. **Go 1.20+ (for numprocessor)**
   ```bash
   # For Ubuntu/Debian
   sudo apt install golang-1.20
   ```

### Python Virtual Environment Setup
```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install boto3 aws-cdk-lib
```

### AWS Configuration
1. Create an AWS account if you don't have one
2. Configure AWS credentials:
   ```bash
   aws configure
   ```
   You'll need to provide:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., us-east-1)
   - Default output format (json)

3. Verify configuration:
   ```bash
   aws sts get-caller-identity
   ```

### Running the Verification Script
After setting up all prerequisites:
```bash
# Make scripts executable
chmod +x verify_all.sh
chmod +x applications/*/deploy.sh
chmod +x applications/*/invoke.sh

# Run verification
./verify_all.sh
```

## Applications

| Application | Language | Pattern | Description |
|------------|----------|---------|-------------|
| dnavisualizer | Python | C1 | Unused Library Imports - Loads unused visualization libraries |
| csvvalidator | Python | C2 | Default Import with Rare Usage - Imports heavy validation libraries |
| versionreporter | Python | C3 | Library Misuse - Inefficient version checking patterns |
| logformatter | Python | C4 | Avoidable Initialization - Unnecessary logging setup |
| statsgen | Python | C5 | Heavy Init Operations - Complex statistical computations during init |
| texthasher | Python | C6 | I/O Operations on Import - File operations during module import |
| jsonvalidator | Python | C7 | Heavy Framework Dependencies - Large validation framework usage |
| textanalyzer | Python | C8 | Eager Plugin Loading - Loads all NLTK modules upfront |
| jsontransform | Java | C7 | Heavy Dependencies - Multiple heavy Java libraries for JSON processing |
| numprocessor | Go | C6 | I/O on Init - File operations during package initialization |

## Directory Structure

```
lib-init-bench/
├── applications/
│   ├── dnavisualizer/      # DNA sequence visualization with unused libraries
│   ├── csvvalidator/       # CSV schema validation with default imports
│   ├── versionreporter/    # Application version reporting with misused libraries
│   ├── logformatter/       # Log formatting with avoidable initialization
│   ├── statsgen/          # Statistical analysis with heavy init
│   ├── texthasher/        # Text hashing with I/O on import
│   ├── jsonvalidator/     # JSON schema validation with heavy framework
│   ├── textanalyzer/      # Text analysis with eager plugin loading
│   ├── jsontransform/     # JSON transformation with heavy Java dependencies
│   └── numprocessor/      # Number processing with Go I/O on init
└── bench/                 # Benchmarking utilities
    └── invoke_bench.py    # Benchmark execution script
```

## Benchmarking

To run benchmarks for all applications:

```bash
python bench/invoke_bench.py
```

## Running Applications

### Method 1: Using verify_all.sh (Recommended)
This script will deploy and test all applications while measuring cold start times:
```bash
./verify_all.sh
```

### Method 2: Individual Testing
Each application can be tested individually:

1. Deploy an application:
```bash
cd applications/<app-name>
./deploy.sh
```

2. Test the application:
```bash
./invoke.sh
```

3. Benchmark with specific parameters:
```bash
python bench/invoke_bench.py \
  --function "<AppName>Function" \
  --count 3 \
  --force-cold \
  --payload '{"key": "value"}'
```

### Common Issues

1. **AWS Credentials**: If you see authentication errors:
   ```bash
   aws configure  # Rerun and verify credentials
   ```

2. **Python Dependencies**: If you encounter missing packages:
   ```bash
   pip install -r applications/<app-name>/requirements.txt
   ```

3. **Java/Maven Issues**: For jsontransform app:
   ```bash
   # Verify Java installation
   java -version
   mvn -version
   ```

4. **Go Build Issues**: For numprocessor app:
   ```bash
   # Verify Go installation
   go version
   ```

5. **Permission Issues**: Make scripts executable:
   ```bash
   chmod +x verify_all.sh
   chmod +x applications/*/deploy.sh
   chmod +x applications/*/invoke.sh
   ```

## Inefficiency Patterns

### C1: Unused Library Imports
Importing heavy libraries that are not used in the actual execution path.

### C2: Default Import with Rare Usage
Importing full libraries when only a small subset of functionality is needed.

### C3: Library Misuse
Using libraries in inefficient ways that cause unnecessary initialization.

### C4: Avoidable Initialization
Performing initialization that could be deferred or avoided entirely.

### C5: Heavy Init Operations
Complex computations or operations during initialization phase.

### C6: I/O Operations on Import
File system or network operations during module/package initialization.

### C7: Heavy Framework Dependencies
Using large frameworks when lighter alternatives would suffice.

### C8: Eager Plugin Loading
Loading all plugins/modules upfront instead of on-demand.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
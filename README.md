<div align="center">
  <img width="450" src="logo.png" alt="smartmutate logo" />
</div>

---

Smartmutate is a file conversion tool built in Python that leverages Anthropic's Claude API to intelligently convert data between common file types. 

## Features

- Support for common data formats like JSON, CSV, YAML, and XML
- Available as command-line interface and as a Python Library
- Secure API key management
- Built-in format validation and error handling

## Installation

Install SmartMutate using pip:

```bash
pip install smartmutate
```

## Quick Start

SmartMutate can be used either directly from the command line or as a Python library. 

### Command Line

Convert files directly from the terminal:

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY='your-api-key'

# Convert a file
smartmutate input.json output.yaml
```

### Python Library

Use the converter function in your Python code:

```python
from smartmutate import Converter

# Initialize the converter
converter = Converter(api_key="your-anthropic-key")

# Convert a file
converter.convert_file("input.json", "output.yaml")
```

## Supported Formats

SmartMutate currently supports conversions between:
- JSON
- YAML
- CSV
- TXT
- More formats coming soon...

Each format is validated before conversion to ensure data integrity.

## Configuration

SmartMutate uses your Anthropic API key for conversions. You can provide it in several ways:
1. Environment variable: `ANTHROPIC_API_KEY`
2. Direct initialization: `Converter(api_key="your-key")`
3. Command line argument: `--api-key` OR `--env` followed by the path to your `.env` file

## Error Handling

SmartMutate includes comprehensive error handling for:
- Invalid file formats
- Missing input files
- API connection issues
- Conversion failures

Each error provides clear feedback to help troubleshoot issues quickly.

## Development

### Running Tests

Run the test suite using pytest:

```bash
# Install development dependencies
pip install -e .[test]

# Run tests
pytest tests/
```

## Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch
3. Make something cool or fix something bad
4. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.
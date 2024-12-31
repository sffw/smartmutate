# smartMutatormartMutator a powerful file conversion tool powered by Anthropic's Claude AI. It enables seamless conversion between various file formats while preserving context and meaning through AI-powered interpretation.

## Features

- 🔄 Convert between multiple file formats (CSV, JSON, XML, YAML, etc.)
- 🤖 AI-powered conversion ensures contextual accuracy
- 🔑 Simple API key management
- ⚡ Fast and efficient processing
- 🛠️ Easy to integrate into existing workflows
- 📦 Available as both CLI tool and Python library

## Installation

```bash
pip install smartMutator
```

## Quick Start

### Command Line Usage

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY='your-api-key'

# Convert a file
smartMutatornvert input.csv output.json

# Get help
smartMutatorhelp
```

### Python Library Usage

```python
from smartMutatorport Converter

# Initialize converter with your API key
converter = Converter(api_key="your-anthropic-key")

# Convert a file
converter.convert("input.csv", "output.json")

# Stream large file conversion
with converter.stream_convert("large_input.csv", "output.json") as stream:
    for progress in stream:
        print(f"Progress: {progress}%")
```

## Supported Formats

- CSV
- JSON
- XML
- YAML
- Excel (xlsx, xls)
- More formats coming soon!

## Configuration

Create a configuration file at `~/.smartMutatornfig.yaml`:

```yaml
api_key: your-anthropic-key
default_format: json
timeout: 300
max_file_size: 100MB
```

## Advanced Usage

### Custom Conversion Rules

```python
from smartMutatorport Converter, ConversionRule

# Define custom conversion rules
rule = ConversionRule(
    source_format="csv",
    target_format="json",
    mapping={
        "column1": "field1",
        "column2": "field2"
    }
)

converter = Converter(rules=[rule])
```

### Batch Processing

```python
converter.batch_convert(
    input_dir="input_files/",
    output_dir="converted_files/",
    source_format="csv",
    target_format="json"
)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Anthropic's Claude API](https://anthropic.com)
- Inspired by the need for intelligent file conversion in data processing pipelines

## Support

- 📚 [Documentation](https://smartMutatoradthedocs.io/)
- 💬 [Discord Community](https://discord.gg/smartMutator 🐛 [Issue Tracker](https://github.com/yourusername/smartMutatorsues)
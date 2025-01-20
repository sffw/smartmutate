from enum import Enum

SUPPORTED_FORMATS = [ "json", "csv", "yaml", "txt"]

class FileFormat(Enum):
    """Supported file formats for conversion"""
    JSON = "json"
    CSV = "csv"
    YAML = "yaml"
    TXT = "txt"

format_instructions = {
    FileFormat.JSON: {
        "output": "Ensure valid JSON with proper nesting, indentation, and double quotes for strings.",
        "input": "Parse the JSON structure, maintaining all nested objects and arrays."
    },
    FileFormat.CSV: {
        "output": "Create logical column headers. Each value should be properly escaped. Flatten nested structures by combining parent/child keys.",
        "input": "Interpret the CSV data, treating the first row as headers and subsequent rows as data records."
    },
    FileFormat.YAML: {
        "output": "Use standard YAML conventions with proper indentation. Use hyphens for lists. Quote keys only when necessary.",
        "input": "Parse the YAML structure, preserving all hierarchical relationships and data types."
    }
}


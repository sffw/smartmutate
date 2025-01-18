from ..handlers import JSONHandler, CSVHandler, YAMLHandler

SUPPORTED_FORMATS = [ "json", "csv", "yaml"]

HANLDERS = {
    "json": JSONHandler(),
    "csv": CSVHandler(),
    "yaml": YAMLHandler()
}

CONVERT_PROMPTS = {
    "csv": (
    "Convert this Python dictionary into CSV format. "
    "Create logical column headers based on the dictionary keys. "
    "Each dictionary value should be in its own cell, properly escaped. "
    "For nested dictionaries, flatten the structure by combining parent and child keys. "
    "For lists of dictionaries, each dictionary should become a row. "
    "Return only the CSV output without explanation.\n\n"
    ),
    "json":(
    "Convert this Python dictionary into JSON format. "
    "Ensure proper nesting with appropriate indentation. "
    "Use double quotes for strings. "
    "Arrays and objects should be properly formatted. "
    "Follow standard JSON specification. "
    "Return only the JSON output without explanation.\n\n"
    ),
    "yaml":(
    "Convert this Python dictionary into YAML format. "
    "Maintain proper indentation and structure. "
    "Use standard YAML conventions for nested data. "
    "Lists should be represented with hyphens. "
    "Keys should not be quoted unless necessary. "
    "Return only the YAML output without explanation.\n\n"
    )
}


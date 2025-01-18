from pathlib import Path
from typing import Dict, Any


from .registry import SUPPORTED_FORMATS, HANLDERS


# Detect input format
def get_file_format(file_path: Path) -> str:
    if not file_path.suffix:
        raise ValueError(f"No file extension found in: {file_path}")
        
    # Get extension without the leading period and convert to lowercase
    format_name = file_path.suffix[1:].lower()
    
    if format_name not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{format_name}'. "
            f"Supported formats are: {', '.join(sorted(SUPPORTED_FORMATS))}"
        )
        
    return format_name

def load_input(file_path: Path) -> Dict[str, Any]:
    """Load the input file into a Python dictionary.
    """
    # Detect input format
    file_format = get_file_format(file_path)
    
    # Get appropriate handler
    handler = HANLDERS.get(file_format)
    if not handler:
        raise ValueError(f"No handler available for format: {file_format}")
        
    # Load and return data
    return handler.load(file_path)

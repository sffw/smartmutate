
from pathlib import Path
from typing import Dict, Any, Optional
from ..handlers import JSONHandler
from .registry import SUPPORTED_FORMATS
from .fileHandler import get_file_format, load_input
from .api import convert_with_claude

class ConversionEngine:
    """
    Central conversion engine that orchestrates workflow:
    get input -> parse to dict -> convert_with_claude -> output file
    """

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
    
    def convert(self, input_path: Optional[Path] = None, output_path: Optional[Path] = None) -> None:
        """
        Orchestrates the complete file conversion workflow.
        """
        # Allow method parameters to override instance paths
        input_path = input_path or self.input_path
        output_path = output_path or self.output_path

        # Step 1: Detect and validate formats
        input_format = get_file_format(input_path)
        output_format = get_file_format(output_path)
                
        try:
            # Step 2: Load and parse input file to dictionary
            data = load_input(input_path)
            
            
        except Exception as e:
            # Wrap any internal errors with more context
            raise ValueError(
                f"Failed to convert {input_path} ({input_format}) to "
                f"{output_path} ({output_format}): {str(e)}"
            ) from e
        
        # Step 3: Convert data to output format
        output_content = convert_with_claude(data, output_format)

        with open(output_path, 'w') as f:
                f.write(output_content)

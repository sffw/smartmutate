import anthropic
import os

from pathlib import Path
from typing import Dict, Any, Optional
from ..handlers import JSONHandler

SUPPORTED_FORMATS = [ "json", "csv"]


class ConversionEngine:
    """
    Central conversion engine that orchestrates workflow:
    get input -> parse to dict -> convert_with_claude -> output file
    """

    
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.SUPPORTED_FORMATS = SUPPORTED_FORMATS

        self.handlers= {
            "json": JSONHandler(),
        }
    
    def load_input(self) -> Dict[str, Any]:
        """Load the input file into a Python dictionary.
        
        Returns:
            Dict containing the parsed input data
            
        Raises:
            ValueError: If input format is unsupported or content is invalid
        """
        # Detect input format
        input_format = self.get_file_format(self.input_path)
        
        # Get appropriate handler
        handler = self.handlers.get(input_format)
        if not handler:
            raise ValueError(f"No handler available for format: {input_format}")
            
        # Load and return data
        return handler.load(self.input_path)

    def convert(self, input_path: Optional[Path] = None, output_path: Optional[Path] = None) -> None:
        """
        Orchestrates the complete file conversion workflow.
        
        This method handles the entire conversion process:
        1. Uses provided paths or falls back to instance paths
        2. Validates input/output formats
        3. Loads and validates input file
        4. Converts input to intermediate dictionary format
        
        Args:
            input_path: Optional override for instance input_path
            output_path: Optional override for instance output_path
            
        Returns:
            Dict containing the parsed data structure
            
        Raises:
            ValueError: For invalid formats or conversion failures
            FileNotFoundError: If input file doesn't exist
        """
        # Allow method parameters to override instance paths
        input_path = input_path or self.input_path
        output_path = output_path or self.output_path

        # Step 1: Detect and validate formats
        input_format = self.get_file_format(input_path)
        output_format = self.get_file_format(output_path)
        
        # Log the conversion attempt (this helps with debugging)
        print(f"Converting from {input_format} to {output_format}")
        
        try:
            # Step 2: Load and parse input file to dictionary
            data = self.load_input()
            
            # For now, just return the dictionary
            self.convert_dict_to_file(data, output_path)
            
        except Exception as e:
            # Wrap any internal errors with more context
            raise ValueError(
                f"Failed to convert {input_path} ({input_format}) to "
                f"{output_path} ({output_format}): {str(e)}"
            ) from e
        
    def get_file_format(self, file_path: Path) -> str:
        """Detect the format of a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: The detected file format (e.g., 'json', 'csv')
            
        Raises:
            ValueError: If the file has no extension or the format is unsupported
        """
        if not file_path.suffix:
            raise ValueError(f"No file extension found in: {file_path}")
            
        # Get extension without the leading period and convert to lowercase
        format_name = file_path.suffix[1:].lower()
        
        if format_name not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format '{format_name}'. "
                f"Supported formats are: {', '.join(sorted(self.SUPPORTED_FORMATS))}"
            )
            
        return format_name
    
    def convert_dict_to_file(self, data: Dict[str, Any], output_path: Path):
        """Convert a Python dictionary to a file in the specified format."""
        dict_string = str(data)
    
        prompt = (
            "Convert this Python dictionary into CSV format. "
            "Create logical column headers based on the dictionary keys. "
            "Each dictionary value should be in its own cell, properly escaped. "
            "For nested dictionaries, flatten the structure by combining parent and child keys. "
            "For lists of dictionaries, each dictionary should become a row. "
            "Return only the CSV output without explanation.\n\n"
            f"Python Dictionary:\n{dict_string}"
        )
        response = self.client.messages.create(model="claude-3-5-sonnet-20241022",max_tokens=1024,messages=[{"role": "user", "content": prompt}])
    
        csv_content = response.content[0].text

        with open(output_path, 'w') as f:
                f.write(csv_content)


from pathlib import Path
from typing import Any

class ConversionEngine:
    """
    Central conversion engine that orchestrates workflow:
    get input -> parse to dict -> convert_with_claude -> output file
    """

    def __init__(self, input_data: Any, input_format: str,output_path: Path):
        self.input_data = input_data
        self.input_format = input_format
        self.output_path = output_path

    # Intake data, validate, and convert
    # Step 1: Validate input data
        # check input format, check output format
        # return input_format, output_format, input_data
    # Step 2: Convert input_data
        # Pass input_format, output_format, data to converter
            # API passed formats into prompt generator 
            # API appends data to prompt
            # API returns output data object
    # Step 3: Write output to file 
    
    
    def convert(self) -> None:
        """
        Orchestrates the complete file conversion workflow.
        """
        print("output path", self.output_path)
        print("input data", self.input_data)
        print("input format", self.input_format)

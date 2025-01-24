from pathlib import Path
from typing import Any
from .file_processor import FileProcessor
from .api import ConverterAPI

class ConversionEngine:
    """
    Central conversion engine that orchestrates workflow:
    get input -> parse to dict -> convert_with_claude -> output file
    """

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.file_processor = FileProcessor()
        self.input_data = self.get_input_data()

    def get_input_data(self) -> Any:
        """
        Validates and loads the input data using the FileProcessor.
        
        Returns:
            Any: The loaded input data
            
        Raises:
            ValueError: If the input format is invalid
        """
        if self.file_processor.validate_format(self.input_path):
            self.input_data = self.file_processor.load_input_data(self.input_path)
            return self.input_data
        else:
            raise ValueError("Invalid input format")
        
    def convert(self) -> None:
        """
        Orchestrates the complete file conversion workflow.
        
        This method handles the entire conversion process:
        1. Gets the source and target formats
        2. Converts the data using the ConverterAPI
        3. Generates the output file
        """
        source_format = self.file_processor.get_file_format(self.input_path)
        target_format = self.file_processor.get_file_format(self.output_path)

        converter_api = ConverterAPI()
        
        converted_data = converter_api.convert(self.input_data, source_format, target_format)

        
        self.file_processor.generate_output(converted_data, self.output_path)
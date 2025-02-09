
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import yaml
import xml.etree.ElementTree as ET
import json

from .registry import FileFormat

class FileProcessor:
    """A class to handle various file operations including reading, writing, and format validation."""
    
    def __init__(self):
        """Initialize the FileProcessor with supported formats."""
        self.supported_formats = {format.value for format in FileFormat}


    def load_input_data(self, file_path: Path) -> Any:
        """
        Read file content based on its extension using pathlib.
        Returns the content as a string that can be sent to Claude API.
        """
        suffix = self.get_file_format(file_path)
        
        try:
            if suffix in ['.csv', '.xlsx', '.xls']:
                # Handle spreadsheet formats
                df = pd.read_csv(file_path) if suffix == '.csv' else pd.read_excel(file_path)
                return df.to_string()
                
            elif suffix == '.json':
                # Handle JSON files
                return file_path.read_text()
                
            elif suffix == '.xml':
                # Handle XML files
                tree = ET.parse(file_path)
                return ET.tostring(tree.getroot(), encoding='unicode', method='xml')
                
            elif suffix == '.yaml' or suffix == '.yml':
                # Handle YAML files
                with file_path.open('r') as f:
                    return yaml.safe_dump(yaml.safe_load(f))
                    
            else:
                # Default to plain text reading for unknown formats
                return file_path.read_text()
            
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {str(e)}")

    def validate_format(self, file_path: Path) -> bool:
        """
        Validate if the file format is supported.
        """
        format_name = self.get_file_format(file_path)

        if format_name not in self.supported_formats:
            raise ValueError(
                f"Unsupported format '{format_name}'. "
                f"Supported formats are: {', '.join(sorted(self.supported_formats))}"
            )
            
        return True

    def get_file_format(self, file_path: Path) -> str:
        """
        Detect the format of a file based on its extension.
        """
        if not file_path.suffix:
            raise ValueError(f"No file extension found in: {file_path}")
            
        # Get extension without the leading period and convert to lowercase
        format_name = file_path.suffix[1:].lower()
        
        return format_name

    def generate_output(self, data: Dict[str, Any], file_path: Path) -> None:
        """
        Generate output file based on its extension using pathlib.
        """
        # Check if file exists, if not create it
        if not file_path.exists():
            file_path.touch()
        else:
            # While file exists, increment file name until it doesn't exist
            i = 1
            while file_path.with_name(f"{file_path.stem} ({i}){file_path.suffix}").exists():
                i += 1
            file_path = file_path.with_name(f"{file_path.stem} ({i}){file_path.suffix}")
        
        suffix = self.get_file_format(file_path)

        try:
            if suffix == '.csv':
                # Handle CSV files
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False)
                
            elif suffix == '.json':
                # Handle JSON files
                with file_path.open('w') as f:
                    json.dump(data, f, indent=4)
                    
            elif suffix == '.xml':
                # Handle XML files
                tree = ET.ElementTree(ET.fromstring(data))
                tree.write(file_path)
                
            elif suffix == '.yaml' or suffix == '.yml':
                # Handle YAML files
                with file_path.open('w') as f:
                    yaml.safe_dump(data, f)
                    
            else:
                # Default to plain text writing for unknown formats
                with file_path.open('w') as f:
                    f.write(data)
                    
        except Exception as e:
            raise ValueError(f"Error writing file {file_path}: {str(e)}")
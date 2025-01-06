import json
from pathlib import Path
from typing import Dict, Any
from .base_handler import BaseHandler

class JSONHandler(BaseHandler):
    """Handler for JSON format files.
    
    This handler provides functionality to load and validate JSON files,
    converting them to and from Python dictionaries.
    """
    
    def load(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a JSON file into a Python dictionary.
        
        This method performs several steps:
        1. Validates the file exists and is readable
        2. Reads the file content
        3. Parses the JSON into a Python dictionary
        4. Returns the resulting dictionary
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Dict containing the parsed JSON data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If the file isn't readable
            ValueError: If the JSON is invalid
        """
        # First validate the file
        self.validate(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Ensure we got a dictionary
                if not isinstance(data, dict):
                    raise ValueError(
                        f"JSON file must contain an object/dictionary at root level, "
                        f"got {type(data).__name__} instead"
                    )
                    
                return data
                
        except json.JSONDecodeError as e:
            # Provide a more user-friendly error message
            raise ValueError(f"Invalid JSON in {file_path}: {str(e)}") from e
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File {file_path} contains invalid characters. "
                f"Please ensure it is UTF-8 encoded"
            ) from e
    
    def validate(self, file_path: Path) -> bool:
        """Validate that a file contains valid JSON data.
        
        This method checks:
        1. File exists and is readable
        2. Content is valid JSON
        3. Root element is a dictionary/object
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            bool: True if file contains valid JSON
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file isn't readable
            ValueError: If JSON is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Ensure root element is a dictionary
                if not isinstance(data, dict):
                    raise ValueError(
                        f"JSON file must contain an object/dictionary at root level, "
                        f"got {type(data).__name__} instead"
                    )
                    
                return True
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {str(e)}") from e
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File {file_path} contains invalid characters. "
                f"Please ensure it is UTF-8 encoded"
            ) from e
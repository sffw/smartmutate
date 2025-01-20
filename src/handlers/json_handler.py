import json
from pathlib import Path
from typing import Dict, Any
from .base_handler import BaseHandler

class JSONHandler(BaseHandler):
    """Handler for JSON format files."""
    def load(self, file_path: Path) -> Dict[str, Any]:
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
        """Validate that a file contains valid JSON data."""
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
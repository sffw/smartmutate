from pathlib import Path
from typing import Dict, Any
import yaml
from .base_handler import BaseHandler

class YAMLHandler(BaseHandler):
    """Handler for YAML format files with comprehensive error handling."""
    
    def __init__(self, encoding: str = 'utf-8'):
        """
        Initialize the YAML handler.
        
        Args:
            encoding: File encoding (default: utf-8)
        """
        self.encoding = encoding
    
    def load(self, file_path: Path) -> Dict[str, Any]:
        """
        Load and parse a YAML file into a dictionary format.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Dictionary containing the parsed YAML data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid or improperly formatted
        """
        # First validate the file
        self.validate(file_path)
        
        try:
            with open(file_path, 'r', encoding=self.encoding) as file:
                # Use safe_load to prevent arbitrary code execution
                data = yaml.safe_load(file)
                
                # Ensure we got a dictionary
                if not isinstance(data, dict):
                    raise ValueError(
                        f"YAML file must contain a mapping at root level, "
                        f"got {type(data).__name__} instead"
                    )
                    
                return data
                
        except yaml.YAMLError as e:
            # Provide detailed error messages for common YAML errors
            if isinstance(e, yaml.MarkedYAMLError):
                context = f" at line {e.problem_mark.line + 1}, column {e.problem_mark.column + 1}"
            else:
                context = ""
                
            raise ValueError(f"Invalid YAML in {file_path}{context}: {str(e)}") from e
            
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File {file_path} contains invalid characters. "
                f"Please ensure it uses {self.encoding} encoding"
            ) from e
    
    def validate(self, file_path: Path) -> bool:
        """
        Validate that a file contains valid YAML data.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            True if validation passes
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
            
        try:
            with open(file_path, 'r', encoding=self.encoding) as file:
                # Use safe_load to prevent arbitrary code execution
                data = yaml.safe_load(file)
                
                # Check for empty file
                if data is None:
                    raise ValueError("YAML file is empty")
                
                # Ensure root element is a dictionary
                if not isinstance(data, dict):
                    raise ValueError(
                        f"YAML file must contain a mapping at root level, "
                        f"got {type(data).__name__} instead"
                    )
                    
                return True
                
        except yaml.YAMLError as e:
            # Provide detailed error messages for common YAML errors
            if isinstance(e, yaml.MarkedYAMLError):
                context = f" at line {e.problem_mark.line + 1}, column {e.problem_mark.column + 1}"
            else:
                context = ""
                
            raise ValueError(f"Invalid YAML in {file_path}{context}: {str(e)}") from e
            
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File {file_path} contains invalid characters. "
                f"Please ensure it uses {self.encoding} encoding"
            ) from e

    def save(self, data: Dict[str, Any], file_path: Path) -> None:
        """
        Save dictionary data to a YAML file.
        
        Args:
            data: Dictionary to save as YAML
            file_path: Path where the YAML file should be saved
            
        Raises:
            ValueError: If data format is invalid
        """
        if not isinstance(data, dict):
            raise ValueError(
                f"Data must be a dictionary, got {type(data).__name__} instead"
            )
            
        try:
            with open(file_path, 'w', encoding=self.encoding) as file:
                # Use safe_dump for consistent output
                yaml.safe_dump(
                    data,
                    file,
                    default_flow_style=False,  # Use block style for better readability
                    allow_unicode=True,        # Support Unicode characters
                    sort_keys=False            # Preserve dictionary order
                )
                
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to save YAML: {str(e)}") from e
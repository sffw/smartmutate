from pathlib import Path
from typing import Dict, Any
import pandas as pd
from .base_handler import BaseHandler

class CSVHandler(BaseHandler):
    """Handler for CSV format files with robust error checking and validation."""
    
    def __init__(self, encoding: str = 'utf-8', delimiter: str = ','):
        """
        Initialize the CSV handler with configurable parameters.
        
        Args:
            encoding: File encoding (default: utf-8)
            delimiter: CSV delimiter character (default: comma)
        """
        self.encoding = encoding
        self.delimiter = delimiter
    
    def load(self, file_path: Path) -> Dict[str, Any]:
        """
        Load and parse a CSV file into a dictionary format.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dictionary containing the CSV data with column names as keys
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid or improperly formatted
        """
        # First validate the file
        self.validate(file_path)
        
        try:
            # Read CSV using pandas for robust handling
            df = pd.read_csv(
                file_path,
                encoding=self.encoding,
                delimiter=self.delimiter,
                on_bad_lines='warn'  # Handle malformed lines gracefully
            )
            
            # Convert to dictionary format
            # Group by index to handle multiple rows
            result = {
                'headers': df.columns.tolist(),
                'data': df.to_dict(orient='records')
            }
            
            return result
            
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file {file_path} is empty")
            
        except pd.errors.ParserError as e:
            raise ValueError(
                f"Failed to parse CSV file {file_path}. "
                f"Please verify the format and delimiter. Error: {str(e)}"
            ) from e
            
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File {file_path} contains invalid characters. "
                f"Please ensure it uses {self.encoding} encoding"
            ) from e
    
    def validate(self, file_path: Path) -> bool:
        """
        Validate that a file is a properly formatted CSV.
        
        Args:
            file_path: Path to the CSV file
            
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
            # Try reading first few lines to validate format
            df = pd.read_csv(
                file_path,
                encoding=self.encoding,
                delimiter=self.delimiter,
                nrows=5  # Only read beginning to validate
            )
            
            # Check that we have at least one column
            if len(df.columns) < 1:
                raise ValueError("CSV file must contain at least one column")
                
            # Validate column names are strings
            if not all(isinstance(col, str) for col in df.columns):
                raise ValueError("All CSV column names must be strings")
                
            return True
            
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file {file_path} is empty")
            
        except pd.errors.ParserError as e:
            raise ValueError(
                f"Invalid CSV format in {file_path}: {str(e)}"
            ) from e
            
        except UnicodeDecodeError as e:
            raise ValueError(
                f"File {file_path} contains invalid characters. "
                f"Please ensure it uses {self.encoding} encoding"
            ) from e

    def save(self, data: Dict[str, Any], file_path: Path) -> None:
        """
        Save dictionary data to a CSV file.
        
        Args:
            data: Dictionary containing 'headers' and 'data' keys
            file_path: Path where the CSV file should be saved
            
        Raises:
            ValueError: If data format is invalid
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        if 'headers' not in data or 'data' not in data:
            raise ValueError("Data dictionary must contain 'headers' and 'data' keys")
            
        try:
            # Convert to DataFrame for easy CSV writing
            df = pd.DataFrame(data['data'])
            
            # Ensure columns match headers
            df = df[data['headers']]
            
            # Write to CSV
            df.to_csv(
                file_path,
                index=False,
                encoding=self.encoding,
                sep=self.delimiter
            )
            
        except (ValueError, KeyError) as e:
            raise ValueError(f"Failed to save CSV: {str(e)}") from e
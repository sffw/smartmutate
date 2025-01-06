# src/smartMutate/core/handlers/base_handler.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class BaseHandler(ABC):
    """Abstract base class that defines the interface for all format handlers.
    
    This class ensures that all format handlers implement the necessary methods
    for reading and validating files in their specific format.
    """
    
    @abstractmethod
    def load(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a file into a Python dictionary.
        
        Args:
            file_path: Path to the file to be loaded
            
        Returns:
            Dict containing the parsed data
            
        Raises:
            ValueError: If the file content is invalid
        """
        pass
    
    @abstractmethod
    def validate(self, file_path: Path) -> bool:
        """Validate that a file contains valid formatted data.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            bool: True if file contains valid data
            
        Raises:
            ValueError: If the file content is invalid
        """
        pass
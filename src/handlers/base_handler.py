from pathlib import Path
from typing import Dict, Any

class BaseHandler():

    def load(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a file into a Python dictionary."""
        pass
    

    def validate(self, file_path: Path) -> bool:
        """Validate that a file contains valid formatted data."""
        pass
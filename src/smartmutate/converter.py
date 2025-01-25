from pathlib import Path
from .engine import ConversionEngine

class Converter:
    # exposed conversion method for Python files
    def __init__(self, api_key: str):
        self.api_key = api_key

    def convert_file(self, input_path: str, output_path: str) -> None:
        """
        entry point for using smartmutate as a Python module
        """
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        if not input_path.exists():
            raise ValueError(f"Input file does not exist: {input_path}")
            
        engine = ConversionEngine(
            input_path=input_path,
            output_path=output_path,
            api_key=self.api_key
        )
        engine.convert()
        
        return None

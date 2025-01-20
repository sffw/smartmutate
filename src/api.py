import os
import anthropic
from typing import Any
from enum import Enum

from .registry import FileFormat, format_instructions


class ConverterAPI:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def get_client(self):
        return self.client
    
    def test_convert_prompt(self):
        fullPrompt = self._get_conversion_prompt(FileFormat.CSV, FileFormat.JSON)
        print(fullPrompt)

    def _get_conversion_prompt(self,source_format: FileFormat, target_format: FileFormat) -> str:
        """Get the conversion prompt for the given source and target formats."""

        # Base prompt template focusing on semantic preservation
        base_prompt = (
            f"You are a specialized file format converter. "
            f"Convert the following {source_format.value} content into {target_format.value} format. "
            "Preserve all data structure, relationships, and semantic meaning. "
            "Return only the converted output without explanation or additional text.\n\n"
        )

        prompt = base_prompt
        if source_format in format_instructions:
            prompt += f"Input instructions: {format_instructions[source_format]['input']}\n"
        if target_format in format_instructions:
            prompt += f"Output instructions: {format_instructions[target_format]['output']}\n"
            
        return prompt


    def convert(self, data: Any, source_format: Any, target_format: Any) -> Any:
            """Convert a input file data to output file format."""
            client = self.get_client()
        
            formatPrompt = self._get_conversion_prompt(source_format=source_format, target_format=target_format)
            prompt = formatPrompt + data
            response = client.messages.create(model="claude-3-5-sonnet-20241022",max_tokens=1024,messages=[{"role": "user", "content": prompt}])
        
            return response.content[0].text

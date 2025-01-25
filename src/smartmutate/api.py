import os
import anthropic
from typing import Any

from .registry import format_instructions


class ConverterAPI:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def get_client(self):
        return self.client
    
    def _get_conversion_prompt(self,source_format: str, target_format: str) -> str:
        """Get the conversion prompt for the given source and target formats."""

        # Base prompt template focusing on semantic preservation
        base_prompt = (
            f"You are a specialized file format converter. "
            f"Convert the following {source_format} content into {target_format} format. "
            "Preserve all data structure, relationships, and semantic meaning. "
            "Return only the converted output without explanation or additional text.\n\n"
        )

        prompt = base_prompt
        if source_format in format_instructions:
            prompt += f"Input instructions: {format_instructions[source_format]['input']}\n"
        if target_format in format_instructions:
            prompt += f"Output instructions: {format_instructions[target_format]['output']}\n"
            
        return prompt


    def convert(self, data: Any, source_format: str, target_format: str) -> Any:
            """Convert a input file data to output file format."""
            client = self.get_client()
            formatPrompt = self._get_conversion_prompt(source_format=source_format, target_format=target_format)
            prompt = formatPrompt + data
            response = client.messages.create(model="claude-3-5-sonnet-20241022",max_tokens=8192,messages=[{"role": "user", "content": prompt}])
        
            return response.content[0].text

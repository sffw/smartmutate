import os
import anthropic

from .registry import SUPPORTED_FORMATS, CONVERT_PROMPTS

class ConversionAPI:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.SUPPORTED_FORMATS = SUPPORTED_FORMATS

    def get_client(self):
        return self.client

def convert_with_claude(data, data_format):
        """Convert a Python dictionary to a file in the specified format."""
        client = ConversionAPI().get_client()
        dict_string = f"Python Dictionary:\n{str(data)}"
    
        prompt = CONVERT_PROMPTS[data_format] + dict_string
        response = client.messages.create(model="claude-3-5-sonnet-20241022",max_tokens=1024,messages=[{"role": "user", "content": prompt}])
    
        return response.content[0].text
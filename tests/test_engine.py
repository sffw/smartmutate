import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from smartmutate.engine import ConversionEngine
from smartmutate.file_processor import FileProcessor
from smartmutate.api import ConverterAPI

@pytest.fixture
def processor():
    proc = Mock(spec=FileProcessor)
    proc.validate_format.return_value = True
    proc.get_file_format.side_effect = lambda path: path.suffix[1:]
    proc.load_input_data.return_value = '{"test": "data"}'
    return proc

@pytest.fixture
def api():
    conv_api = Mock(spec=ConverterAPI)
    conv_api.convert.return_value = '{"converted": "data"}'
    return conv_api

@pytest.fixture
def paths(tmp_path):
    return {
        'input': tmp_path / "input.json",
        'output': tmp_path / "output.yaml"
    }

def test_init(paths, processor):
    with patch('smartmutate.engine.FileProcessor', return_value=processor):
        engine = ConversionEngine(
            input_path=paths['input'],
            output_path=paths['output'],
            api_key="test-key"
        )
        
        assert engine.input_path == paths['input']
        assert engine.output_path == paths['output']
        assert engine.api_key == "test-key"
        processor.validate_format.assert_called_once()
        processor.load_input_data.assert_called_once()

def test_invalid_format(paths, processor):
    processor.validate_format.return_value = False
    
    with patch('smartmutate.engine.FileProcessor', return_value=processor):
        with pytest.raises(ValueError, match="Invalid input format"):
            ConversionEngine(
                input_path=paths['input'],
                output_path=paths['output'],
                api_key="test-key"
            )

def test_conversion(paths, processor, api):
    with patch('smartmutate.engine.FileProcessor', return_value=processor), \
         patch('smartmutate.engine.ConverterAPI', return_value=api):
        
        engine = ConversionEngine(
            input_path=paths['input'],
            output_path=paths['output'],
            api_key="test-key"
        )
        
        engine.convert()
        
        assert processor.get_file_format.call_count == 2
        api.convert.assert_called_once_with(
            '{"test": "data"}',
            'json',
            'yaml'
        )
        processor.generate_output.assert_called_once_with(
            '{"converted": "data"}',
            paths['output']
        )

def test_conversion_error(paths, processor, api):
    api.convert.side_effect = Exception("API conversion failed")
    
    with patch('smartmutate.engine.FileProcessor', return_value=processor), \
         patch('smartmutate.engine.ConverterAPI', return_value=api):
        
        engine = ConversionEngine(
            input_path=paths['input'],
            output_path=paths['output'],
            api_key="test-key"
        )
        
        with pytest.raises(Exception, match="API conversion failed"):
            engine.convert()
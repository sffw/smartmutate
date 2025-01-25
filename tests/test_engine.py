import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from smartmutate.engine import ConversionEngine
from smartmutate.file_processor import FileProcessor
from smartmutate.api import ConverterAPI

@pytest.fixture
def mock_file_processor():
    """
    Create a mock FileProcessor with predefined behaviors.
    This allows us to isolate the ConversionEngine tests from actual file operations.
    """
    processor = Mock(spec=FileProcessor)
    
    # Set up common mock behaviors
    processor.validate_format.return_value = True
    processor.get_file_format.side_effect = lambda path: path.suffix[1:]
    processor.load_input_data.return_value = '{"test": "data"}'
    
    return processor

@pytest.fixture
def mock_converter_api():
    """
    Create a mock ConverterAPI to simulate Claude API responses.
    This prevents actual API calls during testing.
    """
    api = Mock(spec=ConverterAPI)
    api.convert.return_value = '{"converted": "data"}'
    return api

@pytest.fixture
def test_paths(tmp_path):
    """Create temporary test file paths"""
    return {
        'input': tmp_path / "input.json",
        'output': tmp_path / "output.yaml"
    }

def test_engine_initialization(test_paths, mock_file_processor):
    """
    Test that the ConversionEngine initializes correctly and loads input data.
    This verifies the basic setup of the engine works as expected.
    """
    with patch('smartmutate.engine.FileProcessor', return_value=mock_file_processor):
        engine = ConversionEngine(
            input_path=test_paths['input'],
            output_path=test_paths['output'],
            api_key="test-key"
        )
        
        assert engine.input_path == test_paths['input']
        assert engine.output_path == test_paths['output']
        assert engine.api_key == "test-key"
        
        # Verify FileProcessor was used to validate and load data
        mock_file_processor.validate_format.assert_called_once()
        mock_file_processor.load_input_data.assert_called_once()

def test_get_input_data_invalid_format(test_paths, mock_file_processor):
    """
    Test handling of invalid input formats.
    This ensures the engine properly validates input files before processing.
    """
    mock_file_processor.validate_format.return_value = False
    
    with patch('smartmutate.engine.FileProcessor', return_value=mock_file_processor):
        with pytest.raises(ValueError, match="Invalid input format"):
            engine = ConversionEngine(
                input_path=test_paths['input'],
                output_path=test_paths['output'],
                api_key="test-key"
            )

def test_successful_conversion(test_paths, mock_file_processor, mock_converter_api):
    """
    Test a complete successful conversion workflow.
    This verifies all components work together correctly.
    """
    with patch('smartmutate.engine.FileProcessor', return_value=mock_file_processor), \
         patch('smartmutate.engine.ConverterAPI', return_value=mock_converter_api):
        
        engine = ConversionEngine(
            input_path=test_paths['input'],
            output_path=test_paths['output'],
            api_key="test-key"
        )
        
        # Perform conversion
        engine.convert()
        
        # Verify correct format detection
        assert mock_file_processor.get_file_format.call_count == 2
        
        # Verify API conversion was called with correct formats
        mock_converter_api.convert.assert_called_once_with(
            '{"test": "data"}',  # Input data
            'json',              # Source format
            'yaml'               # Target format
        )
        
        # Verify output generation
        mock_file_processor.generate_output.assert_called_once_with(
            '{"converted": "data"}',  # Converted data
            test_paths['output']      # Output path
        )

def test_conversion_error_handling(test_paths, mock_file_processor, mock_converter_api):
    """
    Test error handling during conversion process.
    This ensures the engine properly handles and propagates errors.
    """
    mock_converter_api.convert.side_effect = Exception("API conversion failed")
    
    with patch('smartmutate.engine.FileProcessor', return_value=mock_file_processor), \
         patch('smartmutate.engine.ConverterAPI', return_value=mock_converter_api):
        
        engine = ConversionEngine(
            input_path=test_paths['input'],
            output_path=test_paths['output'],
            api_key="test-key"
        )
        
        with pytest.raises(Exception, match="API conversion failed"):
            engine.convert()
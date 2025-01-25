import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from smartmutate.converter import Converter
from smartmutate.engine import ConversionEngine

@pytest.fixture
def mock_engine():
    """
    Create a mock ConversionEngine to test the Converter class in isolation.
    This prevents actual file operations and API calls during testing.
    """
    engine = Mock(spec=ConversionEngine)
    return engine

@pytest.fixture
def test_paths(tmp_path):
    """
    Create temporary test paths and files.
    This fixture provides both existing and non-existing paths for testing.
    """
    input_file = tmp_path / "input.json"
    input_file.write_text('{"test": "data"}')  # Create actual input file
    
    return {
        'existing_input': input_file,
        'missing_input': tmp_path / "missing.json",
        'output': tmp_path / "output.yaml"
    }

def test_converter_initialization():
    """
    Test that the Converter initializes correctly with an API key.
    This verifies the basic setup of the converter works as expected.
    """
    converter = Converter(api_key="test-key")
    assert converter.api_key == "test-key"

def test_convert_file_success(test_paths, mock_engine):
    """
    Test successful file conversion through the Converter class.
    This verifies the main conversion workflow works correctly.
    """
    with patch('smartmutate.converter.ConversionEngine', return_value=mock_engine):
        converter = Converter(api_key="test-key")
        
        # Perform conversion
        converter.convert_file(
            str(test_paths['existing_input']),
            str(test_paths['output'])
        )
        
        # Verify ConversionEngine was created with correct parameters
        mock_engine.convert.assert_called_once()

def test_convert_missing_input_file(test_paths):
    """
    Test error handling when input file doesn't exist.
    This ensures proper validation of input files.
    """
    converter = Converter(api_key="test-key")
    
    with pytest.raises(ValueError, match="Input file does not exist"):
        converter.convert_file(
            str(test_paths['missing_input']),
            str(test_paths['output'])
        )

def test_convert_with_paths(test_paths, mock_engine):
    """
    Test conversion using Path objects instead of strings.
    This verifies the converter handles different path input types.
    """
    with patch('smartmutate.converter.ConversionEngine', return_value=mock_engine):
        converter = Converter(api_key="test-key")
        
        # Convert using Path objects
        converter.convert_file(
            test_paths['existing_input'],
            test_paths['output']
        )
        
        mock_engine.convert.assert_called_once()

def test_convert_engine_error(test_paths, mock_engine):
    """
    Test handling of conversion engine errors.
    This ensures errors from the engine are properly propagated.
    """
    mock_engine.convert.side_effect = Exception("Conversion failed")
    
    with patch('smartmutate.converter.ConversionEngine', return_value=mock_engine):
        converter = Converter(api_key="test-key")
        
        with pytest.raises(Exception, match="Conversion failed"):
            converter.convert_file(
                str(test_paths['existing_input']),
                str(test_paths['output'])
            )
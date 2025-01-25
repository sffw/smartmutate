import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from smartmutate.converter import Converter
from smartmutate.engine import ConversionEngine

@pytest.fixture
def engine():
    return Mock(spec=ConversionEngine)

@pytest.fixture
def paths(tmp_path):
    input_file = tmp_path / "input.json"
    input_file.write_text('{"test": "data"}')
    
    return {
        'input': input_file,
        'missing': tmp_path / "missing.json",
        'output': tmp_path / "output.yaml"
    }

def test_init():
    conv = Converter("test-key")
    assert conv.api_key == "test-key"

def test_convert_success(paths, engine):
    with patch('smartmutate.converter.ConversionEngine', return_value=engine):
        conv = Converter("test-key")
        conv.convert_file(str(paths['input']), str(paths['output']))
        engine.convert.assert_called_once()

def test_missing_input(paths):
    conv = Converter("test-key")
    with pytest.raises(ValueError, match="Input file does not exist"):
        conv.convert_file(str(paths['missing']), str(paths['output']))

def test_path_objects(paths, engine):
    with patch('smartmutate.converter.ConversionEngine', return_value=engine):
        conv = Converter("test-key")
        conv.convert_file(paths['input'], paths['output'])
        engine.convert.assert_called_once()

def test_engine_error(paths, engine):
    engine.convert.side_effect = Exception("Conversion failed")
    
    with patch('smartmutate.converter.ConversionEngine', return_value=engine):
        conv = Converter("test-key")
        with pytest.raises(Exception, match="Conversion failed"):
            conv.convert_file(str(paths['input']), str(paths['output']))
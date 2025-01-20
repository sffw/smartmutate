# src/smartMutate/cli/convertCLI.py
import click
from pathlib import Path
import sys
from .fileHandler import load_input, validate_output
from .engine import ConversionEngine
from .api import ConverterAPI

@click.command()
@click.argument("input", type=click.Path(exists=True)) #validate input file as valid path
@click.argument("output", type=click.Path())
def mainCLI(input, output):
    """
    SmartMutator CLI tool for converting files between formats.
    
    Arguments:
        input: Path to the input file
        output: Path where the output file should be written
    """
    try:
        input_path = Path(input)
        output_path = Path(output)

        click.echo("Validating input data...")
        inputData = load_input(input_path)

        click.echo("Validating output path...")
        validOutput  = validate_output(output_path)


        # Create engine instance
        engine = ConversionEngine(
            input_data=inputData[0],
            input_format=inputData[1],
            output_path=validOutput
        )
        api = ConverterAPI()
        api.convert()

        # engine.convert()
        
        # # Show what we're attempting
        # click.echo(f"Converting {input_path} to {output_path}")
        
        # # Perform conversion and get resulting dictionary
        # result = engine.convert()
        
        # # For now, display the dictionary to verify our conversion
        # click.echo("Conversion result (Python dictionary):")
        # click.echo(result)
        
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {str(e)}", err=True)
        sys.exit(1)
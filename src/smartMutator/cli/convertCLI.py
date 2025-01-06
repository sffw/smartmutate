# src/smartMutate/cli/convertCLI.py
import click
from pathlib import Path
import sys
from ..core.engine import ConversionEngine

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def cli(input, output):
    """
    SmartMutator CLI tool for converting files between formats.
    
    Arguments:
        input: Path to the input file
        output: Path where the output file should be written
    """
    try:
        input_path = Path(input)
        output_path = Path(output)

        # Create engine instance
        engine = ConversionEngine(
            input_path=input_path,
            output_path=output_path
        )
        
        # Show what we're attempting
        click.echo(f"Converting {input_path} to {output_path}")
        
        # Perform conversion and get resulting dictionary
        result = engine.convert()
        
        # For now, display the dictionary to verify our conversion
        click.echo("Conversion result (Python dictionary):")
        click.echo(result)
        
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {str(e)}", err=True)
        sys.exit(1)
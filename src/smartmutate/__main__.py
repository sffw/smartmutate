import click
import time
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from .engine import ConversionEngine
from .loading_animation import LoadingAnimation

def load_api_key(env_path: Path | None = None) -> str:
    """Load API key from .env file or environment"""
    if env_path:
        if not env_path.exists():
            raise ValueError(f"Environment file not found: {env_path}")
        load_dotenv(env_path)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment or .env file")
    return api_key

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--api-key", default=None, help="Your Anthropic API key")
@click.option("--env", type=click.Path(exists=True), help="Path to .env file")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def smartmutate(input: str, output: str, api_key: str | None, env: str | None = None, verbose: bool = False) -> None: 
    """
    SmartMutator CLI tool for converting files between formats.
    
    Arguments:
        input: Path to the input file
        output: Path where the output file should be written
    """
    try:
        if not input or not output:
            raise ValueError("Please provide input and output paths")
        
        if not api_key:
            try:
                env_path = Path(env) if env else None
                api_key = load_api_key(env_path)
            except ValueError as e:
                if not env:
                    api_key = click.prompt("Please enter your Anthropic API key", type=str)
                else:
                    raise e
        
        input_path = Path(input)
        output_path = Path(output)

        # Create and start the loading animation
        inputLoading = LoadingAnimation(f"Validating input: {input_path.name}")
        inputLoading.start()
        inputLoading.stop()

          # Create and start the loading animation
        loading = LoadingAnimation(f"Validating output: {output_path.name}")
        loading.start()
        time.sleep(0.5)
        loading.stop()
        try:
            # Create engine instance and perform conversion
            engine = ConversionEngine(
                input_path=input_path,
                output_path=output_path,
                api_key=api_key
            )

            conversionLoading = LoadingAnimation(f"Attempting conversion...")
            conversionLoading.start()
            engine.convert()
            conversionLoading.stop()

            # Stop the animation and show success message
            click.echo(f"\nSuccessfully converted {input_path.name} to {output_path.name}")
            click.echo(f"output file generated at {output_path}")
            
        finally:
            # Ensure the animation is stopped even if an error occurs
            loading.stop()
        
    except ValueError as e:
        click.echo(f"\nError: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nAn unexpected error occurred: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    smartmutate()
import click
import time
import sys
import threading
from pathlib import Path
from .engine import ConversionEngine

class LoadingAnimation:
    """
    A simple loading animation that shows dots appearing and disappearing.
    The animation runs in a separate thread so it doesn't block the main conversion process.
    """
    def __init__(self, description: str = "Converting"):
        self.description = description
        self.is_running = False
        self.thread = None

    def animate(self):
        """Animated loading sequence showing dots appearing and disappearing."""
        while self.is_running:
            for dots in ["   ", ".  ", ".. ", "..."]:
                if not self.is_running:
                    break
                # Clear the current line and show the updated animation frame
                click.echo(f"\r{self.description}{dots}", nl=False)
                time.sleep(0.5)  # Control animation speed
        
        sys.stdout.write("\n")
        sys.stdout.flush()

    def start(self):
        """Start the loading animation in a separate thread."""
        self.is_running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def stop(self):
        """Stop the loading animation."""
        self.is_running = False
        if self.thread:
            self.thread.join()

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def cli(input: str, output: str) -> None:
    """
    SmartMutator CLI tool for converting files between formats.
    
    Arguments:
        input: Path to the input file
        output: Path where the output file should be written
    """
    try:
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
                output_path=output_path
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
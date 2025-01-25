import threading
import time
import sys
import click

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

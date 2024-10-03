"""Module creating the main cli app."""
import rich_click as click
from .api import api


@click.group()
def cli():
    """Simple and basic CLI tool for Matomo"""

cli.add_command(api)

if __name__ == "__main__":
    cli()

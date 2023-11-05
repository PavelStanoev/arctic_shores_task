from typing import Optional
import typer
from arctic_shores import __app_name__, __version__
from .core import export_to_csv

app = typer.Typer()


@app.command()
def version():
    """
    Show the application's version
    """
    typer.echo(f"{__app_name__} v{__version__}")


@app.command()
def export(
    input_json: str = typer.Argument(..., help="Path to the input JSON file."),
    output_csv: str = typer.Argument(..., help="Path to the output CSV file.")
):
    """
    Exports data results to a CSV file.
    """
    export_to_csv(input_json, output_csv)
    typer.echo("CSV file generated successfully.")


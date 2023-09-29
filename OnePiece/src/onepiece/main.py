import typer
from typing_extensions import Annotated
from rich.table import Table
from rich.console import Console
import onepiece.net.net as net


app = typer.Typer()
console = Console()

app.add_typer(net.app, name = "net", help="Network Enum tools.")

   
if __name__ == "__main__":
    app()
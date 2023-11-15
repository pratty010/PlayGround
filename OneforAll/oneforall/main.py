import typer
from typing_extensions import Annotated
from rich.console import Console
from nettools import net
from webtools import web

app = typer.Typer()
console = Console()

app.add_typer(net.app, name = "net", help="Network Enum tools.")
app.add_typer(web.app, name = "web", help="Web Enum tools.")

   
if __name__ == "__main__":
    app()
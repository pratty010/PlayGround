import os
from rich.console import Console

console = Console()

def cpath(path:str, tool:str, file: str) -> str:
    """
    This function take input of `tool`, `file` and `path` and provide back a absolute path for the outfile.

    Arguments:
    path    - Base path, must be aa list.
    tool    - Tool to create the dir in which the output is stored, must be a string.
    file    - Name of the outfile, must be a string.
    """
    
    # Creating dir and file path 
    dir = os.path.join(path, tool)
    fpath = os.path.join(dir, file)
    console.print("[bold yellow][~][/bold yellow][yellow] Creating results file if it doesn't exist --> {}.[/yellow]\n".format(fpath))

    # Create directories recursively
    os.makedirs(dir, exist_ok=True)  # exist_ok=True will prevent any error if the directory already exists

    return fpath

    
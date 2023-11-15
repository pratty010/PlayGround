import os
from rich.console import Console

console = Console()

def cpath(path:str, tool:str, file:str) -> str:
    
    dir = os.path.join(path, tool)
    fpath = os.path.join(dir, file)
    console.print("[bold green][>][/bold green] Creating results file if it doesn't exist --> {}".format(fpath))
    # Create directories recursively
    os.makedirs(dir, exist_ok=True)  # exist_ok=True will prevent any error if the directory already exists
    
    # Create the file
    with open(fpath, 'w') as file:
        pass

    return fpath
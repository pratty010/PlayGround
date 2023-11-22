import os
from rich.console import Console

console = Console()

def cpath(path:str, tool:str) -> str:
    
    file = f"{tool}"
    dir = os.path.join(path, tool)
    fpath = os.path.join(dir, file)
    console.print("\n[bold green][>][/bold green] Creating results file if it doesn't exist --> {}.\n".format(fpath))
    # Create directories recursively
    os.makedirs(dir, exist_ok=True)  # exist_ok=True will prevent any error if the directory already exists
    
    # # Create the file
    # with open(fpath, 'w') as file:
    #     pass

    return fpath
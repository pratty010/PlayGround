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
    
    # to take care of frontal and trailing /
    if len(tool) == 1:
        if tool[0] == "/":
            tool = ""
    else:
        if tool[0] == "/":
            tool = tool[1:]
        if tool[-1] == "/":
            tool = tool[:-1]

    # Creating dir and file path 
    dir = os.path.join(path, tool)
    fpath = os.path.join(dir, file)
    console.print("\n[bold yellow][~][/bold yellow][yellow] Generating results file if it doesn't exist --> {}.[/yellow]".format(fpath))

    # Create directories recursively
    os.makedirs(dir, exist_ok=True)  # exist_ok=True will prevent any error if the directory already exists

    # print(dir, fpath)
    return fpath

    
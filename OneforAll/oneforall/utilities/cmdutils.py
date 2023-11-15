import subprocess
from rich.console import Console
from rich.progress import Progress
import time
import typer

console = Console()

def cmd_run(addr:str, cmd:str, silent:bool, tool:str):
    try:
        if not silent:
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()
            pipe.terminate()
        else:
            with Progress() as progress:
                task = progress.add_task(description="> Looking for open dumb ports.", total = 100)

                # Start the subprocess
                pipe = subprocess.Popen(cmd, shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                
                # While the task is not completed
                while not progress.finished:
                    time.sleep(0.1)
                    progress.update(task, advance=0.5)

                    if pipe.poll() is not None:
                        # If the process has finished, stop the progress bar.
                        progress.update(task, completed=100)
                        progress.stop()
                        break
                pipe.terminate()

    except Exception as err:
        console.print("[bold red][!][/bold red][red] Error raised as >\n[/red]{}".format(err))
        raise typer.Abort()
    finally:
        console.print("[bold green][>][/bold green] {} Scan for {} complete".format(tool.capitalize(), addr))
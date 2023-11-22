import subprocess
import shutil
import sys
from rich.console import Console
from rich.progress import Progress
import time

console = Console()

def bin_check(bin: str):
    path = shutil.which(bin)
    if path:
        console.print(f"\n[bold green][>][/bold green][green] {bin} binary found in system at {path}.[/green]\n")
        return True
    console.print(f"\n[bold red][!][/bold red][red] {bin} binary missing.[/red]\n")
    return False


def cmd_run(addr:str, cmd:str, silent:bool, tool:str):
    console.print(f"\n[bold yellow][~][/bold yellow][yellow] {tool} scan has begun. Wait patiently.[/yellow]\n")

    try:
        if not silent:
            pipe = subprocess.Popen(cmd, shell=True)
            pipe.wait()
            pipe.terminate()
        else:
            with Progress() as progress:
                task = progress.add_task(description="> Shhh. Be quiet. Silent scan underway..", total = 100)

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
        console.print("\n[bold red][!][/bold red][red] Error raised as >\n[/red]{}".format(err))
        sys.exit()
    finally:
        console.print("\n[bold green][>][/bold green] {} Scan for {} complete.\n".format(tool.capitalize(), addr))
import subprocess
import shutil
import sys
import time
from rich.console import Console
from rich.progress import Progress

console = Console()

def bin_check(bin: str) -> bool:
    """
    This function to check if `bin` binary exists on the system or not.
    If yes, move forward with the next part. Else implore user to install it.

    Arguments:
    bin     - The binary to be checked, must be a string.
    """

    # to find path if the binary exists on a Linux system
    path = shutil.which(bin)

    # If not None, bin exists
    if path:
        console.print(f"\n[bold green][>][/bold green][green] {bin} binary found in system at {path}. Moving on..[/green]\n")
        return True
    console.print(f"\n[bold red][!][/bold red][red] {bin} binary missing. Might want to install it and add to your $PATH.[/red]\n")
    return False


def cmd_run(cmd:list, silent:bool, tool:str):
    """
    This function runs the `cmd` supplied either in silent mode or not.
    Proper errors are thrown out to the user.

    Arguments:
    cmd     - The command to be passed to subprocess process open, must be aa list.
    silent  - To not display output to the screen, must be a bool.
    tool    - To supply the tool that is at work, must be a string.
    """

    print_cmd = " ".join(cmd)
    console.print("\n[bold yellow][~][/bold yellow][yellow] {} is at work. Wait patiently.[/yellow]".format(tool.capitalize()))
    console.print(f"[bold yellow][~][/bold yellow][yellow] Initiating command - [/yellow][bold yellow on cyan]{print_cmd}[/bold yellow on cyan]\n")

    try:
        if not silent:
            pipe = subprocess.Popen(cmd)
            pipe.wait()
            pipe.terminate()
        else:
            with Progress() as progress:
                task = progress.add_task(description="[>] SSShhhh. Be quiet. Silent scan underway.\n", total = 100)
                
                # Start the subprocess with stdout to a pipe
                pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # While the task is not completed
                while not progress.finished:
                    time.sleep(0.2)
                    progress.update(task, advance=0.01)
                    if pipe.poll() is not None:
                        # If the process has finished, stop the progress bar.
                        progress.update(task, completed=100)
                        progress.stop()
                        break
                
                # communicate function returns tuple of stdout and stderr once the process finishes
                output, error = pipe.communicate()
                
                # If we get a valid output and error as None - command ran successfully.
                if output.decode() and not error.decode():
                    console.print("[bold green][>][/bold green][green] Command ran successfully !![/green]")
                else:
                    console.print("[bold red][!][/bold red][red] Error raised while executing command as --> {}[/red]".format(error))
                
                # kill the process
                pipe.terminate()

    except Exception as err:
        console.print("\n[bold red][!][/bold red][red] Error raised as >[/red]{}\n".format(err))
        sys.exit()
    finally:
        console.print("\n[bold green][>][/bold green] Work is done. Shutting down.\n")
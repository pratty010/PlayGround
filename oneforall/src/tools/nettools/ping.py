from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
from src.utilities import cmdutils, netutils
import sys

tool = "ping"

console = Console()

def cmd_gen(ip:str, count: int, timeout: int, v6: bool, nop: str) -> list:
    """
    This function creates a ping command with the user flags set.
    It will return a list of the command `cmd` to be input for subprocess module.

    Arguments:
    ip      - IP of the remote host, must be a string.
    count   - The number of ping counts, must be an int.
    timeout - Max time to wait for the response, must be an int.
    v6      - To use an IPv6 protocol, must be a bool.
    nop     - To set additional options for ping command, must be a string.
    """

    #setting command with known flags
    cmd = ["ping", "-W" , f"{timeout}", "-c", f"{count}"]

    # To check if user want to use IPv6  address
    if v6:
        if netutils.ipv6_check(ip):
            cmd.append("-6")
        else:
            console.print("\n[bold red][!][/bold red][red] Wrong IPv6 address format.[/red][cyan] Format be like x.x.x.x.x.x[/cyan]\n")
            sys.exit() 
    
    # To set additional ping flags if supplied. The split is based on space to support subprocess command format.
    if nop:
        cmd.extend(nop.split(" "))

    # adding ip to the end.
    cmd.append(f"{ip}")

    return cmd


def ping_scan(ip: str):
    """
    This function pings the remote IP by calling the ping_scan function.

    Arguments:
    ip  – IP of the remote host, must be a string.
    """
    
    # To check if the binary exists
    if cmdutils.bin_check(tool):
        questions = [
            {
                "type": "number",
                "message": "Number of pings to be sent:",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid integer > 0.",
                "min_allowed": 1,
                "default": 4,
                "name": "count",
            },
            {
                "type": "number",
                "message": "Please provide timeout in seconds:",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid integer > 0.",
                "min_allowed": 5,
                "max_allowed": 20,
                "default": 10,
                "name": "timeout",
            },
            {
                "type": "confirm",
                "message": "Want the turn on a IPv6 scan?:",
                "default": False,
                "name": "ipv6",
            },
            {
                "type": "input",
                "message": "Please provide additional options as needed:",
                "name": "op",
                "long_instruction": "Please check out the ping -h option or man page.",
            },
        ]

        results = prompt(questions=questions)
        # print(results)
        
        cmd = cmd_gen(ip, results["count"], results["timeout"], results["ipv6"], results["op"])
        # print(cmd)

        # to run the command with output to screen
        cmdutils.cmd_run(ip, cmd, False, tool)
    
    # stop the program if not.
    else:
        sys.exit()
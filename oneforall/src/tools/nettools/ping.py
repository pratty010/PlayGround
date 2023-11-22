from InquirerPy import prompt, inquirer
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
from src.utilities import cmdutils, netutils
import sys

tool = "ping"

console = Console()

def cmd_gen(ip:str, count: int, timeout: int, v6: bool):
    cmd = ""
    if v6:
        if netutils.ipv6_check(ip):
            cmd = "ping -6 -W {} -c {} {}".format(timeout, count, ip)
        else:
            console.print("\n[bold red][!][/bold red][red] Wrong IPv6 address format.[/red][cyan] Format be like x.x.x.x.x.x[/cyan]\n")
            sys.exit() 
    else:
        cmd = "ping -W {} -c {} {}".format(timeout, count, ip)

    return cmd


def ping(silent:bool):
    
    if cmdutils.bin_check(tool):

        questions = [
            {
                "type": "number",
                "message": "Number of pings to be sent:",
                "validate": EmptyInputValidator,
                "invalid_message": "Please input a valid integer > 0.",
                "min_allowed": 1,
                "default": 4,
                "name": "count",
            },
            {
                "type": "number",
                "message": "Please provide timeout in seconds:",
                "validate": EmptyInputValidator,
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
            {
            "type": "input",
            "message": "Please input the IP to be scanned:",
            "default": "0.0.0.0",
            "name": "ip",
            "validate": EmptyInputValidator,
            "invalid_message": "IP can't be empty.",
            "validate": netutils.ip_check,
            "invalid_message": "Wrong IP format. Example format - [x.x.x.x , x.google.com, x.x.x.x.x.x].",
            },
        ]

        results = prompt(questions=questions)
        # print(results)
        
        cmd = cmd_gen(results["ip"], results["count"], results["timeout"], results["ipv6"])
        cmdutils.cmd_run(results["ip"], cmd, silent, tool)
from rich.console import Console
from InquirerPy import prompt, inquirer
from InquirerPy.validator import PathValidator, EmptyInputValidator
import sys

from src.tools.nettools import ping, mapper, ftp
from src.utilities import netutils, cmdutils

console = Console()


def mapper_scn(ip: str, outpath: str, silent: bool):
    """
    This function is initiate a network mapper function.

    Arguments:
    ip        - IP of the remote host, must be a string.
    silent    - To turn off output to the shell, must be a bool.
    outpath   - Path for the output file to be stored at, must be an string.
    """ 
    
    questions = [
        {
            "type": "list",
            "message": "What network mapper you want to enumerate with?:",
            "choices": ["Nm4p", "Ru5t5c4n"],
            "default": "Ru5t5c4n",
            "filter": lambda results: "nmap" if results == "Nm4p" else "rustscan", 
            "name": "mapper",
        },
        {
            "type": "list",
            "message": "Please select the format for the results to be stored in:",
            "choices": ["-oN", "-oS", "-oG", "-oX", "-oA"],
            "default": "-oA",
            "name": "format",
            "long_instruction": "-oN: Output scan in normal text\n-oX: Output scan in XML\n-oS: Output scan in s|<rIpt kIddi3 format\n-oG: Output scan in Grepable format\n-oA: Output in the three major formats at once",   
            "when": lambda results: outpath,
        },
    ]

    results = prompt(questions=questions)
    # print(results)

    mapper.mapper_scan(ip, results["format"], outpath, silent, results["mapper"])


def ping_scn(ip: str):
    """
    This function pings the remote IP by calling the ping_scan function.

    Arguments:
    ip  - IP of the remote host, must be a string.
    """
    
    tool= "ping"

    # To check if the binary exists
    if cmdutils.bin_check(tool):
        console.print(f"\n[bold yellow][~][/bold yellow][yellow] Ping is on.[/yellow]\n")
        ping.ping_scan(ip, tool)
    #program exits
    else:
        sys.exit()


def net():
    """
    This function houses all the network enumeration related tools.

    Tools Supported:
    1. Ping - Common tools to ping the host.
    2. Network Mappers - Tools to do active enumeration of the services running on an IP.
        1. Nmap - Commonly known tool for services enumeration.
        2. Rustscan - Nmap on steroids.
    3. FTP - Tool to interact with anonymous FTP logins if allowed.
    """

    console.print(f"\n[bold yellow][~][/bold yellow][yellow] Entering into network toolkit[/yellow]\n")
    
    # To select the network tool of choice
    scan = inquirer.select(
        message="Please select the weapon for enumeration:",
        choices=["P1n9 5c4n", "N37w0rk M4pp3r", "F7P"],
        default="N37w0rk M4pp3r",
        ).execute()
    # print(scan)

    # Collect the IP for scan
    questions = [
        {
            "type": "input",
            "message": "Please input the IP to be scanned:",
            "default": "127.0.0.1",
            "name": "ip",
            "validate": EmptyInputValidator(),
            "invalid_message": "IP can't be empty.",
            "validate": netutils.ip_check,
            "invalid_message": "Wrong IP format. Example format - [x.x.x.x , x.google.com, x.x.x.x.x.x].",
        },
        {
            "type": "confirm",
            "message": "Want the store the results?",
            "default": False,
            "name": "store",
            "long_instruction": "If set to no, the print output to screen will be set to True by default.",
            "when": lambda results: scan in ["N37w0rk M4pp3r", "F7P"]
        },
        {
            "type": "filepath",
            "message": "Please provide the directory to store the results:",
            "default": "./",
            "name": "outpath",
            "validate": PathValidator(is_dir=True),
            "invalid_message": "Not a valid directory.",
            "when": lambda results: results["store"],
        },
        {
            "type": "confirm",
            "message": "Want the scan to be silent?",
            "default": False,
            "name": "silent",
            "long_instruction": "If set to Yes, will not print output to screen as STDOUT.",
            "when": lambda results: results["store"],
        }, 
    ]

    results = prompt(questions=questions)
    # print(results)

    # To set output to screen if store option not set.
    if not results["store"]:
        results["silent"] = False
    # print(results)
    
    if scan == "P1n9 5c4n":
        ping_scn(results["ip"])
    elif scan == "N37w0rk M4pp3r":
        mapper_scn(results["ip"], results["outpath"], results["silent"])
    elif scan == "F7P":
        ftp.ftp_scan(results["ip"], results["outpath"], results["silent"])


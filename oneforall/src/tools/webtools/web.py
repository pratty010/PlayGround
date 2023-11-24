from rich.console import Console

from InquirerPy import prompt, inquirer
from InquirerPy.validator import PathValidator, EmptyInputValidator

from src.tools.webtools.dirb import dirbuster, ffuf, gobuster, feroxbuster
from src.utilities import netutils

console = Console()


def web():
    """
    This function houses all the Web Exploitation related tools.

    Tools Supported:
    1. Directory Buster - To brute force directories.
        1. Dirb - One of the oldest and most reliable tool.
        2. GoBuster - Faster and built in GO.
        3. FeroxBuster- Most Reliable and widely used.
        4. FFUF - Fast Web Fuzzer Created in Go.
    2. Virtual Host Scanner - To find virtual subdomains for the given host URL.
        1. GoBuster - Faster and built in GO.
        2. FFUF - Fast Web Fuzzer Created in Go.
    """
    console.print(f"\n[bold yellow][~][/bold yellow][yellow] Entering into web exploit toolkit[/yellow]\n")
    
    scan = inquirer.select(
        message="Please select the weapon for web exploit:",
        choices=["D1r3ct0ry Bru73f0rc1n9", "V1rtu4l H05t5 5c4n"],
        ).execute()
    
    # print(scan)

    questions = [
        {
            "type": "list",
            "message": "What dirbuster you want to employ?:",
            "choices": ["D1r6", "G0bu5t3r", "F3r0xBu5t3r", "FFUF"],
            "default": "F3r0xBu5t3r",
            "name": "dirb_tool",
            "when": lambda results: scan == "D1r3ct0ry Bru73f0rc1n9",
        },
        {
            "type": "list",
            "message": "What dirbuster you want to employ?:",
            "choices": ["G0bu5t3r", "FFUF"],
            "default": "G0bu5t3r",
            "name": "vhost_tool",
            "when": lambda results: scan == "V1rtu4l H05t5 5c4n",
        },
        {
            "type": "input",
            "message": "Please provide the URL to be scanned:",
            "name": "url",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please provide an input.",
            "validate": netutils.dns_check,
            "invalid_message": "Not a valid URL.",
        },
        {
            "type": "filepath",
            "message": "Please provide the wordlist for bruteforcing:",
            "default": "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "name": "wordlist",
            "validate": PathValidator(is_file=True),
            "invalid_message": "Not a valid file.",
        },
        {
            "type": "confirm",
            "message": "Want the store the results?",
            "default": False,
            "name": "store",
            "long_instruction": "If set to no, the print output to screen will be set to True by default."
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

    # invoke the correct fuzzer
    if results["dirb_tool"] == "D1r6":
        dirbuster.dirb_scan(results["url"], results["wordlist"], results["silent"], results["outpath"])
    elif results["dirb_tool"] == "F3r0xBu5t3r":
        feroxbuster.ferox_scan(results["url"], results["wordlist"], results["silent"], results["outpath"])
    elif results["dirb_tool"] == "G0bu5t3r" or results["vhost_tool"] == "G0bu5t3r":
        print("Go Goa Gone.")
    elif results["dirb_tool"] == "FFUF" or results["vhost_tool"] == "FFUF":
        print("Fuzzer at FFUFFFFF.")
        


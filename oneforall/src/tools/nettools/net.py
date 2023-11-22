from rich.console import Console

from InquirerPy import prompt, inquirer
from InquirerPy.validator import PathValidator

from src.tools.nettools import ping, mapper

console = Console()

def net():
    console.print(f"\n[bold yellow][~][/bold yellow][yellow] Entering into network toolkit[/yellow]\n")
    
    scan = inquirer.select(
        message="Please select the weapon for enumeration:",
        choices=["Ping Scan", "Network Mapper"],
        default="Network Mapper",
        ).execute()
    
    # print(scan)

    questions = [
        {
            "type": "list",
            "message": "What network mapper you want to enumerate with?:",
            "choices": ["Nmap", "Rustscan"],
            "default": "Rustscan",
            "name": "mapper",
            "when": lambda results: scan == "Network Mapper",
        },
        {
            "type": "confirm",
            "message": "Want the scan to be silent?",
            "default": False,
            "name": "silent",
            "long_instruction": "No output to the screen if set.",
        },
        {
            "type": "confirm",
            "message": "Want the store the results?",
            "default": False,
            "name": "store",
            "when": lambda results: scan == "Network Mapper",
        },
        {
            "type": "list",
            "message": "Please select the format for the results to be stored in:",
            "choices": ["-oN", "-oS", "-oG", "-oX", "-oA"],
            "default": "-oN",
            "name": "format",
            "long_instruction": "-oN: Output scan in normal text\n-oX: Output scan in XML\n-oS: Output scan in s|<rIpt kIddi3 format\n-oG: Output scan in Grepable format\n-oA: Output in the three major formats at once",   
            "when": lambda results: results["store"],
        },
        {
            "type": "filepath",
            "message": "Please provide the directory to store the results:",
            "default": "./",
            "name": "outpath",
            "validate": PathValidator(is_dir=True),
            "invalid_message": "Not a directory.",
            "when": lambda results: results["store"],
        },
    ]

    results = prompt(questions=questions)
    # print(results)
    
    if scan == "ping scan":
        ping.ping(results["silent"])
    elif scan == "Network Mapper":
        mapper.mapper_scan(results["silent"], results["format"], results["outpath"], results["mapper"])


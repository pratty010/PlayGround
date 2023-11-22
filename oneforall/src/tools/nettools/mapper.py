from InquirerPy import prompt, inquirer
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
from src.utilities import cmdutils, netutils, pathutils


console = Console()

def cmd_gen(addr: str, ports: str, scan_type: str, format: str, outpath: str, timing: int, nop: str, verbose: str, tool:str) -> str:

    portsc = netutils.port_check(ports, tool)
    flags = ""
    cmd = ""

    
    if nop:
        if tool == "nmap":
            flags = "{} -T{} {} {} {} ".format(verbose, timing, portsc, nop, scan_type)
        elif tool == "rustscan":
            flags = "{} -a {} -- -T{} {} {} ".format(portsc, addr, timing, nop, scan_type)
    else:
        if tool == "nmap":
            flags = "{} -T{} {} {} ".format(verbose, timing, portsc, scan_type)
        elif tool == "rustscan":
            flags = "{} -a {} -- -T{} {} ".format(portsc, addr, timing, scan_type)
        
    # print(flags)

    if outpath and format:
        console.print("\n[bold yellow][~][/bold yellow][yellow] File store mode - On!")
        spath = pathutils.cpath(outpath, tool)
        console.print("[bold yellow][~][/bold yellow][yellow] Check results at {}\n".format(spath))
        flags += "{} {} ".format(format, spath)
    else:
        pass
        # // add more cases 
    # print(flags)

    if tool == "nmap":
        cmd = "sudo nmap {} {}".format(flags, addr)
    elif tool == "rustscan":
        cmd = "rustscan {}".format(flags)

    return cmd


def mapper_scan(silent: bool, format: str, outpath: bool, mapper: str):
    
    tool = "nmap" if mapper == "Nmap" else "rustscan"

    if cmdutils.bin_check(tool):

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
                "type": "list",
                "message": "Please provide the scan type:",
                "choices": ["-sC", "-sV", "-O" ,"-sC -sV", "-A"],
                "default": "-sC -sV",
                "long_instruction": "-sC: equivalent to --script=default\n-sV: Probe open ports to determine service/version info\n-O: Enable OS detection\n-A: Enable OS detection, version detection, script scanning, and traceroute",
                "name": "scan_type",
            },
            {
                "type": "confirm",
                "message": "Auto mode on. Want me to do the heavy lifting?:",
                "default": False,
                "name": "auto",
            },
            {
                "type": "number",
                "message": "Please provide timing settings for scan:",
                "min_allowed": 1,
                "max_allowed": 5,
                "default": 3,
                "name": "timing",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input something.",
                "filter": lambda results: int(results),
                "when": lambda results: results["auto"] == False,
            },
            {
                "type": "list",
                "message": "Want to run a full port scan?:",
                "choices": ["Yuss", "Non"],
                "default": "Non",
                "name": "all",
                "when": lambda results: results["auto"] == False,
            },
            {
                "type": "input",
                "message": "Please input the ports to scan:",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid set as a, b, c.",
                "name": "ports",
                "default": "1-1024",
                "when": lambda results: results["all"] == "Non" and results["auto"] == False,
            },
            {
                "type": "input",
                "message": "Please provide additional options as needed:",
                "name": "op",
                "long_instruction": "Please check out the nmap -h option or man page.",
                "when": lambda results: results["auto"] == False,
            },
            {
                "type": "list",
                "message": "Please select the verbosity level for the scan:",
                "choices": ["-v", "-vv", "-vvv"],
                "default": "-v",
                "name": "verbose",
                "instruction": "Default is set to none.",
                "when": lambda results: results["auto"] == False,
            }
            
        ]

        results = prompt(questions=questions)
        print(results, tool)
        
        if results["auto"]:
            results["timing"] = 3
            results["ports"] = "1-65535"
            results["verbose"] = "-vv"
        
        if results["all"] == "Yuss":
            results["ports"] = "1-65535"

        print(results, tool)
        
        cmd = cmd_gen(results["ip"], results["ports"], results["scan_type"],format,  outpath, results["timing"], results["op"], results["verbose"], tool)
        print(cmd)
        cmdutils.cmd_run(results["ip"], cmd, silent, tool)
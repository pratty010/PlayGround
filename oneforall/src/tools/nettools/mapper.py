from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
import sys

from src.utilities import cmdutils, netutils, pathutils

# creating an instance of rich console.
console = Console()

def outpath_gen(outpath: str, format: str, tool: str, file: str) -> str:
    """
    This function helps in generate output file path for mappers.
    Returns the file path `pflag` to be added tot he command.

    Arguments:
    format    - Format for output file, must be an string.
    outpath   - Path for the output file to be stored at, must be an string.
    tool      - To select the mapper for the scan, must be a string.
    """

    console.print("\n[bold yellow][~][/bold yellow][yellow] File store mode - On![/yellow]")
    spath = pathutils.cpath(outpath, tool, file)
    pflags = "{} {}".format(format, spath)


    return pflags


def cmd_gen_nmap(ip: str, ports: str, scan_type: str, format: str, outpath: str, timing: int, nop: str, verbose: str, tool:str) -> str:
    """
    This function helps in generating command for nmap tool.
    Returns the command `cmd` to executed in string format.

    Arguments:
    ip        - IP of the remote host, must be a string.
    ports     - Specific ports to be scanned on the remote host, must be a string.
    scan_type - Type of scan that you want to perform, must be a string.
    format    - Format for output file, must be an string.
    outpath   - Path for the output file to be stored at, must be an string.
    timing    - To turn off output to the shell, must be a bool.
    nop       - To set additional options for nmap command, must be a string.
    verbose   - To set the verbosity level on the scan, must be a string
    tool      - To select the mapper for the scan, must be a string.
    """
    
    # set command with known flags
    cmd = ["sudo", "nmap", f"{verbose}", f"-T{timing}"]

    # add ports if they are manually set
    if ports:
        cmd.extend(ports.split(" "))

    # To set the scan type
    if scan_type != "None":
        cmd.extend(scan_type.split(" "))

    # To check for any additional flags supplied
    if nop:
        cmd.extend(nop.split(" "))
    
    # To set the output file path
    if outpath and format:
        oflag = outpath_gen(outpath, format, tool, "nmap")
        cmd.extend(oflag.split(" "))
    
    
    # adding IP at the end
    cmd.append(f"{ip}")

    return cmd

def cmd_gen_rust(ip: str, ports: str, scan_type: str, format: str, outpath: str, nop: str, tool:str) -> str:
    """
    This function helps in generating command for rustscan tool.
    Returns the command `cmd` to executed in string format.

    Arguments:
    ip        - IP of the remote host, must be a string.
    ports     - Specific ports to be scanned on the remote host, must be a string.
    scan_type - Type of scan that you want to perform, must be a string.
    format    - Format for output file, must be an string.
    outpath   - Path for the output file to be stored at, must be an string.
    nop       - To set additional options for nmap command, must be a string.
    tool      - To select the mapper for the scan, must be a string.
    """

    cmd = ["rustscan"]

    # add ports if they are manually set
    if ports:
        cmd.extend(ports.split(" "))
    
    # adding IP address
    cmd.extend(["-a", f"{ip}", "--"])
    
    # To set command according to scan type
    if scan_type in ['-O', '-A']:
        console.print("\n[bold yellow][>][/bold yellow][yellow] OS detection set. Will need to run as sudo.[/yellow]\n")
        cmd.insert(0, "sudo")
        cmd.append(f"{scan_type}")
    elif scan_type == "None":
        pass
    else:
       cmd.extend(scan_type.split(" "))

    # To check for any additional flags supplied
    if nop:
        cmd.extend(nop.split(" "))

    # To set the output file path
    if outpath and format:
        oflag = outpath_gen(outpath, format, tool, "rustscan")
        cmd.extend(oflag.split(" "))

    # print(flags)

    return cmd

def mapper_scan(ip:str, format: str, outpath: bool, silent: bool, tool: str):
    """
    This function invokes the network mapper functionality.

    Arguments:
    ip      - IP of the remote host, must be a string.
    format  - Format for output file, must be an string.
    outpath - Path for the output file to be stored at, must be an string.
    silent  - To turn off output to the shell, must be a bool.
    tool    - To select the mapper for the scan, must be a string.
    """

    if cmdutils.bin_check(tool):
        console.print(f"\n[bold yellow][~][/bold yellow][yellow] Let's Map the IP.[/yellow]\n")
        
        questions = [
            {
                "type": "confirm",
                "message": "Auto mode on. Want me to do the heavy lifting?:",
                "default": False,
                "name": "auto",
            },
            {
                "type": "list",
                "message": "Please provide the scan type:",
                "choices": ["-sC", "-sV", "-O" ,"-sC -sV", "-A", "None"],
                "default": "-sC -sV",
                "long_instruction": "-sC: equivalent to --script=default\n-sV: Probe open ports to determine service/version info\n-O: Enable OS detection\n-A: Enable OS detection, version detection, script scanning, and traceroute",
                "name": "scan_type",
                "when": lambda results: not results["auto"]
            },
            {
                "type": "number",
                "message": "Please set timing settings for scan:",
                "min_allowed": 1,
                "max_allowed": 5,
                "default": 3,
                "name": "timing",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input something.",
                "filter": lambda results: int(results),
                "when": lambda results: not results["auto"] and tool == "nmap",
            },
            {
                "type": "confirm",
                "message": "Want to run a full port scan?:",
                "name": "all",
                "transformer": lambda result: "Yuss" if result else "Non",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "input",
                "message": "Please input the ports to scan:",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid set as a, b, c.",
                "name": "ports",
                "default": "1-1024",
                "when": lambda results: not results["all"] and not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide additional options as needed:",
                "name": "op",
                "long_instruction": "Please check out the nmap -h option or man page.",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "list",
                "message": "Please select the verbosity level for the scan:",
                "choices": ["-v", "-vv", "-vvv"],
                "default": "-v",
                "name": "verbose",
                "long_instruction": "Default is set to none.",
                "when": lambda results: not results["auto"] and tool == "nmap",
            },
        ]

        results = prompt(questions=questions)
        # print(results, tool)
        
        # To set options for automated scan
        if results["auto"]:
            results["scan_type"] = "-sC -sV"
            results["timing"] = 3
            results["ports"] = "1-65535"
            results["verbose"] = "-vv"
        
        if results["all"]:
            results["ports"] = "1-65535"

        # To check if the ports supplied are the right format for the tool
        ports = netutils.port_check(results["ports"], tool)
        
        # generate command based on the tool.
        cmd = ""
        if tool == "nmap":
            cmd = cmd_gen_nmap(ip, ports, results["scan_type"], format, outpath, results["timing"], results["op"], results["verbose"], tool)
        elif tool == "rustscan":
            cmd= cmd_gen_rust(ip, ports, results["scan_type"], format, outpath, results["op"], tool)
        # print(cmd)
        
        if tool == "nmap" or results["scan_type"] in ["-O", "-A"] and silent:
            silent = False

        # Run the command as shown.
        cmdutils.cmd_run(cmd, silent, tool)

    else:
        sys.exit()
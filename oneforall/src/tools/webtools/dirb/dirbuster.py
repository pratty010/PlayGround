from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
import sys

from src.utilities import cmdutils, pathutils

console = Console()

tool = "dirb"

def outpath_gen(outpath: str, file:str) -> str:
    """
    This function helps in generate output file path for the saved output.
    Returns the file path `pflag` to be added tot he command.

    Arguments:
    outpath   - Path for the output file to be stored at, must be an string.
    file      - Out-file name, must be a string.
    """
    console.print("\n[bold yellow][~][/bold yellow][yellow] File store mode - On!")
    spath = pathutils.cpath(outpath, tool, file)
    pflags = "-o {}".format(spath)

    return pflags


def cmd_gen(url: str, wordlist: str, extensions: str, cookie: str, ua: str, outpath: str, verbose: str, nop: str) -> str:
    """
    This function helps in generating command for dirb tool.
    Returns the command `cmd` to executed in string format.

    Arguments:
    url        - URL of the remote host, must be a string.
    wordlist   - Path to wordlist with common directory namelist, must be a string.
    extensions - Set of extensions to be used to generate the brute list, must be a string.
    cookie     - Optional cookie to be supplied, must be an string.
    ua         - Optional custom User-Agent to be supplied, must be an string.
    outpath    - Path for the output file to be stored at, must be an string.
    verbose    - If you want to set the verbosity option on, must be a bool.
    nop        - To set additional options for dirb command, must be a string.
    """

    cmd = ["dirb", f"{url}", f"{wordlist}"]

    # set all the supplied flags
    if verbose:
        cmd.append("-v")
    if extensions:
        cmd.extend(["-X", f"{extensions}"])
    if cookie:
        cmd.extend(["-c", f"{cookie}"])
    if ua:
        cmd.extend(["-a", f"{ua}"])
    if nop:
        cmd.extend(nop.split(" "))
    if outpath:
        oflag = outpath_gen(outpath, "dirb.txt")
        cmd.extend(oflag.split(" "))

    return cmd

def dirb_scan(url: str, wordlist: str, silent: bool, outpath: str):
    """
    This function helps in generating command for dirb scan.
    Takes all the user's flag that are supplied and run's the dirb scan.

    Arguments:
    url       - Remote host URL to be dir-busted, must be a string.
    wordlist  - Path to wordlist with common directory namelist, must be a string.
    silent    - To turn off output to the shell, must be a bool.
    outpath   - Path for the output file to be stored at, must be an string.
    """

    if cmdutils.bin_check(tool):
        console.print(f"\n[bold yellow][~][/bold yellow][yellow] You choose dirb, boomer !![/yellow]\n")

        questions = [
            {
                "type": "confirm",
                "message": "Auto mode - Do you want to me to decide for you?:",
                "default": False,
                "name": "auto",
            },
            {
                "type": "confirm",
                "message": "Do you want to add some file extensions in the mix?:",
                "default": False,
                "name": "extension_check",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide the set of extensions to be scanned for:",
                "default": ".html,.js,.txt",
                "name": "extensions",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid set of extensions.",
                "when": lambda results: results["extension_check"] and not results["auto"],
            },
            {
                "type": "confirm",
                "message": "Do you want to set a cookie?:",
                "default": False,
                "name": "cookie_check",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide the cookie string:",
                "name": "cookie",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid cookie.",
                "when": lambda results: results["cookie_check"] and not results["auto"],
            },
            {
                "type": "confirm",
                "message": "Do you want to set a custom user-agent?:",
                "default": False,
                "name": "ua_check",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide the user agent:",
                "name": "user_agent",
                "long_instruction": "Might wanna proxy the request to know what it is.",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid user-agent string.",
                "when": lambda results: results["ua_check"] and not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide additional options if required:",
                "name": "op",
                "long_instruction": "Please check out the dirb option or man page.",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "confirm",
                "message": "Do you want to set on the verbosity option?:",
                "default": False,
                "name": "verbose",
                "when": lambda results: not results["auto"],
            },
            
        ]

        results = prompt(questions=questions)
        
        # setting common extensions for auto mode
        if results["auto"]:
            results["extensions"] = "js,txt,html"
        # print(results)
        
        cmd = cmd_gen(url, wordlist, results["extensions"], results["cookie"], results["user_agent"], outpath, results["verbose"], results["op"])
        print(cmd)

        # command run
        cmdutils.cmd_run(cmd, silent, tool)

    else:
        sys.exit()
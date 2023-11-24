from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console
import sys

from src.utilities import cmdutils, pathutils

console = Console()

tool = "feroxbuster"

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


def cmd_gen(url: str, wordlist: str, outpath: str, threads: int, extensions: str, sc_check: str, sc: str, res_check: str, response: str, cookie: str, recursive: bool, verbose: str, nop: str) -> str:
    """
    This function helps in generating command for dirb tool.
    Returns the command `cmd` to executed in string format.

    Arguments:
    url        - URL of the remote host, must be a string.
    wordlist   - Path to wordlist with common directory namelist, must be a string.
    outpath    - Path for the output file to be stored at, must be an string.
    threads    - Concurrent scans you want to initiate, must be an int.
    extensions - Set of extensions to be used to generate the brute list, must be a string.
    sc_check   - To store the kind of status code filter, must be a string.
    sc         - Store value for the filtered status codes, must be a string.
    res_check  - To store the kind of response size filters, must be a string.
    response   - Store value for the filtered response sizes, must be a string.
    cookie     - Optional cookie to be supplied, must be an string.
    recursive  - To set scan to be non-recursive. Recursive by default, must be an string.
    verbose    - If you want to set the verbosity option on, must be a bool.
    nop        - To set additional options for ferox command, must be a string.
    """

    # basic command
    cmd = ["feroxbuster", f"{verbose}", "-t" , f"{threads}", "-u", f"{url}", "-w", f"{wordlist}"]

    # set all the supplied flags
    if extensions:
        cmd.extend(["-x", f"{extensions}"])
    if cookie:
        cmd.extend(["-c", f"{cookie}"])
    if recursive:
        cmd.append("-n")
    if nop:
        cmd.extend(nop.split(" "))
    
    # add filter status codes
    if sc_check != "No":
        if sc_check == "Allowlist Response Codes":
            cmd.extend(["-s", f"{sc}"])
        elif sc_check == "Blacklist Response Codes":
            cmd.extend(["-C", f"{sc}"])

    # add filters based on responses
    if res_check != "No": 
        if res_check == "Response Size":
            cmd.extend(["-S", f"{response}"])
        elif res_check == "Response Words Count":
            cmd.extend(["-W", f"{response}"])
        elif res_check == "Response Lines Count":
            cmd.extend(["-N", f"{response}"])
    
    # add output file
    if outpath:
        oflag = outpath_gen(outpath, "ferox.txt")
        cmd.extend(oflag.split(" "))

    return cmd

def ferox_scan(url: str, wordlist: str, silent: bool, outpath: str):
    """
    This function helps in generating command for feroxbuster scan.
    Takes all the user's flag that are supplied and run's the feroxbuster scan.

    Arguments:
    url       - Remote host URL to be dir-busted, must be a string.
    wordlist  - Path to wordlist with common directory namelist, must be a string.
    silent    - To turn off output to the shell, must be a bool.
    outpath   - Path for the output file to be stored at, must be an string.
    """

    if cmdutils.bin_check(tool):
        console.print(f"\n[bold yellow][~][/bold yellow][yellow] FeroxBuster is in trend. You choose well.[/yellow]\n")
        questions = [
            {
                "type": "confirm",
                "message": "Want to run on the auto mode?:",
                "default": False,
                "name": "auto",
                "long_instruction": "I will take over from here. Thank you for your efforts.",
            },
            {
                "type": "number",
                "message": "Please provide threads:",
                "name": "threads",
                "long_instruction": "Number of concurrent threads. Might take a toll on your connection. Choose wisely.",
                "min_allowed": 0,
                "max_allowed": 250,
                "default": 50,
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid thread > 0.",
                "when": lambda results: not results["auto"],
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
                "default": "html,js,txt",
                "name": "extensions",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid set of extensions.",
                "when": lambda results: results["extension_check"] and not results["auto"],
            },
            {
                "type": "list",
                "message": "Do you want to filter the response based on content's status-codes? Here are some choices:",
                "choices": ["Allowlist Response Codes", "Blacklist Response Codes", "No"],
                "default": "No",
                "name": "status_code_check",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide a set of status codes:",
                "name": "sc",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid set of valid status codes.",
                "when": lambda results: results["status_code_check"] != "No" and not results["auto"],
            },
            {
                "type": "list",
                "message": "Do you want to filter the response based on content? Here are some choices:",
                "choices": ["Response Size", "Response Words Count", "Response Lines Count", "No"],
                "default": "No",
                "long_instruction": "Response Size: Filter out messages of a particular size. Lookout for column with format [*c].\nResponse Words Count: Filter out messages of a particular word count. Lookout for column with format [*w].\nResponse Lines Count: Filter out messages of a particular line count. Lookout for column with format [*l].",
                "name": "response_check",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "input",
                "message": "Please provide a proper size:",
                "name": "response",
                "long_instruction": "Number of concurrent threads. Might take a toll on your connection. Choose wisely.",
                "validate": EmptyInputValidator(),
                "invalid_message": "Please input a valid set of numbers.",
                "when": lambda results: results["response_check"] != "No" and not results["auto"],
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
                "type": "input",
                "message": "Please provide additional options if required:",
                "name": "op",
                "long_instruction": "Please check out the feroxbuster option or man page.",
                "when": lambda results: not results["auto"],
            },
            {
                "type": "confirm",
                "message": "Non-recursive search if you are in a hurry?:",
                "default": False,
                "name": "recursive",
            },
            {
                "type": "list",
                "message": "Please select the verbosity level for the scan:",
                "choices": ["-v", "-vv", "-vvv"],
                "default": "-v",
                "name": "verbose",
                "long_instruction": "Default is set to none.",
                "when": lambda results: not results["auto"],
            },
        ]

        results = prompt(questions=questions)
        # print(results)

        # set options for an auto scan
        if results["auto"]:
            results["extensions"] = "js,txt,html"
            results["threads"] = 70
            results["verbose"] = "-v"
        # print(results)
        
        cmd = cmd_gen(url, wordlist, outpath, results["threads"], results["extensions"], results["status_code_check"], results["sc"], results["response_check"], results["response"], results["cookie"], results["recursive"], results["verbose"], results["op"])
        # print(cmd)

        cmdutils.cmd_run(cmd, silent, tool)

    else:
        sys.exit()
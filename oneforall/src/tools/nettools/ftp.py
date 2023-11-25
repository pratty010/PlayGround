import ftplib
from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator, PathValidator
from rich.console import Console
from src.utilities import pathutils
import sys

# creating a rich Console instance
console = Console()

# FTP Instance
ftp = ftplib.FTP()
tool = "ftp"


def file_upload(ftp, silent: bool) -> str:
    """
    This function uploads file to remote server.

    Arguments:
    ftp       - FTP login instance.
    silent    - To turn off output to the shell, must be a bool.
    """

    questions = [
        {
            "type": "input",
            "message": "Please provide the path of the file to be uploaded:",
            "name": "filepath",
            "default": "./",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please provide a valid file path.",
            "validate": PathValidator(is_file=True),
            "invalid_message": "Not a valid file.",
        },
        {
            "type": "input",
            "message": "Please provide the remote directory where to put the file:",
            "name": "remote_dir",
            "default": "/",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please provide a valid remote directory.",
        },
        {
            "type": "input",
            "message": "Please provide the remote file name:",
            "name": "remote",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please provide a valid file name with proper extension.",
        },
    ]
    
    results = prompt(questions=questions)

    try:
        # setting the remote dir to upload the file to 
        if results["remote_dir"] == "/":
            pwd = ftp.pwd()
        else:
            pwd = results["remote_dir"]
        
        # Migrating into the remote directory supplied
        ftp.cwd(pwd)
        if not silent:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Migrating into remote directory supplied > {pwd}[/yellow]")
        
        if not silent:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Trying to upload the file to the remote server.[/yellow]")
        
        # Open the file you want to upload in binary mode
        file = open(f'{results["filepath"]}', 'rb')
        # Use the storbinary method to upload the file with the STOR command
        ftp.storbinary(f'STOR {results["remote"]}', file)
        # Close the file
        file.close()
    # Any FTP Errors
    except Exception as err:
        if not silent:
            console.print("\n[bold red][!][/bold red][red] Error raised as > {}[/red]".format(err))
        sys.exit()

def file_download(ftp, pwd: str, outpath: str, silent: bool):
    """
    This function downloads ftp files recursively from FTP remote server.

    Arguments:
    ftp       - FTP login instance.
    pwd       - Present working directory for the FTP Root, must be a string.
    silent    - To turn off output to the shell, must be a bool.
    outpath   - Path for the output file to be stored at, must be an string.
    """
    try:
        # changing into the source ftp dir supplied
        ftp.cwd(pwd)
        # Printing dir listing of current working directory
        if not silent:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Migrating into current working directory > {pwd}[/yellow]")
        
        # Storing files/directories of CWD
        files = ftp.nlst()

        # checking for empty dirs
        if len(files) == 0:
            if not silent:
                console.print(f"[bold yellow][~][/bold yellow][yellow] {pwd} is an empty directory.[/yellow]")
            return

        if not silent:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Directory listing:[/yellow]")
            ftp.retrlines('LIST')

        # Recursing through every file in CWD
        if not silent:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Checking for dir/files in CWD.[/yellow]")
        for file in files:
            try:
                # Trying to change to the file name, assuming it is a directory
                ftp.cwd(pwd + file)
                if not silent:
                    console.print(f"\n[bold yellow][~][/bold yellow][yellow] {file} is a directory. Will dig into it.[/yellow]")

                # recursively download the directory
                file_download(ftp, pwd + file + "/", outpath, silent)
            
            except ftplib.error_perm as err:
                if not silent:
                    console.print(f"\n[bold green][>][/bold green][green] {file} is a file. Let's download it to local.[/green]")
                
                # Checking if the local directory exists
                outf = pathutils.cpath(outpath, pwd, file)
                # the file name is not a directory, it is a file
                with open(outf, "wb") as f: # open a local file in binary write mode
                    try:
                        ftp.retrbinary(f"RETR {file}", f.write) # download the file from the FTP server and write it to the local file
                        if not silent:
                            console.print(f"[bold green][>][/bold green][green] {file} is downloaded to local.[/green]")
                    except ftplib.error_perm as err:
                        if not silent:
                            console.print("[bold red][!][/bold red][red] Couldn't download this file. Try other methods manually.[/red]")
                f.close()

        # Proper return code to show download is finished
        return "Files Downloaded", pwd
    
    # Any FTP Errors
    except Exception as err:
        if not silent:
            console.print("\n[bold red][!][/bold red][red] Error raised as > {}[/red]".format(err))
        return err.args[0], pwd

    

def login(ip:str, port: int, username: str, password: str, err: bool):
    """
    This function logs into the FTP service at a port and with creds.
    The function returns a ftp instance if logged in.

    Arguments:
    ip        - IP of the remote host, must be a string.
    port      - port for FTP service, must be an int.
    username  - Username for the ftp login, must be an string.
    password  - Password for the ftp login, must be an string.
    err       - Error to be set to have an intermediary login, must be a bool.
    """
    try:
        # create a ftp instance to an IP and Port
        ftp.connect(ip, port) 

        # different username:password use cases
        if username == "anonymous" and password == "" and not err:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Checking for ANONymous FTP login on {ip}.[/yellow]")
            ftp.login("anonymous", "" )
        elif username and password and not err:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Checking for FTP login on {ip} for {username}.[/yellow]")
            ftp.login(f"{username}", f"{password}")
        else:
            console.print(f"\n[bold yellow][~][/bold yellow][yellow] Creating new FTP Login Instance due to Error raised.[/yellow]")
            ftp.login(f"{username}", f"{password}")

        console.print("\n[bold green][>][/bold green][green] FTP login was the successful. Onto next task..[/green]\n")
        return ftp
    # In case of a login failure.
    except Exception as err:
        console.print("\n[bold red][!][/bold red][red] Error raised as > {}[/red]".format(err))
        sys.exit()
       


def ftp_scan(ip: str, outpath:str, silent: bool):
    """
    This function searches the FTP shares and provides other FTP operations.

    Arguments:
    ip        - IP of the remote host, must be a string.
    silent    - To turn off output to the shell, must be a bool.
    outpath   - Path for the output file to be stored at, must be an string.
    """
    
    questions = [
        {
            "type": "confirm",
            "message": "Auto mode on. I will FTP the shit out:",
            "default": False,
            "name": "auto",
            "long_instruction": "This is CTF mode. Check anonymous login, download it all.",
        },
        {
            "type": "number",
            "message": "Please provide the port for the FTP service:",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please input a valid port number.",
            "min_allowed": 0,
            "max_allowed": 65535,
            "default": 21,
            "name": "port",
            "filter": lambda results: int(results),
            "when": lambda results: not results["auto"]
        },
        {
            "type": "confirm",
            "message": "Do you want to login anonymously?:",
            "default": True,
            "name": "anon",
            "when": lambda results: not results["auto"],
        },
        # # To add test for brute force case
        # {
        #     "type": "confirm",
        #     "message": "Do you want to brute force the login?:",
        #     "default": False,
        #     "name": "brute",
        # },
        {
            "type": "input",
            "message": "Please provide the username for login:",
            "name": "username",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please provide a valid username.",
            "when": lambda results: not results["anon"] and not results["auto"],
        },
        {
            "type": "password",
            "message": "Please provide the password for login:",
            "name": "password",
            "validate": EmptyInputValidator(),
            "invalid_message": "Please provide a valid password.",
            "when": lambda results: not results["anon"] and not results["auto"],
        },
         {
            "type": "list",
            "message": "Want to download or upload some information?:",
            "choices": ["Upload Files to Remote FTP server", "Download Files from FTP server", "None"],
            "default": "Download Files from FTP server",
            "long_instruction": "Upload Files: Upload files to a place on FTP share.\nDownload Files: Download files recursively from shared FTP folders.",
            "name": "mode",
            "when": lambda results: not results["auto"],
        },
    ]

    results = prompt(questions=questions)
    # print(results)
    
    if results["auto"]:
        results["anon"] = True
        results["username"] = "anonymous"
        results["password"] = ""
        results["port"] = 21
        results["mode"] = "Download Files from FTP server"

    if results["anon"]:
        results["username"] = "anonymous"
        results["password"] = ""
    # print(results)

    # First time login.
    ftp = login(ip, results["port"], results["username"], results["password"], False)
    
    # If you want to store the shares recursively
    if results["mode"] == "Download Files from FTP server":
        if not outpath or outpath == "./":
            outpath = "./ftp"
        
        # deciding on FTP Root.
        pwd = ftp.pwd()

        # Initiate the files download process
        code = file_download(ftp, pwd, outpath, silent)
        
        # Checking for successful completion of file transfers
        while code[0] != "Files Downloaded":
            # To check if Passive or Active mode is supported.
            if code[0] in ['500 OOPS: invalid pasv_address', '500 OOPS: priv_sock_get_cmd']:
                ftp = login(ip, results["port"], results["username"], results["password"], True)
                ftp.set_pasv(False)
                code = file_download(ftp, pwd, outpath, silent)
                ftp.quit()

        console.print(f"\n[bold green][>][/bold green][green] All files are here for analysis.[/green]")

    elif results["mode"] == "Upload Files to Remote FTP server":
        # # set this option if you get passive mode error
        # ftp.set_pasv(False)
        file_upload(ftp, silent)

    # close ftp connection
    ftp.quit()
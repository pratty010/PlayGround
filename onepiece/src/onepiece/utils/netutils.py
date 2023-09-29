import re
import typer
from rich.console import Console
from onepiece.utils import cmdutils

console = Console()

reg = {
    "ipv4" : r'^(?:\d{1,3}\.){3}\d{1,3}$',
    "ipv6" : r'^(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}$',
    "dns":  r'^(?=.{1,253}$)((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$'
}

def hostf_check(host: str) -> [bool, str]:
    if re.match(reg["ipv4"], host):
        return True, "ipv4"
    elif re.match(reg["ipv6"], host):
        return True, "ipv6"
    elif re.match(reg["dns"], host):
        return True, "dns" 
    else:
        return False, "[bold red][!][/bold red][red] Wrong host address format for {} [/red][blue] format - [x.x.x.x , x.google.com, x.x.x.x.x.x[/blue]".format(host) 
    
def host_check(addr:str, ports: str, tool:str, mode: str) -> [str, str]:
    hosts = []
    if tool == "rustscan":
        hosts = list(addr.split(","))
    elif tool == "nmap":
        hosts = list(addr.split(" "))
    for host in hosts:
        check = hostf_check(host)
        if not check[0]:
            raise typer.Abort()
    if ports:
        pc = port_check(ports, tool, mode)
        if not pc:
            raise typer.Abort()
        return len(hosts), pc
    return len(hosts), None


def port_check(ports: str, tool:str, mode:str) -> str:
    if tool == "rustscan":
        if "," and "-" in ports:
            console.print("[bold yellow][!][/bold yellow][yellow] Both range and ports options not allowed.")
            return None
        elif "top" in ports:
            return "--top"
        elif "," in ports:
            return "--ports {}".format(ports)
        elif "-" in ports:
            return  "--range {}".format(ports)
        else:
            console.print("[bold red][!][/bold red][red] Wrong ports format. Refer to help for correct format use case.[/red]")
            return None
    elif tool == "nmap":
        if ports == "-p-":
            return "-p-"
        return  "-p{}".format(ports) if ports else "no-ports-set"
    else:
        console.print("[bold red][!][/bold red][red] Wrong tool name.[/red]")
        return None
    

  
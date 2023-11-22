import re
import socket
from rich.console import Console

console = Console()

reg = {
    "url"  : r'^(((ht|f)tps?):\/\/)?[\w-]+(\.[\w-]+)+([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?$',
    "dns"  : r'^(?=.{1,253}$)((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$',
}

def ipv6_check(ip: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False
    
def ipv4_check(ip: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False
    
def dns_check(url: str) -> bool:
    if re.match(reg["url"], url):
        return True
    else:
        return False
    
def url_check(url : str) -> bool:
    if re.match(reg["url"], url):
        return True
    else:
        return False

def ip_check(ip: str) -> bool:
    if ipv4_check(ip) or ipv6_check(ip) or dns_check(ip):
        return True
    return False

def port_check(ports: str, tool:str) -> str:
    if tool == "rustscan":
        if "," in ports and '-' in ports:
            console.print("\n[bold red][!][/bold red][red] Both range and ports options not allowed.[/red]\n")
            return None
        elif "1-1024" in ports:
            return "--top"
        elif "," in ports:
            return "--ports {}".format(ports)
        elif "-" in ports:
            return  "--range {}".format(ports)
        else:
            console.print("\n[bold red][!][/bold red][red] Wrong ports format. Refer to help for correct format use case.[/red]\n")
            return None
    elif tool == "nmap":
        if ports == "1-65535":
            return "-p-"
        return  "-p{}".format(ports) if ports else "no-ports-set"
    else:
        console.print("\n[bold red][!][/bold red][red] Wrong tool name.[/red]\n")
        return None


# if __name__ == "__main__":
#     main()
  
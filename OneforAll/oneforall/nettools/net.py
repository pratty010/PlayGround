import typer
from typing_extensions import Annotated
from rich.console import Console
import subprocess
from utilities import netutils, cmdutils
from nettools.mapper import nmap, rustscan


app = typer.Typer()
console = Console()

def cmd_ping_gen(host: str, count:int, timeout:int, ip6:bool) -> str:

    check = netutils.host_fcheck(host)

    if check[0]:
        if check[1] == "ipv4" and ip6:
            console.print("[bold red][!][/bold red][red] Wrong IPv6 address format.[/red][blue] format - x.x.x.x.x.x[/blue]",)
            raise typer.Abort()
        # add more cases
    else:
        # console.print(check[1])
        raise typer.Abort()
    
    cmd = "ping -6 -w {} -c {} {}".format(count, host)
    if not ip6:
        cmd = "ping -w {} -c {} {}".format(count, host)        

    return cmd

@app.command(name="auto", help="Easy way to NMAP. I will take care of it.")
def auto(
    addr: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name. Can be in format : [0.0.0.0; google.com, 127.0.0.1]", show_default=False)],
    tool: Annotated[
        str, typer.Option("--tool", "-t", help="To select the tool to use.")] = "rustscan",
    all: Annotated[
        bool, typer.Option("--all", "-A", help="If you want to run all NMAP scan options.")] = False,
    silent: Annotated[
        bool, typer.Option("--silent", "-S", help="If you don't want to see output to shell.")] = False,
    store: Annotated[
        bool, typer.Option("--store", "-s", help="To store output to the results.")] = False):
    
    if tool == "rustscan":
        rustscan.auto_scan(addr, all, silent, store)
    elif tool == "nmap":
        nmap.auto_scan(addr, all, silent, store)
    else:
        console.print("[bold red][!][/bold red][red] Wrong tool name. Refer to help for correct format use case.[/red]")
        raise typer.Abort()

@app.command(name="ping", help="ping your host")
def ping_scan(
    host: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name.", show_default=False)],
    count: Annotated[
        int, typer.Option("-c", "--count", help="Provide number of pings.", prompt="> Want to increase the count.")] = 4,
    timeout: Annotated[
        int, typer.Option("-w", "--timeout", help="Provide timeout in seconds", prompt="> Want to increase the timeout.")] = 5,
    ip6: Annotated[
        bool, typer.Option("-6", "--ipv6", help="To use IPv6 mode. Might wanna use an IPv6 address.", prompt="> Want to turn on IPv6 mode")] = False):
    
    cmd = cmd_ping_gen(host, count, ip6)
    # print(cmd)

    console.print("[bold green][>][/bold green] Starting ping scan.")
    
    cmdutils.cmd_run(host, cmd, False)

    return False

app.add_typer(rustscan.app, name="rustscan", help="NMAP on steroids.")
app.add_typer(nmap.app, name="nmap", help="friendly NMAP")


if __name__ == "__main__":
    app()
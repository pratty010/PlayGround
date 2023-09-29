import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.progress import Progress, TaskProgressColumn
import time
import os
import subprocess
from onepiece.utils import netutils, pathutils, cmdutils


app = typer.Typer()
console = Console()

tool = "rustscan"


def cmd_gen(addr: str, store:bool, grep:bool, mode:str, ports:int = None, nop:str = None) -> str:
    
    hc = netutils.host_check(addr, ports, tool, mode)
    # print(hc)

    flags = {
        "preop": hc[1] if ports else "--range 1-65535",
        "postop": "-- {} ".format(nop) if nop else "-- ",
        "file": "{}.nmap".format(mode),
    }

    if store and grep:
        console.print("[bold yellow][!][/bold yellow][yellow] Grep-able and File out save format both set. Choose either!")
        raise typer.Abort()
    elif hc[0] > 1:
        console.print("[bold yellow][!][/bold yellow][yellow] Multiple hosts provided. Only ports will be scanned. Turning of the out file format.")
        grep, store = True, False
    elif store:
        console.print("[bold green][>][/bold green][green] File store mode set. Turning of the Grep-able format.")
        path = console.input("[bold magenta][>][/bold magenta][magenta] Please provide the path to store the results.[blue] Default - current directory.[/blue]\n> [/magenta]")
        if not path:
            path = "."
        flags["postop"] = flags["postop"] + ("-oN" + " " + pathutils.cpath(path, tool, flags["file"]))
    elif grep:
        flags["preop"] =  "-g " + flags["preop"]
    else:
        pass
        # // add more cases 
    # print(flags)
    cmd  = "rustscan {} -a {} {}".format(flags["preop"], addr, flags["postop"])
    return cmd

@app.command(name="all", help="all port scan. As I said only ports.")
def port_scan(
    addr: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name. Can be in format : [0.0.0.0; google.com, 127.0.0.1]", show_default=False)],
    silent: Annotated[
        bool, typer.Option("--silent", "-S", help="If you don't want to see output to shell.")] = False,
    nop: Annotated[
        str, typer.Option("--nmap-op", "-nop", help="To add extra NMAP options to the command.")] = None,      
    grep: Annotated[
        bool, typer.Option("--grep", "-g", help="To grab only ports")] = False,
    threads: Annotated[
        int, typer.Option("--timing", "-t", help="To set the speed of the scan.[range: 1-5]")] = 3,
    store: Annotated[
        bool, typer.Option("--store", "-s", help="To store output to the results.")] = False):

    nop = "-T{} ".format(threads)

    cmd = cmd_gen(addr, store, grep, "all", None, nop)
    # print(cmd)

    console.print("[bold green][>][/bold green] Starting All Port Rust Scan as ....")
    console.print("[white on green]{}[/white on green]".format(cmd))
    
    cmdutils.cmd_run(addr, cmd, silent, tool)    


@app.command(name="basic", help="Default scan.")
def basic_scan(
    addr: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name. Can be in format : [0.0.0.0; google.com, 127.0.0.1]", show_default=False)],
    ports: Annotated[
        str, typer.Option("--port", "-p", help="Please provide ports to scan. Format : [x; x,y,z; x-y]")] = "top",
    all: Annotated[
        bool, typer.Option("--all", "-A", help="If you want to run all NMAP scan options.")] = False,
    nop: Annotated[
        str, typer.Option("--nmap-op", "-nop", help="To add extra NMAP options to the command.")] = None,
    threads: Annotated[
        int, typer.Option("--timing", "-t", help="To set the speed of the scan.[range: 1-5]")] = 4,
    silent: Annotated[
        bool, typer.Option("--silent", "-S", help="If you don't want to see output to shell.")] = False,
    grep: Annotated[
        bool, typer.Option("--grep", "-g", help="To grab only ports")] = False,
    store: Annotated[
        bool, typer.Option("--store", "-s", help="To store output to the results.")] = False):

    nop = "-T{} ".format(threads)
    nop += "-A " if all else "-sC -sV "

    cmd = cmd_gen(addr, store, grep, "main", ports, nop)
    # print(cmd)

    console.print("[bold green][>][/bold green] Starting All Port Rust Scan as ....")
    console.print("[white on green]{}[/white on green]".format(cmd))
    
    cmdutils.cmd_run(addr, cmd, silent, tool) 


@app.command(name="auto", help="Let me take over. I will do the most efficient scan.")
def auto_scan(
    addr: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name. Can be in format : [0.0.0.0; google.com, 127.0.0.1]", show_default=False)],
    all: Annotated[
        bool, typer.Option("--all", "-A", help="If you want to run all NMAP scan options.")] = False,
    silent: Annotated[
        bool, typer.Option("--silent", "-S", help="If you don't want to see output to shell.")] = False,
    store: Annotated[
        bool, typer.Option("--store", "-s", help="To store output to the results.")] = False):
    
    nop = "-T3 "
    nop += "--A " if all else "-sC -sV "
  

    cmd = cmd_gen(addr, store, False, "auto", None, nop)
    # print(cmd)

    console.print("[bold green][>][/bold green] Starting All Port Rust Scan as ....")
    console.print("[white on green]{}[/white on green]".format(cmd))
    
    cmdutils.cmd_run(addr, cmd, silent, tool)

if __name__ == "__main__":
    app()
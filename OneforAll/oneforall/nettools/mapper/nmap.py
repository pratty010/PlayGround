import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.progress import Progress, TaskProgressColumn
import time
import os
import subprocess
from utilities import netutils, pathutils, cmdutils



app = typer.Typer()
console = Console()

tool = "nmap"

def cmd_gen(addr: str, store:bool, mode:str, ports:int = None, nop:str = None) -> str:
    
    hc = netutils.host_check(addr, ports, tool, mode)
    # print(hc)

    flags = {
        "preop": "{} {} ".format(nop, hc[1]) if hc[1]!='no-ports-set' else "{} ".format(nop),
        "file": "{}.nmap".format(mode),
    }
    # print(flags)
    if store:
        console.print("[bold green][>][/bold green][green] File store mode set.")
        path = console.input("[bold magenta][>][/bold magenta][magenta] Please provide the path to store the results.[blue] Default - current directory.[/blue]\n> [/magenta]")
        if not path:
            path = "."
        flags["preop"] = flags["preop"] + ("-oN" + " " + pathutils.cpath(path, tool, flags["file"]))
    else:
        pass
        # // add more cases 
    # print(flags)
    
    cmd  = "sudo nmap {} {}".format(flags["preop"], addr)
    return cmd


@app.command(name="all", help="all port scan. As I said only ports.")
def port_scan(
    addr: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name. Can be in format : [0.0.0.0; google.com, 127.0.0.1]", show_default=False)],
    silent: Annotated[
        bool, typer.Option("--silent", "-S", help="If you don't want to see output to shell.")] = False,
    add_flags: Annotated[
        str, typer.Option("--nmap-op", "-nop", help="To add extra NMAP options to the command.")] = None,      
    threads: Annotated[
        int, typer.Option("--timing", "-t", help="To set the speed of the scan.[range: 1-5]")] = 3,
    store: Annotated[
        bool, typer.Option("--store", "-s", help="To store output to the results.")] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="To store output to the results.")] = False):
    

    if add_flags:
        add_flags = "-vvv -T{} {} ".format(threads, add_flags) if verbose else "-v -T{} {} ".format(threads, add_flags)
    else:
        add_flags = "-vvv -T{} ".format(threads) if verbose else "-v -T{} ".format(threads)

    cmd = cmd_gen(addr, store, "all", "-p-", add_flags)
    print(cmd)

    console.print("[bold green][>][/bold green] Starting All Port Rust Scan as ....")
    console.print("[white on green]{}[/white on green]".format(cmd))
    cmdutils.cmd_run(addr, cmd, silent, tool)    
    

@app.command(name="basic", help="Default scan.")
def basic_scan(
    addr: Annotated[
        str, typer.Argument(..., help="provide host IP or DNS name. Can be in format : [0.0.0.0; google.com, 127.0.0.1]", show_default=False)],
    ports: Annotated[
        str, typer.Option("--port", "-p", help="Please provide ports to scan. Format : [x; x,y,z; x-y]")] = "1-1024",
    all: Annotated[
        bool, typer.Option("--all", "-A", help="If you want to run all NMAP scan options.")] = False,
    add_flags: Annotated[
        str, typer.Option("--nmap-op", "-nop", help="To add extra NMAP options to the command.")] = None,
    threads: Annotated[
        int, typer.Option("--timing", "-sp", help="To set the speed of the scan.[range: 1-5]")] = 4,
    silent: Annotated[
        bool, typer.Option("--silent", "-S", help="If you don't want to see output to shell.")] = False,
    store: Annotated[
        bool, typer.Option("--store", "-s", help="To store output to the results.")] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="To store output to the results.")] = False):

    if add_flags:
        add_flags = "-vvv -T{} {} ".format(threads, add_flags) if verbose else "-v -T{} {} ".format(threads, add_flags)
    else:
        add_flags = "-vvv -T{} ".format(threads) if verbose else "-v -T{} ".format(threads)
    
    add_flags += "-A " if all else "-sC -sV "

    cmd = cmd_gen(addr, store, "main", ports, add_flags)
    print(cmd)

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
    
    add_flags = "-T3 "
    add_flags += "--A " if all else "-sC -sV "

    cmd = cmd_gen(addr, store, "auto", "-p-",  add_flags)
    print(cmd)

    console.print("[bold green][>][/bold green] Starting All Port Rust Scan as ....")
    console.print("[white on green]{}[/white on green]".format(cmd))
    cmdutils.cmd_run(addr, cmd, silent, tool)  

if __name__ == "__main__":
    app()
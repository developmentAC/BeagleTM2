#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import random, typer, os
from beagletm2 import parser as p
from beagletm2 import dbMaker
from pathlib import Path


DATE = "22 July 2023"
VERSION = "0.18.0"
AUTHOR = "Oliver Bonham-Carter"
AUTHORMAIL = "obonhamcarter@allegheny.edu"


banner0_str = """
  ██████╗ ███████╗ █████╗  ██████╗ ██╗     ███████╗████████╗███╗   ███╗
  ██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝╚══██╔══╝████╗ ████║
  ██████╔╝█████╗  ███████║██║  ███╗██║     █████╗     ██║   ██╔████╔██║
  ██╔══██╗██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝     ██║   ██║╚██╔╝██║
  ██████╔╝███████╗██║  ██║╚██████╔╝███████╗███████╗   ██║   ██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝     ╚═╝
"""
# banner ref: https://manytools.org/hacker-tools/ascii-banner/

colorWords_list = [
    "bold bright_black",
    "bold bright_red",
    "bold bright_green",
    "bold bright_yellow",
    "bold bright_blue",
    "bold bright_magenta",
    "bold bright_cyan",
    "bold bright_white",
]


# create a Typer object to support the command-line interface
cli = typer.Typer()

console = Console()


@cli.command()
def main(
    client: str = "",
    bighelp: bool = False,
    data_file: Path = typer.Option(None),
    make_db: bool = True,
    abs_only: bool = True,  # scan only the abstracts?
    save_less: bool = True,  # save first 100 chars of the abstracts in the data?
) -> None:
    """Driver of the program. The clientType allows the user to select parser version or the parser."""
    console = Console()
    # console.print(f"\t [bold cyan] Client type is <<{client}>>")

    if client.lower() == "browser":
        console.print("\t browser:\n\t Running Command\n\t :smiley:")
        os.system("poetry run streamlit run beagletm2/beagleTM2_browser2.py")

    elif client.lower() == "parser":
        console.print("\t :sparkles: Parser selected ...")
        # check for the key word file
        if data_file is None:
            console.print("\t :scream: No data file specified!")
            raise typer.Abort()
        # --> the file was specified and it is valid so we should read and check it
        if data_file.is_file() == False:
            console.print(
                f"\t [bold red]Oh :poop:! Error with data-file loading. Exiting..."
            )
            exit()  # :thumbs_down:

        csv_file = p.main(
            data_file, abs_only, make_db, save_less
        )  # pass word list and run parser, pass abstract or full journal scanning option

        # make a SQL DB file from the output?
        if make_db == True:
            dbMaker.main(csv_file)

    elif bighelp:
        bigHelp()

        # console.print(f"\t :skull:[bold red] Enter command")


# end of main()


def bigHelp():
    """Helper function"""

    # console.print(f"[bold green]{banner0_str}")
    console.print(banner0_str, style=random.choice(colorWords_list))

    h_str = "   " + DATE + " | version: " + VERSION + " |" + AUTHOR + " | " + AUTHORMAIL
    console.print(f"[bold green] {len(h_str) * '-'}")
    console.print(f"[bold yellow]{h_str}")
    console.print(f"[bold green] {len(h_str) * '-'}")

    console.print("\n\t[bold yellow] Client: Parser or Browser")

    console.print(
        "\t [bold blue] * Parser: App for searching for keywords in articles. Note: you must include a keyword file."
    )
    console.print("\t [bold blue] * Browser: App to visualize data after parsing job.")

    console.print(f"\n\t [bold blue] Execute, process abstracts only")
    console.print(
        f"\t :smiley: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --abs-only"
    )

    console.print(
        f"\n\t [bold blue] Execute, process abstracts only and create db from results."
    )
    console.print(
        f"\t :smiley: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --make-db --abs-only"
    )

    console.print(f"\n\t [bold blue] Execute, process whole articles.")
    console.print(
        f"\t :smiley: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --no-abs-only"
    )

    console.print(
        f"\n\t [bold blue] Execute, process whole articles and create db from results of smaller size."
    )
    console.print(
        f"\t :smiley: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --make-db --no-abs-only --save-less"
    )


# end of bigHelp()

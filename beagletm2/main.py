#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import random, typer, os
from beagletm2 import parser as p
from beagletm2 import networkBuilder as nb
from beagletm2 import queryData as qd
from beagletm2 import dbOps  # database operations

from pathlib import Path


DATE = "2 Dec 2024"
VERSION = "v1.0.0"
AUTHOR = "Oliver Bonham-Carter"
AUTHORMAIL = "obonhamcarter@allegheny.edu"


banner0_str = """
  ██████╗ ███████╗ █████╗  ██████╗ ██╗     ███████╗████████╗███╗   ███╗
  ██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝╚══██╔══╝████╗ ████║
  ██████╔╝█████╗  ███████║██║  ███╗██║     █████╗     ██║   ██╔████╔██║
  ██╔══██╗██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝     ██║   ██║╚██╔╝██║
  ██████╔╝███████╗██║  ██║╚██████╔╝███████╗███████╗   ██║   ██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝     ╚═╝ 2
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
    makePlots: bool = True,
    bighelp: bool = False,
    data_file: Path = typer.Option(None),  # incoming data file for different purposes
    make_db: bool = True,
    abs_only: bool = True,  # scan only the abstracts?
    save_less: bool = True,  # save first 100 chars of the abstracts in the data?
    # networkBuilder: str = "", # a command line driven network maker similar to the one in the streamlit app
    words_to_query_file: Path = typer.Option(
        None
    ),  # list of words from which to build a network
) -> None:
    """Driver of the program. The clientType allows the user to select parser version or the parser."""
    console = Console()
    # console.print(f"\t [bold cyan] Client type is <<{client}>>")

    #################
    # Query data
    #################

    if client.lower() == "query":
        console.print("\t[bold cyan] Query: \n\t Preparing to complete query. ")
        console.print(f"\t[bold yellow] Data File: {data_file}")
        if data_file is None:
            console.print("\t :scream: No data file specified!")
            raise typer.Abort()

        console.print(f"\t[bold yellow] File of words to query: {words_to_query_file}")
        if words_to_query_file is None:
            console.print("\t :scream: No word file specified!")
            raise typer.Abort()

        # --> the file was specified and it is valid so we should read and check it
        if data_file.is_file() == False or words_to_query_file.is_file() == False:
            console.print(
                f"\t [bold red]Oh :poop:! Error with data-file loading. Exiting..."
            )
            exit()  # :thumbs_down:
        qd.main(
            data_file, words_to_query_file, makePlots
        )  # call the stand-alone network builder

    #################
    # NetworkBuilder
    #################

    if client.lower() == "builder":
        console.print(
            "\t[bold cyan] NetworkBuilder:\n\t Preparing stand-alone network building app"
        )

        if data_file is None:
            console.print("\t :scream: No data file specified!")
            raise typer.Abort()
        # --> the file was specified and it is valid so we should read and check it
        if data_file.is_file() == False:
            console.print(
                f"\t [bold red]Oh :poop:! Error with data-file loading. Exiting..."
            )
            exit()  # :thumbs_down:

        nb.main(data_file)  # call the stand-alone network builder

    ##########
    # Browser
    ##########

    elif client.lower() == "browser":
        console.print("\t browser:\n\t Preparing browser app\n\t :smiley:")
        os.system(" pwd > mypath.txt") # 28Feb2024
        os.system("poetry run streamlit run beagletm2/beagleTM2_browser.py")
        exit()

    elif client.lower() == "nbrowser":
        console.print("\t :thumbsup: [bold cyan]Preparing new browser app ...")
        # Change 200MB to larger size in parameter below as necessary.
        console.print(
            f"\t [bold green]Command: [bold yellow]poetry run streamlit run beagletm2/nbrowser.py -- server.maxUploadSize 200"
        )
        os.system(
            "poetry run streamlit run beagletm2/nbrowser.py -- server.maxUploadSize 200"
        )

    #########
    # Parser
    #########

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

        # csv_file is directory and filename.csv
        csv_file, wordCsv_file = p.main(
            data_file, abs_only, make_db, save_less  # csv_file is filename
        )  # pass word list and run parser, pass abstract or full journal scanning option

        # make a SQL DB file from the output?
        if make_db == True:
            dbOps.main(csv_file, wordCsv_file)
        exit()

    elif bighelp:
        bigHelp()
        exit()
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
        "\t *[bold yellow] Parser:[bold blue] App for searching for keywords in articles. Note: you must include a keyword file."
    )
    console.print("\t *[bold yellow] Browser: [bold blue] App to visualize data after parsing job.")

    console.print(f"\n\t [bold blue] Execute, process abstracts only")
    console.print(
        f"\t :dog: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --abs-only"
    )

    console.print(
        f"\n\t [bold blue] Execute, process abstracts only and create db from results."
    )
    console.print(
        f"\t :dog: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --make-db --abs-only"
    )

    console.print(f"\n\t [bold blue] Execute, process whole articles.")
    console.print(
        f"\t :dog: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --no-abs-only"
    )

    console.print(
        f"\n\t [bold blue] Execute, process whole articles and create db from results of smaller size."
    )
    console.print(
        f"\t :dog: [bold cyan] poetry run beagletm2 --client parser --data-file kw_short.md --make-db --no-abs-only --save-less"
    )
    console.print(f"\n\t [bold blue] Execute the former browser app")
    console.print(f"\t :poodle: [bold cyan] poetry run beagletm2 --client browser")

    console.print(f"\n\t [bold blue] Execute the new browser app")
    console.print(f"\t :poodle: [bold cyan] poetry run beagletm2 --client nbrowser")

    console.print(f"\n\t [bold blue] Network builder -- builds maps without Streamlit")
    console.print(
        f"\t [bold blue] Build plots: Note the input csv files from this are the query files which are outputted\n\t  from the Streamlit app. This option produces files containing nodes,\n\t  analysis and figures."
    )
    console.print(
        f"\t :wolf: [bold cyan] poetry run beagletm2  --client builder --data-file pmidsRefs_observed_patterns.csv"
    )
    console.print(
        f"\n\t [bold blue] Query keywords in database -- builds the csv files used to produce nodes\n\t  and plots using the builder option."
    )

    console.print(
        f"\t :smiley: [bold cyan] poetry run beagletm2  --client query --data-file ./0_out/kw_short_analysis_out_save-less.sqlite3 --words-to-query-file wordsToQuery.md --makeplots"
    )
    console.print("\t :hand: [bold yellow] Note: Each command from above is to be entered on one line.[/bold yellow]")

# end of bigHelp()

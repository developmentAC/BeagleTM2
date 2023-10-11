import typer
from rich.console import Console
from beagletm2 import fileOps
from beagletm2 import dbOps  # database operations
import pandas as pd


# import networkx as nx
# import pandas as pd
# import matplotlib.pyplot as plt


# globals
dir_str = "0_out/"
plot_str = "plots/"
nodesDir_str = "nodes/"


cli = typer.Typer()
console = Console()

# Note the datafile input here is a listing of keywords -- each word on own line.

def main(dataFile_str: str, wordsToQuery_str : str, makePlots_bool: bool) -> None:
    """Main driver function to query main database to create the csv output files which are used to build networks without having to use Streamlit. Note the data_file is a sqlite3 database file and the file wordsToQuery_str is a file of words (going line by line) to be queried to the database. """

    console.print(f"""
                  \t[bold green] Welcome! This is the CLI for querying inputted database files
                   to create the csv output files. These CSV files may be used with the builder 
                   option to build node and plot files without using the Streamlit app.
                  """)

    # console.print(f"\t[bold blue] Data File: {dataFile_str}")
    # console.print(f"\t[bold blue] File of words to query: {wordsToQuery_str}")
    

    wordsToQuery_str = open(wordsToQuery_str,"r").readlines()
    wordsToQuery_str = fileOps.listCleaner(wordsToQuery_str)

    # console.print(f"[bold yellow] word list is :{wordsToQuery_str}")
    dbOps.CLI_selectAllKwsInArticles(wordsToQuery_str, dataFile_str, makePlots_bool) # string of words, datafilename, bool to produce plots: true or false

    # end of main()



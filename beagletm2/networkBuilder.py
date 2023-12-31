import typer
from rich.console import Console
from beagletm2 import fileOps


import networkx

# import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# globals
dir_str = "0_out/"
plot_str = "plots/"
nodesDir_str = "nodes/"


cli = typer.Typer()
console = Console()


def main(csvFilename_str: str) -> None:
    """Main driver function to build networks from output files without having to use streamlit"""
    # console.print(f"\t[bold green] Welcome! This is the CLI for building network models without the Streamlit app.")
    makeNetworkxPlot_nonSTREAMLIT(csvFilename_str)

    # end of main()


def cleanFilename(in_str):
    """Remove all path information but the filename itself."""
    in_str = in_str[::-1]  # reverse
    in_str = in_str[
        : in_str.find("/")
    ]  # look first for path forward line (which is last in fill path+file)
    in_str = in_str[::-1]
    return in_str
    # end of cleanFilename()


def makeNetworkxPlot_nonSTREAMLIT(filename_str):
    # This function is almost the same one in plotOps.py. Here we do not use Streamlit as this
    # part of the software is to be used from the command.
    """Networkx network plotter function. filename_str is the csvfile"""
    # console.print(f"\t[bold cyan] Creating a Networkx plot for file :{filename_str}")

    thisFileName_str = str(filename_str)

    thisFileName_str = cleanFilename(thisFileName_str)

    got_df = pd.read_csv(filename_str)
    # print(got_df)

    G = networkx.from_pandas_edgelist(got_df, "Pmid", "Reference", "Weight")

    fileOps.checkDataDir(
        dir_str + plot_str
    )  # does the data directory exist? If not make it exist.

    # gotFilename_str = dir_str + plot_str + "cli_GOT-network.graphml"
    # networkx.write_graphml(G, gotFilename_str)
    networkx.draw(G)

    ### degree calculations
    networkx.degree(G)

    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name="degree", values=degrees)

    degree_df = pd.DataFrame(G.nodes(data="degree"), columns=["node", "degree"])
    degree_df = degree_df.sort_values(by="degree", ascending=False)

    # show full network

    # draw plot
    plt.figure(figsize=(8, 8))
    # pos = networkx.shell_layout(G)
    pos = networkx.circular_layout(G)
    networkx.draw(
        G,
        label="labelGoesHere",
        with_labels=False,
        node_color="#1f78b4",  # dark sky blue
        width=0.5,  # edges
        font_size=8,
        node_shape="8",
        edge_color="black",
        alpha=0.7,
        pos=pos,
    )

    fileOps.checkDataDir(
        dir_str + nodesDir_str
    )  # does the data directory exist? If not make it exist.

    filename_str = thisFileName_str.replace(
        dir_str, ""
    )  # cleaning filename before adding new dir
    figFilename_str = (
        dir_str + plot_str + thisFileName_str[: thisFileName_str.find(".csv")] + ".png"
    )
    plt.savefig(figFilename_str)
    console.print(f"[bold green]\n\t Saved figfile : [bold yellow]{figFilename_str} ")

    highDegreeNodes_list = []  # used for plotting
    highDegreeNodes_str = "node, degree\n"  # save the degrees as csv format
    for index, row in degree_df.iterrows():
        if row["degree"] > 3: # Focus on all nodes having at least 3 (here, for example) degrees
            highDegreeNodes_list.append(row["node"])
            highDegreeNodes_str = (
                highDegreeNodes_str + str(row["node"]) + "," + str(row["degree"]) + "\n"
            )
    fileOps.checkDataDir(
        dir_str + nodesDir_str
    )  # does the data directory exist? If not make it exist.

    filenameNodesDegrees_str = nodesDir_str + "nodeDegs_" + filename_str

    fileOps.saveCSV_cli(highDegreeNodes_str, filenameNodesDegrees_str)

    console.print(
        f"[bold green]\t Saved nodes file : [bold yellow]{filenameNodesDegrees_str}"
    )
    # console.print(f"[bold green]\t NODES : [bold yellow]{highDegreeNodes_str}")

    # draw plot
    plt.figure(figsize=(8, 8))
    # pos = networkx.shell_layout(G)
    pos = networkx.circular_layout(G)
    networkx.draw(
        G,
        nodelist=highDegreeNodes_list,
        label="labelGoesHere",
        with_labels=False,
        node_color="#1f78b4",  # dark sky blue
        width=0.5,  # edges
        font_size=8,
        node_shape="8",
        edge_color="black",
        alpha=0.7,
        pos=pos,
    )

    # node_color='skyblue'

    filename_str = filename_str.replace(
        dir_str, ""
    )  # cleaning filename before adding new dir
    # node_color='skyblue'
    figFilename_str = (
        dir_str
        + plot_str
        + filename_str[: filename_str.find(".csv")]
        + "_highDegree_allKws.png"
    )
    plt.savefig(figFilename_str)
    console.print(f"[bold green]\t Saved figfile : [bold yellow]{figFilename_str} ")

    # end of makeNetworkxPlot()

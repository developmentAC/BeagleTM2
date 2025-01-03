import networkx
import streamlit as st
import networkx
import pandas as pd
import matplotlib.pyplot as plt

# from bokeh.models import (BoxSelectTool, Circle, HoverTool, MultiLine,
#                           NodesAndLinkedEdges, Plot, Range1d, TapTool)
# from bokeh.palettes import Spectral4
# from bokeh.plotting import from_networkx, show

from beagletm2 import dbOps
from beagletm2 import fileOps


# globals
dir_str = "0_out/"
plot_str = "plots/"
nodesDir_str = "nodes/"


def makeNetworkxPlot(filename_str, header_list):
    """networkx network plotter function"""
    st.write(f"Creating a Networkx plot for file :{filename_str}")

    # st.write(f"HEADER LIST :{header_list}")
    # HEADER LIST :['Pmid', 'Reference', 'Weight17183658', '14242501', '117183658', '10916682', '117183658', '8807088', '117183658', '12023819', '117183658', '8571957', '117183658', '
              
    got_df = pd.read_csv(filename_str)
    # print(got_df)

    G = networkx.from_pandas_edgelist(got_df, "Pmid", "Reference", "Weight")

    fileOps.checkDataDir(
        dir_str + plot_str
    )  # does the data directory exist? If not make it exist.

    # gotFilename_str = dir_str + plot_str + "GOT-network.graphml"
    # networkx.write_graphml(G, gotFilename_str)
    networkx.draw(G)

    ### degree calculations
    networkx.degree(G)

    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name="degree", values=degrees)

    degree_df = pd.DataFrame(G.nodes(data="degree"), columns=["node", "degree"])
    degree_df = degree_df.sort_values(by="degree", ascending=False)
    # st.text(f"{degree_df}")

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

    filename_str = filename_str.replace(
        dir_str, ""
    )  # cleaning filename before adding new dir
    # node_color='skyblue'
    figFilename_str = (
        dir_str + plot_str + filename_str[: filename_str.find(".csv")] + "_allKws.png"
    )
    # figFilename_str =   filename_str[:filename_str.find(".csv")] + ".png"
    plt.savefig(figFilename_str)

    openPage(figFilename_str)

    # get nodes for which degree greater than a value.

    highDegreeNodes_list = []  # used for plotting
    highDegreeNodes_str = "node, degree\n"  # save the degrees as csv format
    for index, row in degree_df.iterrows():
        if row["degree"] > 3:
            highDegreeNodes_list.append(row["node"])
            highDegreeNodes_str = (
                highDegreeNodes_str + str(row["node"]) + "," + str(row["degree"]) + "\n"
            )

    filenameNodesDegrees_str = nodesDir_str + "nodeDegs_" + filename_str
    st.write(filenameNodesDegrees_str)
    fileOps.checkDataDir(
        dir_str + nodesDir_str
    )  # does the data directory exist? If not make it exist.

    fileOps.saveCSV(highDegreeNodes_str, filenameNodesDegrees_str)

    whatIsThis_str = "Node Degrees"
    dbOps.prettyTabler(degree_df, whatIsThis_str)

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

    openPage(figFilename_str)

    # end of makeNetworkxPlot()


def openPage(fname):
    """function to open a a web page in a browser"""
    import webbrowser
    from pathlib import Path

    myPath_posixPath = Path.cwd()
    # myUrl_str = "file://" + str(myPath_posixPath) + "/" + dir_str + fname
    myUrl_str = "file://" + str(myPath_posixPath) + "/" + fname
    st.code(myUrl_str, language="bash")
    webbrowser.open(myUrl_str, new=0, autoraise=True)


# end of openPage()


# junk bin ####################################


def old_getNodeDegrees(
    G,
):  # note: I had some trouble passing G to this function from another. It was easier to paste this code into the makeNetWorkxPlot().
    """function to calculate the degrees of nodes."""

    networkx.degree(G)

    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name="degree", values=degrees)

    degree_df = pd.DataFrame(G.nodes(data="degree"), columns=["node", "degree"])
    degree_df = degree_df.sort_values(by="degree", ascending=False)
    st.text(f"degree_df --> {degree_df}")


# end of old_getNodeDegrees()


def makePlot(a_list, b, c):  # pmids_list,"Abstract","Pmid"
    """Bokah function to prepare network plots from inputted data"""

    G = networkx.karate_club_graph()

    plot = Plot(
        width=400, height=400, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1)
    )
    plot.title.text = "Graph Interaction Demonstration"

    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(G, networkx.circular_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(
        size=15, fill_color=Spectral4[2]
    )
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="#CCCCCC", line_alpha=0.8, line_width=5
    )
    graph_renderer.edge_renderer.selection_glyph = MultiLine(
        line_color=Spectral4[2], line_width=5
    )
    graph_renderer.edge_renderer.hover_glyph = MultiLine(
        line_color=Spectral4[1], line_width=5
    )

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    show(plot)

    # end of makePlot()


def bk_makePlot(a_list, b, c):  # pmids_list,"Abstract","Pmid"
    """Bokah function to prepare network plots from inputted data"""

    G = networkx.karate_club_graph()

    plot = Plot(
        width=400, height=400, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1)
    )
    plot.title.text = "Graph Interaction Demonstration"

    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(G, networkx.circular_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(
        size=15, fill_color=Spectral4[2]
    )
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(
        line_color="#CCCCCC", line_alpha=0.8, line_width=5
    )
    graph_renderer.edge_renderer.selection_glyph = MultiLine(
        line_color=Spectral4[2], line_width=5
    )
    graph_renderer.edge_renderer.hover_glyph = MultiLine(
        line_color=Spectral4[1], line_width=5
    )

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    show(plot)

    # end of bk_makePlot()

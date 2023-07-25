import networkx as nx
import streamlit as st
import networkx
import pandas as pd
import matplotlib.pyplot as plt

from bokeh.models import (BoxSelectTool, Circle, HoverTool, MultiLine,
                          NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, show


# globals
dir_str = "0_out/"



def makeNetworkxPlot(filename_str):
    """networkx network plotter function"""
    st.write(f"Make a networkx plot for file :{filename_str}")

    # filename_str = "0_out/got-edges.csv"
    got_df = pd.read_csv(filename_str)
    print(got_df)

    G = networkx.from_pandas_edgelist(got_df, 'Pmid', 'Reference', 'Weight')

    # G = networkx.read_edgelist(got_df, delimiter=",",nodetype=int)# data=[("Pmid", "Reference")])
    # G = networkx.from_pandas_edgelist(got_df)#, 'Pmid', 'Reference')

    gotFilename_str = dir_str + "GOT-network.graphml"
    # networkx.write_graphml(G, gotFilename_str)
    networkx.draw(G)

    plt.figure(figsize=(8,8))
    networkx.draw(G, with_labels=True, node_color='skyblue', width=.3, font_size=8)
    plt.show()
    plt.savefig("0_out/mygraph.png")
    st.write("plot created?")
    # end of makeNetworkxPlot()


def makePlot(a_list, b, c): # pmids_list,"Abstract","Pmid"
    """ Bokah function to prepare network plots from inputted data"""

    G = nx.karate_club_graph()

    plot = Plot(width=400, height=400,
                x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
    plot.title.text = "Graph Interaction Demonstration"

    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0,0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    show(plot)

    # end of makePlot()



def bk_makePlot(a_list, b, c): # pmids_list,"Abstract","Pmid"
    """ Bokah function to prepare network plots from inputted data"""

    G = nx.karate_club_graph()

    plot = Plot(width=400, height=400,
                x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
    plot.title.text = "Graph Interaction Demonstration"

    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0,0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    show(plot)

    # end of bk_makePlot()
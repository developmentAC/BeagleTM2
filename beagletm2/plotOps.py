import networkx as nx
import streamlit as st
import networkx
import pandas as pd
import matplotlib.pyplot as plt

from bokeh.models import (BoxSelectTool, Circle, HoverTool, MultiLine,
                          NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, show

from beagletm2 import dbOps


# globals
dir_str = "0_out/"


def makeNetworkxPlot(filename_str, header_list):
    """networkx network plotter function"""
    st.write(f"Make a networkx plot for file :{filename_str}")


    got_df = pd.read_csv(filename_str)
    # print(got_df)


    G = networkx.from_pandas_edgelist(got_df, 'Pmid', 'Reference', 'Weight')

    gotFilename_str = dir_str + "GOT-network.graphml"
    # networkx.write_graphml(G, gotFilename_str)
    networkx.draw(G)



### degree calculations
    networkx.degree(G)

    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)

    degree_df = pd.DataFrame(G.nodes(data='degree'), columns=['node', 'degree'])
    degree_df = degree_df.sort_values(by='degree', ascending=False)
    # st.text(f"degree_df --> {degree_df}")

# get nodes for which degree greater than 2.
    highDegreeNodes_list=[]
    lowDegreeNodes_list=[]
    # print(degree_df)
    for i in range(len(degree_df)):
        print(f"# {degree_df[0]}, {degree_df[1]}")



    whatIsThis_str = "Node Degrees"
    dbOps.prettyTabler(degree_df, whatIsThis_str)





# draw plot
    plt.figure(figsize=(8,8))
    # pos = nx.shell_layout(G)
    pos = nx.circular_layout(G)
    networkx.draw(G,
                  label = "haha", 
                  with_labels=False, 
                  node_color='#1f78b4', # dark sky blue
                  width=0.5, # edges
                  font_size=8, 
                  node_shape ="8", 
                  edge_color = "black", 
                  alpha = 0.7, 
                  pos = pos
                  )

    # node_color='skyblue'

    figFilename_str =   filename_str[:filename_str.find(".csv")] + ".png"
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
    st.code(myUrl_str, language = 'bash')
    webbrowser.open(myUrl_str, new=0, autoraise=True)


# end of openPage()





# junk bin ####################################

def old_getNodeDegrees(G): # note: I had some trouble passing G to this function from another. It was easier to paste this code into the makeNetWorkxPlot(). 
    """function to calculate the degrees of nodes."""

    networkx.degree(G)

    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)

    degree_df = pd.DataFrame(G.nodes(data='degree'), columns=['node', 'degree'])
    degree_df = degree_df.sort_values(by='degree', ascending=False)
    st.text(f"degree_df --> {degree_df}")

# end of old_getNodeDegrees()


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
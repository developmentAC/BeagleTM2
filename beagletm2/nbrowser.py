# Load libraries
import streamlit as st
import pandas as pd
from beagletm2 import plotOps
from beagletm2 import dbOps
from beagletm2 import fileOps  # for grabFile()


# DB Mgmt
import sqlite3


# global variables
DATADIR = "0_out/"

banner0_str = """
  ██████╗ ███████╗ █████╗  ██████╗ ██╗     ███████╗████████╗███╗   ███╗
  ██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝╚══██╔══╝████╗ ████║
  ██████╔╝█████╗  ███████║██║  ███╗██║     █████╗     ██║   ██╔████╔██║
  ██╔══██╗██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝     ██║   ██║╚██╔╝██║
  ██████╔╝███████╗██║  ██║╚██████╔╝███████╗███████╗   ██║   ██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝     ╚═╝ 2
"""
# banner ref: https://manytools.org/hacker-tools/ascii-banner/


from io import StringIO


def main() -> None:
    """Driver function of the network browser."""
    st.title("BeagleTM2 Network Browser")
    # st.subheader("SQL Database Managment")
    # st.text(banner0_str)

    # myConn = None # define variable for conn from database which is given later

    ### upload field with button
    st.sidebar.text("Drag and Drop in a file to provide path information.")
    # f = st.sidebar.file_uploader("Upload a file", accept_multiple_files=False,type=(["sqlite3","csv","md"]))

    dataFile = fileOps.grabFile()

    # st.subheader("Database Output")

    # # Columns/Layout
    # myCol1, myCol2 = st.columns(2)

    if dataFile is not None:
        # We must add path information to filename (path_in), file_upload does not add this info!!!!
        c = dbOps.loadDbGetConn(dataFile)
        # st.subheader("File:")
        st.success(f"{dataFile}")

        # menu system
        doThis_sb = None
        menu_list = [
            "Show_Tables",
            "Find_articles_containing_ALL_selected_keywords",
            # "Balloons",
            # "Snow",
        ]
        doThis_sb = st.sidebar.selectbox("What are we doing with this data?", menu_list)

        if (
            doThis_sb == menu_list[0]
        ):  # putting menu options in this format makes it easier to customize menu option language
            st.title("Showing tables of database ...")
            # st.header(f"{menu_list[0]}")

            st.text(f"Option: {menu_list[0]}")
            result_str = dbOps.getTablesListing(c)

        if doThis_sb == menu_list[1]:
            st.text(f"Option: {menu_list[1]}")
            result_str = dbOps.selectAllKwsInArticles(c)

        # if doThis_sb == menu_list[2]:
        #     st.text(f"Option: {menu_list[2]}")
        #     st.balloons()

        # if doThis_sb == menu_list[3]:
        #     st.text(f"Option: {menu_list[3]}")
        #     st.snow()

    else:
        path_in = None

    # end of main()


if __name__ == "__main__":
    main()

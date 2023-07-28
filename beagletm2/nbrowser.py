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
    st.text(banner0_str)

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
            "Balloons",
            "Snow",
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

        if doThis_sb == menu_list[2]:
            st.text(f"Option: {menu_list[2]}")
            st.balloons()

        if doThis_sb == menu_list[3]:
            st.text(f"Option: {menu_list[3]}")
            st.snow()
    else:
        path_in = None

    # end of main()


def getTablesListing(myConn) -> None:
    """function to show tables on new page"""
    st.title("Tables")

    with st.form(key="query_form"):
        myCommand_str = st.text_area("SQL Code Here")
        submit_button = st.form_submit_button("Execute")

        if submit_button:
            st.info("Query Submitted")
            st.code(myCommand_str)

            # Results
            query_results = sql_executor(myConn, myCommand_str)
            with st.expander("Results"):
                st.write(query_results)

            with st.expander("Pretty Table"):
                query_df = pd.DataFrame(query_results)
                st.dataframe(query_df)


def getTablesListing(myConn):
    myQuery_str = "SELECT name FROM sqlite_master WHERE type='table';"
    return sql_executor(myConn, myQuery_str)

    # end of getTablesListing()


def old_main():
    st.title("BeagleTM2 Network Browser")

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Database Output")

        # Columns/Layout
        myCol1, myCol2 = st.columns(2)

        # Results Layouts
        with myCol1:
            with st.form(key="query_form"):
                myCommand_str = st.text_area("SQL Code Here")
                submit_button = st.form_submit_button("Execute")

                # commit_code = st.form_submit_button("Commit Changes")

                # st.balloons() # show some balloons!
                # st.snow()
                # st.success("oh yeah")

                st.write("Command to list tables.")
                copyThis_tmp = "SELECT name FROM sqlite_master WHERE type='table';"
                st.code(copyThis_tmp, language="bash")
            # not all tables are displayed with this code. Read all about it at the below reference.
            # ref: https://database.guide/2-ways-to-list-tables-in-sqlite-database/

            if submit_button:
                st.info("Query Submitted")
                st.code(myCommand_str)

                # Results
                query_results = sql_executor(myCommand_str)
                with st.expander("Results"):
                    st.write(query_results)

                with st.expander("Pretty Table"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

        with myCol2:
            with st.form(key="row1"):
                st.write("Query")

                myTable_str = st.text_input("Enter Table name")
                q_attribute1_str = st.text_input("Enter 1st attribute name")
                q_attribute2_str = st.text_input("Enter 2nd attribute name")
                myQueryButton = st.form_submit_button("Build Query String")

                if myQueryButton:  # if clicked
                    myQuery_str = f"SELECT {q_attribute1_str},{q_attribute2_str} FROM {myTable_str}"
                    st.code(myQuery_str, language="bash")

    else:
        st.subheader("About")
        st.write("Put about information here!! ")
        # end of old_main()


if __name__ == "__main__":
    main()

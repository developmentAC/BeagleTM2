# Import required libraries
import sqlite3, typer
import pandas as pd
from beagletm2 import fileOps
import streamlit as st

from rich.console import Console

# globals
# dir_str = "0_out/"
dir_str = fileOps.dir_str

# cli = typer.Typer()
console = Console()


def main(csv_file:str, wordCsv_file:str) -> None:
    """driver function"""
    dbfname_str = csv_file.replace(".csv", ".sqlite3") #database filename

    tableName_str = "main"
    builder(dbfname_str, csv_file, tableName_str) # build the first database

    tableName_str = "counts"
    builder(dbfname_str, wordCsv_file, tableName_str) # build the first database

    # end of main()


def builder(dbfname_str: str, csvFile_str:str, tableName_str : str) -> None:

    """driver function"""
    # console.print(f"\n\t :sparkles:[bold cyan] Making a SQL database from results.")

    console.print(
        f"\n\t :package:[bold green] Making a SQL database from cvs file :{dbfname_str}"
    )

    # fname = input("Enter name of the analysis file: ")

    fileOps.checkDataDir(
        dir_str
    )  # does the data directory exist? If not make it exist.

    console.print(f"\t [bold purple] --> Opening csv file: [bold cyan]{dbfname_str}")

    # Connect to SQLite database
    conn = sqlite3.connect(dbfname_str)

    # Load CSV data into Pandas DataFrame
    student_data = pd.read_csv(csvFile_str)

    # Write the data to a sqlite table
    student_data.to_sql(tableName_str, conn, if_exists="replace", index=False)

    # Create a cursor object
    cur = conn.cursor()

    console.print(f"\t [bold purple] --> Finished building sqlite3 database")

    conn.close()

    console.print(f"\t :Rocket:[bold yellow] DB File saved to: {dbfname_str}")


# Code for querying

# for row in cur.execute("select pmid,keyword from student where Keyword LIKE '%gene%'"):
#     tmp = str(row)
#     tmp = tmp.replace("[","").replace("]","").replace(" '","").replace("' ","").strip()
#     print(tmp)

# # print("-----------------")

# for row in cur.execute("select pmid,keyword from student where Keyword LIKE '%patterns%'"):
#     tmp = str(row)
#     tmp = tmp.replace("[","").replace("]","").replace(" '","").replace("' ","").strip()
#     print(tmp)

# Close connection to SQLite database

# examples of queries
# select keyword from student where Keyword LIKE '%virus%';
# select keyword from student where Keyword LIKE '%analysis%' AND keyword LIKE '%research%';
# select pmid,keyword from student where Keyword LIKE '%gene%';

# end of builder()





# # @st.cache_data
def loadDbGetConn(myDBFile_str):
    """ Function to load an sqlite3 file and then return conn."""
    # st.text("dbOps::loadDBGetConn()")
    st.text(f"loadDbGetConn() received filename :{myDBFile_str}")
    # conn = sqlite3.connect(myDBFile_str)
    conn = sqlite3.connect(myDBFile_str)
    c = conn.cursor()
    st.text(f"loadDbGetConn() : returning cursor ---> {c}")
    return c
#     # end of loadDbGetConn()

def getTablesListing(myConn):
    st.write("getTablesListing()")
    myQuery_str = "SELECT name FROM sqlite_master WHERE type='table'"
    # st.text(f"getTablesListing()::: myConn ::::: {myConn}, query ::::: {myQuery_str}")
    result = sql_executor(myConn,myQuery_str)
    # st.text(f"getTablesListing()::: result = {result}}")
    return result
    # end of getTablesListing()


# Fxn Make Execution
def sql_executor(myConn,myCommand_str):
    """ function to complete the query and parse results from a query."""
    # if myCommand_str is None:
    st.text(f"sql_executor() :: conn ---> {myConn},  myCommand_str = <{myCommand_str}> ")
    thisResult = myConn.execute(myCommand_str)
    st.text(f"sql_executor() thisResult = {thisResult}")
    data = myConn.fetchall()
    st.text(f"sql_executor() : {data}")
    return data
# end of sql_executor()

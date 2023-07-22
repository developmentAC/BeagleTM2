# Import required libraries
import sqlite3, typer
import pandas as pd
from beagletm2 import fileOps

from rich.console import Console

# globals
# dir_str = "0_out/"
dir_str = fileOps.dir_str

# cli = typer.Typer()
console = Console()


def main(csv_file:str, wordCsv_file:str) -> None:
    """driver function"""
    tableName_str = "main"
    dbfname_str = csv_file.replace(".csv", ".sqlite3") #database filename
    builder(dbfname_str, csv_file, tableName_str) # build the first database

    tableName_str = "counts"
    # dbfname_str = wordCsv_file.replace(".csv", ".sqlite3") #database filename
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

    # dbfname_str = fname_str.replace(".csv", ".sqlite3")

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

    console.print(f"\n\t :Rocket:[bold yellow] DB File saved to: {dbfname_str}")


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

# Import required libraries
import sqlite3, typer
import pandas as pd
import streamlit as st

from rich.console import Console

import plotOps
import fileOps


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



# Fxn Make Execution
def sql_executor(myConn,myCommand_str):
    """ function to complete the query and parse results from a query."""
    thisResult = myConn.execute(myCommand_str)
    data = myConn.fetchall()
    return data
# end of sql_executor()


# # @st.cache_data
def loadDbGetConn(myDBFile_str):
    """ Function to load an sqlite3 file and then return conn."""
    conn = sqlite3.connect(myDBFile_str)
    c = conn.cursor()
    return c
#     # end of loadDbGetConn()


def getTablesListing(myConn):
    """ Prepare a query to get table names in SQL db, run query, display results as pretty table."""
    myQuery_str = "SELECT name FROM sqlite_master WHERE type='table'"
    st.write("Query Code")
    st.code(myQuery_str, language = 'bash')
    results = sql_executor(myConn,myQuery_str)
    prettyTabler(results)
    return results
    # end of getTablesListing()


def prettyTabler(results):
    """Show results in pretty table formatting."""
    st.write("Results of query")
    with st.expander("Pretty Table of database tables"):
        query_df = pd.DataFrame(results)
        st.dataframe(query_df)
    # end of prettyTabler()



def listCleaner(in_list) -> list:
    """Function to remove extra textual clutter from returned lists from queries."""
    tmp_list = []
    for i in in_list:
        tmp_list.append(i[0])
    # st.success(tmp_list)
    return tmp_list
    #end of listCleaner()


def selectAllKwsInArticles(myConn):
    """Function to prepare networks of articles which have simultaneous presence of one or more keywords."""
    # write query to determine available keywords.
    myQuery_str =  "SELECT keyword FROM 'counts';"
    st.write("Query Code")
    st.code(myQuery_str, language = 'bash')

    keyWords_list = sql_executor(myConn, myQuery_str)
    prettyTabler(keyWords_list)
    keyWords_list = listCleaner(keyWords_list)
    # st.success(f"selectAllKwsInArticles() : keywords_list --> {keyWords_list}")

    selectedKws_list = st.multiselect(
        "Check and Build network",
        keyWords_list,
        [],
    )  # the selected keywords from the user.

# what are the keywords to select from?
    wordNetwork_btn = st.button(
        "Find articles containing ALL selected keywords in abstracts. Click for all keywords in set."
    )



# query pmids from entered keywords

    # st.success(f"Selected keywords :'%{selectedKws_list}%' ")
    myQuery_str = ""
    tmp_str = ""
    try:
        myQuery_str =f"SELECT Pmid,\"References\", Title FROM main WHERE keyword LIKE '%{selectedKws_list[0]}%'"
        if len(selectedKws_list) > 1:# the list of selected words
            for i in range(1, len(selectedKws_list),1):
                tmp_str = tmp_str + f" AND keyword LIKE '%{selectedKws_list[i]}%'"
    except Exception:
        pass

    # myQuery_str =  "SELECT Pmid,keyword FROM main WHERE keyword like "%mRNA%" and keyword like "%observe%";"
    myQuery_str = myQuery_str + tmp_str
    st.write("Query Code")
    st.code(myQuery_str, language = 'bash')

    pmids_list = sql_executor(myConn, myQuery_str)
    # pmids_list = listCleaner(pmids_list)
    
    prettyTabler(pmids_list) # show results of query





    if st.button('Make Networkx plot of results'):
        st.write('Making plot')

        saveDataAsCSV(pmids_list) # prep a csv dataframe of results
#        # plotOps.makePlot(pmids_list,"Abstract","Pmid")
        plotOps.makeNetworkxPlot()
    else:
        st.write('ok')
        
    # end of selectAllKwsInArticles()

def saveDataAsCSV(pmids_list):
    """ function to make a tidy csv quality dataframe"""
    st.write("saveDataAsCSV()")
    # print(pmids_list)

    # line by line creation of csv file
    CSV_str = "Pmid, Reference\n" # line by line of all the csv lines here
    for i in pmids_list:
        line = i
        # print(f"1st line = {line[0]}\n")
        # print(f"2nd line = {line[1]}, {type(line[1])}\n")
        # print(f"3rd line = {line[2]}\n")
        pmidValue_int = int(line[0])

        # convert string to list
        references_list = "".join(list(line[1]))
        references_list = list(references_list.split(","))

        for ref in references_list:
            ref_line = str(pmidValue_int) +","+ ref.strip().replace("[","").replace("]","")
            CSV_str = CSV_str + ref_line + "\n"

    print(CSV_str)
    # save the csv
    import fileOps

    fileOps.saveCSV(CSV_str,"pmidsRefs.csv")
            


### output
# 1st line = 12975657.0

# 2nd line = [12219091, 9254694, 11752243, 9278503, 11102698, 11750686, 12560809, 11431701, 10555290, 12024217, 12097345, 12907801, 12142430, 10381871, 7542800, 9021275, 12446813, 12116432, 10952301, 12554446, 10097118, 1633570, 11443357, 9089078, 11248100, 11677609, 8610134, 12107590, 10360571, 11675594, 11118198, 10830951, 11586360, 11677608, 12705866, 11206551, 11934758, 10993077, 10910347, 11070046, 12572614, 10984043, 8805245, 7984417, 9799792, 9864315, 9244264, 2439888, 12175808, 10464188, 12228001]

# 3rd line = From Gene Trees to Organismal Phylogeny in Prokaryotes:The Case of the &#947;-Proteobacteria



    # end of saveDataAsCSV()
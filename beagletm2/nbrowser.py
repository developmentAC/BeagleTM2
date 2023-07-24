
# Load libraries
import streamlit as st
import pandas as pd
import fileOps as fo # for grabFile()
import dbOps
# DB Mgmt
import sqlite3


# # global variables
# FILE_EXTENTION = "csv"
# DATADIR = "data/"
# OUTDATADIR = "0_outAnalysis/"  # output directory

banner0_str = """
  ██████╗ ███████╗ █████╗  ██████╗ ██╗     ███████╗████████╗███╗   ███╗
  ██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝╚══██╔══╝████╗ ████║
  ██████╔╝█████╗  ███████║██║  ███╗██║     █████╗     ██║   ██╔████╔██║
  ██╔══██╗██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝     ██║   ██║╚██╔╝██║
  ██████╔╝███████╗██║  ██║╚██████╔╝███████╗███████╗   ██║   ██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝     ╚═╝
"""
# banner ref: https://manytools.org/hacker-tools/ascii-banner/


myDBFile_str = "/tmp/kw_short_analysis_out_save-less.sqlite3"
# conn = sqlite3.connect(myDBFile_str)
# myConn = conn.cursor()



from io import StringIO




def main() -> None:
    """Driver function of the network browser. """
    st.title("BeagleTM2 Network Browser")
    # st.subheader("SQL Database Managment")
    st.text(banner0_str)

    # myConn = None # define variable for conn from database which is given later


###

    # st.sidebar.text("Open a file")
    # uploaded_file = st.sidebar.file_uploader("Choose a file",accept_multiple_files=False)
    # myConn = None
    # if uploaded_file is not None:
    #     myDBFile_str = str(uploaded_file.name)
    #     st.success(f"{myDBFile_str}")
    #     st.success(f"main() file -> {uploaded_file.name}")
    myConn = dbOps.loadDbGetConn(myDBFile_str)
    #     st.text(f"myConn == {myConn}")
    #     conn = sqlite3.connect(myDBFile_str)
    #     st.text("loadDbGetConn() : returning cursor")
    #     myConn = conn.cursor()

    # menu system
    doThis_sb = None
    doThis_sb = st.sidebar.selectbox(
        "What are we doing with this data?",
        [
            "Show_Tables",
            "Balloons",
	        "Snow"
        ],
    )
    
    if doThis_sb == "Show_Tables":
        st.text("Showing tables of database ...")
        # result = dbOps.getTablesListing(myConn)
        myQuery_str = "SELECT name FROM sqlite_master WHERE type='table';"
        result = myConn.execute(myQuery_str)
        result_str = myConn.fetchall()

        st.text(f"myConn ::: {myConn}, result :::: {result_str}")
	


    if doThis_sb == "Balloons":
        st.balloons()

    if doThis_sb == "Snow":
        st.snow()

    # end of main()



def getTablesListing(myConn)->None:
    """ function to show tables on new page"""
    st.title("Tables")
    # myCursor=myConn.cursor()
    # end of getTablesListing()
    with st.form(key='query_form'):

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
    return(sql_executor(myConn,myQuery_str))

    # end of getTablesListing()









def old_main():
	st.title("BeagleTM2 Network Browser")

	menu = ["Home","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Database Output")

		# Columns/Layout
		myCol1, myCol2 = st.columns(2)


		# Results Layouts
		with myCol1:
			with st.form(key='query_form'):
				myCommand_str = st.text_area("SQL Code Here")
				submit_button = st.form_submit_button("Execute")

				# commit_code = st.form_submit_button("Commit Changes")

				# st.balloons() # show some balloons!
				# st.snow()
				# st.success("oh yeah")


				st.write("Command to list tables.")
				copyThis_tmp = "SELECT name FROM sqlite_master WHERE type='table';"
				st.code(copyThis_tmp, language = 'bash')
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

			with st.form(key='row1'):
				st.write("Query")

				myTable_str = st.text_input("Enter Table name")
				q_attribute1_str = st.text_input("Enter 1st attribute name")
				q_attribute2_str = st.text_input("Enter 2nd attribute name")
				myQueryButton = st.form_submit_button("Build Query String")

				if myQueryButton: # if clicked
					myQuery_str = f"SELECT {q_attribute1_str},{q_attribute2_str} FROM {myTable_str}"
					st.code(myQuery_str , language = 'bash')


	else:
		st.subheader("About")
		st.write("Put about information here!! ")
    # end of old_main()

if __name__ == '__main__':
	main()

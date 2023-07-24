
# Load libraries
import streamlit as st
import pandas as pd
import fileOps as fo # for grabFile()
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


# myDBFile_str = "myCampusDB.sqlite3"
# conn = sqlite3.connect(myDBFile_str)
# c = conn.cursor()


# Fxn Make Execution
def sql_executor(myCommand_str):
	""" function to complete the query and parse results from a query."""
	c.execute(myCommand_str)
	data = c.fetchall()
	return data
# end of sql_executor()


def main() -> None:
    """Driver function of the network browser. """
    st.title("BeagleTM2 Network Browser")
    st.text(banner0_str)

    myFile_str = fo.grabFile() # from fileOps as fo
    try:
        data = fo.load_big_data(myFile_str)
        # create a dictionary having headers as keys and values as lists of column data.
        data_dic = hc.createMasterDataDic(data)
    except:
        st.sidebar.error("No data entered...")

    # # menu system
    # doThis_sb = st.sidebar.selectbox(
    #     "What are we doing with this data?",
    #     [
    #         "ReadMe",
    #         "Show_data",
    #         "Article inter-connectivity",
    #         "Articles containing ANY of the selected keywords",
    #         "Articles containing ALL of the selected keywords",
    #         "Heatmaps of keyword saturation",
    #         "Make Simple Heatmaps",
    #         "Statistics",
    #     ],
    # )
    # if doThis_sb == "ReadMe":
    #     with open("README.md") as readme_file:
    #         # Note : the FILE README.MD is assumed to be in the directory behind this one.
    #         st.markdown(readme_file.read())


    # end of main()





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

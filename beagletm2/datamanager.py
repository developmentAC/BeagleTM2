""" functions to manage data."""

import streamlit as st
import matplotlib.pyplot as plt

def demopullKeyWords(dataframe, colName_str):
    """function to pull specific keywords from the main dataframe"""
    st.write(f"headers of cols : {dataframe.dtypes}")
    st.write(f"years ::{dataframe.Year}")
    tmp = set([i for i in dataframe.Year])
    st.write(f"datamanager() years listed :{tmp}")
# end of demodataframe()

def pullKeyWords(dataframe, colName_str):
    """function to pull specific keywords from the main dataframe"""
    # st.write(f"headers of cols : {dataframe.dtypes}")
    # st.write(f"years ::{dataframe.Year}")
    tmp = set([i for i in dataframe.Year])
    st.write(f"datamanager() years listed :{tmp}")

# end of dataframe()


def getHeaders(dataframe):
    """ returns a list of headers from the dataframe"""
    tmp  = [i for i in dataframe.dtypes.keys()]
    # st.write(f"getHeaders : {tmp}, {type(tmp)}")
    return tmp

# end of getHeaders

    # create a dataframe
#     # Import pandas library
# import pandas as pd
  
# # initialize list of lists
# data = [['tom', 10], ['nick', 15], ['juli', 14]]
  
# # Create the pandas DataFrame
# df = pd.DataFrame(data, columns=['Name', 'Age'])
  
# # print dataframe.
# df
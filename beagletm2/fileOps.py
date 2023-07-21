#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import csv,os,typer

# globals
dir_str = "0_out/"

cli = typer.Typer()
console = Console()



def openFile(data_file: str) -> list:
    """function to open and read the keyword file (text). Returns data as list of words"""

    with open(data_file, 'r') as file:
        contents_list = []
        for line in file:
            line = line.strip()
            contents_list.append(line)
    
    console.print(f" [bold green] contents_list = {contents_list}")
  
    return contents_list

# end of openFile()

def openArticleFile(inFile1):
    """open a text file, return string"""

    try:  # is the file there??
        f = open(inFile1, "r").read()  # returns a string
        return f
    except IOError:
        console.print(f"\t :scream: Error opening file :{inFile1} ")
# end of openArticleFile()

def saveResultsFromDic(master_dic:dict, kwFileName_str:str, headers_list:list, abs_only: bool, save_less: bool) -> None:
    """ pull out each record of the saved results and save as csv file. 
    abs_only : bool to process only abstracts. Used here to alter filename.
    save_less : bool to save fewer results in output. Used here to alter filename."""
    # console.print(f"[bold cyan] saveResultsFromDic.")
    # console.print(f"kwFileName_str: {kwFileName_str}")
    # console.print(f"headers_list: {headers_list}")
    # console.print(f"master_dic: {master_dic}")


    #set up large list to dump into csv file
    data_list = []
    for i in master_dic:
        data_list.append(master_dic[i])


    # place contents into csv file
    absOnlyTag_str = ""
    if abs_only:
         absOnlyTag_str = "_abs-only"

    saveLess_str = ""
    if save_less:
         saveLess_str = "_save-less"


    addToFilename_str = absOnlyTag_str+saveLess_str

    kwFileName_str = str(kwFileName_str).replace(".md","")
    # csv_file =  dir_str + kwFileName_str + addToFilename_str + "_analysis_out.csv"
    csv_file =  dir_str + kwFileName_str + "_analysis_out" + addToFilename_str + ".csv"

    checkDataDir(dir_str) # does the data directory exist? If not make it exist.

    try:
        with open(csv_file, 'w') as csvfile:

            write = csv.writer(csvfile)
            write.writerow(headers_list)
            write.writerows(data_list)

	
    except IOError:
        console.print("\t :scream: [bold red] Input/Output error")
        exit()
    console.print(f"\n\t :Rocket:[bold yellow] File saved to: {csv_file}")

    return csv_file # return file name for database maker

# end of saveResultsFromDic()


def checkDataDir(dir_str):
#function to determine whether a data output directory exists.
#if the directory doesnt exist, then it is created

	try:
		os.makedirs(dir_str)
		#if DIR doesn't exist, create directory
		return 1

	except OSError:
		return 0
#end of checkDataDir()

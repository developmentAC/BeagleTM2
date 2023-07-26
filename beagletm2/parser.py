#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import os, typer
from beagletm2 import fileOps
from beagletm2 import extractor


# globals
FILE_EXTENTION1 = "nxml"
FILE_EXTENTION2 = "xml"
CORPUS_DIR = "corpus/"  # location of corpus files


cli = typer.Typer()
console = Console()


def main(dataFile_str: str, abs_only: bool, make_db: bool, save_less: bool) -> None:
    """myFilename is passed to goThruFiles to name the results file. keyword_list is a listing of words.
    make_db -- bool to make an SQL database of the results (default).. Set to False to disable db creation at the end.
    abs_only -- bool to parse only abstracts (default). Set to False to parse the whole article.
    reducedSave -- bool to save the first 100 chars (one lines) of the abstract in the results.
    """
    console.print(f"\t :package:[bold green] Welcome! This is Parser!")
    keyWord_list = fileOps.openFile(dataFile_str)  # Open file, get list
    console.print(f"\n\t[bold blue] Keywords [bold purple]: {keyWord_list}")

    console.print(
        f"\n\t[bold blue] Scanning only abstracts        : [bold yellow] {abs_only}"
    )
    console.print(
        f"\t[bold blue] SQL Database of results        : [bold yellow] {make_db}"
    )
    console.print(
        f"\t[bold blue] Save less data in results file : [bold yellow] {save_less}"
    )
    # pass the filename (str) for labelling output, and list of words, return a dictionary of pmid (key) and records (value), scanning for abstracts or the full document?
    master_dic, headers_list = goThruFiles(
        dataFile_str, keyWord_list, abs_only, save_less
    )

    master_dic = cleaner(master_dic) # remove empty records

    # save the results from master_dic
    csv_file, wordCsv_file = fileOps.saveResultsFromDic(
        master_dic, dataFile_str, headers_list, abs_only, save_less
    )
    return csv_file, wordCsv_file  # return filenames of analysis for database maker.


# end of main()


def cleaner(in_dic):
    """A function to remove empty records and pmid none types from inputted dictionary."""
    # console.print(f"[bold blue] cleaner() dictionary keys -> {in_dic.keys()} ")

    # remove None keys

    target_key = None
    tmp_dic = {}

    for i in in_dic:
        if i != target_key:
            tmp_dic[i] = in_dic[i]
    return tmp_dic
    # end of cleaner()

def getFileListing() -> list:
    """method to grab all files with a particular extension"""
    files_list = []  # holds each file and directory
    for root, dirs, files in os.walk(CORPUS_DIR):
        for file in files:
            if file.endswith(FILE_EXTENTION1) or file.endswith(FILE_EXTENTION2):
                dataFile = os.path.join(root, file)
                files_list.append(dataFile)
    # console.print(f"\t [bold blue] getfileListing : files_list : {files_list}")
    return files_list


# end of getFileListing()


def goThruFiles(
    inFile0_str: str, keyWord_list: list, abs_only: bool, save_less: bool
) -> dict:
    """file collecting, loading and parsing Accepts a list of keyword (words in strings)"""


    master_dic = {} # store all retrieved data from articles as lists in dictionary structure


    file_list = (
        getFileListing()
    )  # get a listing of the files out there in the corpus dir.
    if len(file_list) == 0:
        console.print(f"\t [bold red] :scream: No input corpus files? Exiting...")
        exit()
    # console.print(f"\n\t[bold blue] Corpus files [bold purple]: {file_list}, {type(file_list)}")

    # load each files separately for parsing for information
    headers_list = []
    pmidsubNumber = 0  # used for files having no pmid value
    fileCount_int = 0  # used to keep track of the number of processes files.

    for thisFile in file_list:
        contents_str = ""
        contents_str = fileOps.openArticleFile(thisFile)
        fileCount_int += 1
        # initiate class
        # p = myParser(f, data_str, keyWord_list)  # send filename, contents of file, list of key words

        p = extractor.parserEngine(
            thisFile, contents_str, keyWord_list, abs_only, save_less
        )


        headers_list = p.getTitlesOfCols()
        # console.print(f"[bold green] headers_list is : {headers_list}")
        # for header in headers_list:
        #     console.print(f"\t\t[bold blue] {header} {type(header)}")
        #     # Title <class 'str'> [0]
        #     # Abstract <class 'str'> [1]
        #     # PMID <class 'str'> [2]
        #     # Journal <class 'str'> [3]
        #     # Year <class 'str'> [4]
        #     # References <class 'str'> [5]
        #     # Keyword <class 'str'> [6]
        #     # Counts <class 'str'> [7]

        tmp_list = p.getInformationOfKwInDocs()

        if tmp_list != None: # contains the information from article

            # console.print(f"[bold red] goThruFiles() tmp_list  = {tmp_list }")

            console.print(
                f"\n\t :dog: [bold cyan]{tmp_list[2]}[white],[bold green] {thisFile}" # pmid
            )
            console.print(
                f"\t :sparkles: Parsed: {tmp_list[6]} <- [bold yellow] {tmp_list[7]}"
            )
            console.print(
                f"\t   [bold cyan]   [bold cyan] {fileCount_int} of {len(file_list)}",
                end="",
            )
            console.print(f"[bold blue] tmp_list[2] --> {tmp_list[2]}, {type(tmp_list[2])}")



            if type(tmp_list[2]) == list:  # (empty) list returned but no pmid value found in NXML!
                console.print(f"[bold yellow] +++++++++++ {tmp_list[2]}")

# todo #!!!!!!!!!!!!!!!!!!!!! pmidsubNumber

                tag = "noPMID_" + str(pmidsubNumber) #!!!!!!!!!!!!!!!!!!!!!

                master_dic[tag] = tmp_list  # place in dic; pmid as key, record as value
                console.print(
                    f"\n\t ---> [bold purple]{tmp_list[2]} renamed to [bold green] {tag}"
                )


# record a temp id for this record
                master_dic[tag] = tmp_list  # place in dic; pmid as key, record as value


                # console.print(f"[bold yellow] +++++++++++ {tmp_list[2]}")
                # console.print(f"[bold yellow] +++++++++++ {master_dic}")
                # input()
                pmidsubNumber = pmidsubNumber + 1

            else:
                master_dic[
                    tmp_list[2]
                ] = tmp_list  # place in dic; pmid as key, record as value

            # console.print(f"[bold purple] tmp_list ==> {tmp_list}")
    # console.print(f"[bold purple] master_dic ==> {master_dic}")

    return master_dic, headers_list


# end of goThruFile()

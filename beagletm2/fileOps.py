#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import csv, os, typer

# globals
dir_str = "0_out/"

cli = typer.Typer()
console = Console()


def openFile(data_file: str) -> list:
    """function to open and read the keyword file (text). Returns data as list of words"""

    with open(data_file, "r") as file:
        contents_list = []
        for line in file:
            line = line.strip()
            contents_list.append(line)

    # console.print(f" [bold green] contents_list = {contents_list}")

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


def saveResultsFromDic(
    master_dic: dict,
    kwFileName_str: str,
    headers_list: list,
    abs_only: bool,
    save_less: bool,
) -> None:
    """pull out each record of the saved results and save as csv file.
    abs_only : bool to process only abstracts. Used here to alter filename.
    save_less : bool to save fewer results in output. Used here to alter filename."""
    # console.print(f"[bold cyan] saveResultsFromDic.")
    # console.print(f"kwFileName_str: {kwFileName_str}")
    # console.print(f"headers_list: {headers_list}")
    # console.print(f"master_dic: {master_dic}")

    # set up large list to dump into csv file
    data_list = []

# master_dic record looks like:
# saveResultsFromDic() 17183658,['Triose Phosphate Isomerase Deficiency Is Caused by Altered Dimerization&#8211;Not Catalytic Inactivity&#8211;of the Mutant Enzymes', '<abstract><p>Triosephosphate isomerase (TPI) deficiency is an autosomal recessiv', 17183658, 'PLoS One', '2006', [14242501, 10916682, 8807088, 12023819, 8571957, 3447514, 7155666, 6381286, 3358419, 6946452, 113220, 2693209, 8944178, 2876430, 9338582, 1339398, 10910933, 8503454, 8244340, 9871806, 9294216, 7816830, 10655478, 7737504, 16842759, 9483801, 15383276, 2692852, 8879153, 12039737, 378952, 15001397, 15102338, 16115810, 15489199, 16116786, 5542016, 16221686, 11698297, 14608502, 7708701, 15959805, 9322041, 11674994, 7565735, 10998258, 11251834, 10330404, 10601882, 1959537, 12359716, 5076768, 4434738, 16381912, 15606901, 16081222, 10851077, 15501681, 16086671, 5353890, 7651192, 15087496, 12755685, 11053248, 12446208, 10082531, 8181459, 7929187, 7586028, 15862094, 11213485, 1870650], ['observed', 'observe', 'mRNA'], [18, 19, 6]]
# saveResultsFromDic() 17183679,['Concentration of the Most-Cited Papers in the Scientific Literature: Analysis of Journal Ecosystems', '<abstract><sec><title>Background</title><p>A minority of scientific journals pub', 17183679, 'PLoS One', '2006', [16391221, 15173104, 15254529, 15169550, 16690827, 15819606, 12038930, 16701337, 16701421, 14633274, 15118046, 15900006, 16014596, 16749869, 16275915], ['central'], [2]]

    for i in master_dic:
        # print(f"saveResultsFromDic() {i},{master_dic[i]}")
        data_list.append(master_dic[i])

    secondDB_list = buildWordBase(master_dic)

    # place contents into csv file
    absOnlyTag_str = ""
    if abs_only:
        absOnlyTag_str = "_abs-only"

    saveLess_str = ""
    if save_less:
        saveLess_str = "_save-less"

    addToFilename_str = absOnlyTag_str + saveLess_str

    kwFileName_str = str(kwFileName_str).replace(".md", "")
    # csv_file =  dir_str + kwFileName_str + addToFilename_str + "_analysis_out.csv"
    csv_file = dir_str + kwFileName_str + "_analysis_out" + addToFilename_str + ".csv"

    checkDataDir(dir_str)  # does the data directory exist? If not make it exist.

    try:
        with open(csv_file, "w") as csvfile:
            write = csv.writer(csvfile)
            write.writerow(headers_list)
            write.writerows(data_list)

    except IOError:
        console.print("\t :scream: [bold red] Input/Output error")
        exit()
    console.print(f"\n\t :Rocket:[bold yellow] File saved to: {csv_file}")

    return csv_file  # return file name for database maker


# end of saveResultsFromDic()

def buildWordBase(master_dic):
    """ function to build a smaller db: [word (pk)|count|pmid] """

# saveResultsFromDic() 17183679,
# [
# 'Concentration of the Most-Cited Papers in the Scientific Literature:',
# '<abstract><sec><title>Background</title><p>A minority of scientific journals pub',
# 17183679,
# 'PLoS One',
# '2006',
# [ 16690827, 15819606, 12038930, 16701337, 16701421, 14633274, 15118046, 15900006, 16014596, 16749869, 16275915],
# ['central'],
# [2]
# ]


    word_dic = {}
    for row in master_dic:
        console.print(f"[bold green]row = {row}")
    # 6th element is word
        wordRow_list = master_dic[row][6] 
        console.print(f"[bold green]wordRow_list = {wordRow_list}")
    # 7th element is count,
        countRow_list = master_dic[row][7]
        console.print(f"[bold green]countRow_list = {countRow_list}\n")
        for w in range(len(wordRow_list)):
            console.print(f"[bold yellow] word_dic = {word_dic}")
            if wordRow_list[w] not in word_dic:
                word_dic[wordRow_list[w]] = countRow_list[w]
            else:
                word_dic[wordRow_list[w]] = word_dic[wordRow_list[w]] + countRow_list[w]



    # end of buildWordBase()





def checkDataDir(dir_str):
    # function to determine whether a data output directory exists.
    # if the directory doesnt exist, then it is created

    try:
        os.makedirs(dir_str)
        # if DIR doesn't exist, create directory
        return 1

    except OSError:
        return 0


# end of checkDataDir()

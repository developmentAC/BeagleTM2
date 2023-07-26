#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
import xml.etree.ElementTree as ET

import re, typer

cli = typer.Typer()
console = Console()

# globals
# myCHARSLIMIT = 10
MAXCHARS = 80  # size of text to include in output


class parserEngine(object):
    def __init__(self, filename_str, contents_str, keyword_list, abs_only, save_less):
        self.filename_str = filename_str  # name of keyword file
        self.contents_str = contents_str  # the article's text
        self.keyword_list = keyword_list  # the listing of keywords to parse in article
        self.abs_only = abs_only  # boolean, searching abstracts only or the whole article (all contents of the nxml file?)
        self.save_less = save_less  # boolean, save less data in results?

    # end of __init__()

    def getInformationOfKwInDocs(self) -> list:
        """A Method to locate the keywords in the document abstracts. If any keyword is found, return all details to program. Returns a list"""

        # console.print(f"____ getInformationOfKwInDocs() _____")

        pmid_str = self.getPmid()
        # console.print(f"[bold yellow] pmid --> {pmid_str} type: {type(pmid_str)}")
        if type(pmid_str) == list: # no pmid number available, assign a temp one.
            # console.print(f"\n\t :poop: Missing pmid value. [bold yellow] pmid assigned --> {pmid_str}")
            return None # no pmid number, reject the record

        searchabletext_str = (
            ""  # variable to hold the text (abs or whole contents) to scan
        )

        # get the text to work on

        # get abstracts only
        if self.abs_only:  # checking only abstracts
            searchabletext_str = self.getAbstract()

        else:  # get full article. This text is all between <abstract> and the <references>.
            try:
                searchabletext_str = self.contents_str[
                    self.contents_str.find("<abstract>") + 10: self.contents_str.find(
                        "<ref-list>"
                    )+10
                ]
            except Exception:
                searchabletext_str = None

        if searchabletext_str == None:
            ## console.print(f"\t:poop: [bold red] Error in searchabletext_str = {searchabletext_str}")
            searchabletext_str = ""


        # check each keyWord against searchabletext_str
        foundKeywords_list, foundKeywordCounts_list = self.getWordCount(
            searchabletext_str
        )

        title_str = self.getTitle()


        abstract_str = self.getAbstract()
        if self.save_less:
            abstract_str = searchabletext_str[
                :MAXCHARS
            ]  # MAXCHARS defined as global above

        journal_str = self.getJournal()
        refs_list = self.getReferences()
        year_int = self.getYear()
        # see above: foundKeywords_list, foundKeywordCounts_list

        # console.print(f"""
        #     [bold cyan]title_str: [bold yellow]{title_str},
        #     [bold cyan]pmid_str: [bold yellow]{pmid_str},
        #     [bold cyan]abstract_str: [bold yellow]{abstract_str},
        #     [bold cyan]journal_str: [bold yellow]{journal_str},
        #     [bold cyan]refs_list: [bold yellow]{refs_list},
        #     [bold cyan]year_int: [bold yellow]{year_int},
        #     [bold cyan]foundKeywords_list: [bold yellow]{foundKeywords_list},
        #     [bold cyan]foundKeywordCounts_list:[bold yellow] {foundKeywordCounts_list}
        #     """)

        # combine all this data into one list (Title,Abstract,PMID,Journal,Year,References,Keyword,Counts) to return
        tmp_list = []
        tmp_list.append(title_str)
        tmp_list.append(abstract_str)
        tmp_list.append(pmid_str)
        tmp_list.append(journal_str)
        tmp_list.append(year_int)
        tmp_list.append(refs_list)
        tmp_list.append(foundKeywords_list)
        tmp_list.append(foundKeywordCounts_list)

        # console.print(f"[bold green] {tmp_list}")

        return tmp_list

    # end of getInformationOfKwInDocs

    def getWordCount(self, searchabletext_str) -> dict:
        """Method to check all words in a text sample. Return two lists: FoundKeywords, FoundKeywordCounts"""

        kwBank_dic = {}  # keep track of which keywords appear in the text
        for kw in self.keyword_list:
            # print(f"{kw}", end = ",")
            kwBank_dic[kw] = searchabletext_str.count(kw)
        # console.print(f"kwBank_dic = [bold yellow] {kwBank_dic}")

        # extract word and count information from the dic
        foundKeywords_list = []
        foundKeywordCounts_list = []
        for i in kwBank_dic:
            if kwBank_dic[i] != 0:
                # console.print(f"\t    :sparkles: {i} : {kwBank_dic[i]}")
                foundKeywords_list.append(i)
                foundKeywordCounts_list.append(kwBank_dic[i])
        return foundKeywords_list, foundKeywordCounts_list
        # end of getWordCount()

    def getTitlesOfCols(self):
        """Method to call each of the information gathering methods to determine what the headers of the information should be called. Each method (i.e., getTitle()) has a task that will only return the header name. Note, be sure have header names in the order of the data."""

        #  We are appending this list to the top of the main list of article details. The header list is collected each time the parser methods are run.

        # console.print(f"extractor :: getTilesOfCols()")
        headers_list = []
        # get the names of the data's headers. (i.e,. the titles of the columns)
        headers_list.append(self.getTitle("headerCall"))
        headers_list.append(self.getAbstract("headerCall"))
        headers_list.append(self.getPmid("headerCall"))
        headers_list.append(self.getJournal("headerCall"))
        headers_list.append(self.getYear("headerCall"))
        headers_list.append(self.getReferences("headerCall"))

        # we have to add some column headers manually... :-(
        headers_list.append("Keyword")
        headers_list.append("Counts")
        return headers_list

    # end of getTitlesOfCols()

    def getTitle(self, task_str=None):
        """Method to get the title of article in the xml doc. The task_str is a command to only return the column header f the method and will be used in the CVS file creation."""
        # print("\t [+] getTitle()")
        if task_str == "headerCall":
            return "Title"

        # title:tag, get child.text
        childTag = "article-title"

        self.title_str = self.extractTextFromElement0(childTag)

        return self.title_str

    # end of getTitle()

    def getAbstract(self, task_str=None):
        """gets the title of main article in the xml doc"""
        # abstract, get abstract from child.tag
        if task_str == "headerCall":
            return "Abstract"

        childTag = "abstract"
        # 		f_str = self.extractTextFromElement0(childTag, self.data_str)
        self.abstract_str = self.extractTextFromElement0(childTag)
        return self.abstract_str

    # end of getAbstract()

    def getPmid(self, task_str=None) -> list:
        """gets the main pmid (pubmed's primary key) of main article in the xml doc"""
        # article pmid
        if task_str == "headerCall":
            return "PMID"

        childTag = "article-id"
        attrib_str = "pmid"

        f_list = self.extractTextFromElement1(childTag, attrib_str)

        try:
            return f_list[0]  # gimme a string, not a list
        except:
            return f_list

    # end of getPmid()

    def getJournal(self, task_str=None):
        """gets the journal name of main article in the xml doc"""
        # journal name
        if task_str == "headerCall":
            return "Journal"

        childTag = "journal-id"
        attrib_str = "nlm-ta"

        f_list = self.extractTextFromElement1(childTag, attrib_str)

        try:
            return f_list[0]  # gimme a string, not a list
        except:
            return f_list

    # end of getJournal()

    def getReferences(self, task_str=None):
        """gets list of references of main article in the xml doc"""
        # #references (pmids)
        if task_str == "headerCall":
            return "References"

        childTag = "pub-id"
        attrib_str = "pmid"
        # 		f_list = self.extractTextFromElement1(childTag, self.data_str, attrib_str)
        f_list = self.extractTextFromElement1(childTag, attrib_str)

        return f_list

    # end of getReferences()

    def getYear(self, task_str=None):
        """gets the year of main article in the xml doc"""
        # abstract, get abstract from child.tag
        if task_str == "headerCall":
            return "Year"

        childTag = "year"
        f_str = self.extractTextFromElement0(childTag)
        return f_str

    # end of getYear()

    def extractTextFromElement0(self, childTag):
        """Pulls element from tag.child. Usage: extractTextFromElement('tag2', XML_data)"""
        # print("\n\t + extractTextFromElement0()")
        try:
            tree = ET.fromstring(self.contents_str)
        except ET.ParseError as err:
            # printErrorByPlatform("Error detected in current File")
            return None

        # for child in tree.getiterator(): # formerly for Python 3.8
        for child in tree.iter():  # Python 3.10
            tmp_str = (
                "child.tag: "
                + str(child.tag)
                + str(type(child.tag))
                + "\n child.attrib :"
                + str(child.attrib)
                + "\n child.text :"
                + str(child.text)
                + "\n child.tail :"
                + str(child.tail)
            )
            # debugging info
            # console.print(f"[bold blue]{tmp_str}")
            # print("child.tag: ",child.tag, type(child.tag))
            # print("child.attrib :", child.attrib) # dict
            # print("child.text :", child.text) #attrib
            # print("child.tail :", child.tail)
            # 		if child.tag == childTag:
            if childTag in child.tag:
                # print("tag found...",child.tag, type(child.tag), childTag)
                len = (
                    ET.tostring(child)
                    .decode("utf-8")
                    .replace("\n", " ")
                    .replace("  ", "")
                    .strip()
                )
                # print("len type :",type(len))
                return re.sub(r"<.*?>", "", len)

    # end of extractTextFromElement0()

    def extractTextFromElement1(self, childTag, attribTag_str):
        """Pulls element from tag.child. Works with lists. Usage: extractTextFromElement('tag2', XML_data, attribTag_str)"""

        tmp_str = "\t attribTag_str: " + attribTag_str + "\n\t childTag: " + childTag

        tmp_list = []
        try:
            tree = ET.fromstring(self.contents_str)
        except ET.ParseError as err:
            # printErrorByPlatform("Error detected in current File")
            return None

        # for child in tree.getiterator(): formerly for Python 3.8
        for child in tree.iter():  # Python 3.10
            # print("child.tag: ",child.tag, type(child.tag))
            # print("child.attrib :", child.attrib) # dict
            # print("child.text :", child.text) #attrib
            # print("child.tail :", child.tail)
            if childTag in child.tag and attribTag_str in child.attrib.values():
                # print("\t[+] attribTag_str:",attribTag_str,"found.")
                # print("\t child.text:",child.text)
                try:
                    tmp_list.append(int(child.text))
                except ValueError:  # not an int
                    tmp_list.append(child.text)
        # 				print("extractTextFromElement1(): {} is type {}".format(child.text, type(child.text)))
        # 		print("extractTextFromElement1(): tmp_list is {} ".format(tmp_list))

        # print("\t extractTextFromElement1: returning {}",format(tmp_list))
        return tmp_list

    # end of extractTextFromElement1()

    # end of parserEngine()

    # The following code is obsolete but is left in the project for reference.
    # *******************************************************************************************************

    def old_getInformationOfKwInDocs(self):
        """A Method to locate the keywords in the document abstracts. If any keyword is found, return all details to program"""

        # console.print(f"self.abs_only : {self.abs_only}")
        # print("\n\t Searching abstract: {} \n".format(self.abstract_str))
        # Get the details of the current article; used later if keywords are found.
        docDetails_list = []

        self.title_str = self.getTitle()  # check to see whether the file is good
        # console.print(f"\t[bold red][TITLE]: {self.title_str}")

        if self.title_str != None:  # working title found?
            docDetails_list.append(self.title_str)

            # print("docDetails_list : {}".format(docDetails_list))

            # 14 July 2023: removed for save_less option.
            # dont want to save the entire abstract each time?
            self.abstract_str = self.getAbstract()

            if self.save_less != False:
                shortAbs_str = ""  # save a shorter version of abstract
                try:
                    shortAbs_str = self.abstract_str[
                        :myCHARSLIMIT
                    ]  # set above in globals
                except TypeError:
                    shortAbs_str = None
                # console.print(f"\t[bold red][ADD FULL ABSTRACT]: {shortAbs_str}")
                docDetails_list.append(shortAbs_str)

            else:  # save full abstract
                self.abstract_str = self.getAbstract()
                # console.print(f"\t[bold green][ADD FULL ABSTRACT]: {self.abstract_str}")
                docDetails_list.append(self.abstract_str)

            self.pmid_str = self.getPmid()
            # console.print(f"\t[bold red][PMID]: {self.pmid_str}")
            docDetails_list.append(self.pmid_str)

            self.journal_str = self.getJournal()
            # console.print(f"\t[bold red][JOURNAL]: {self.journal_str}")
            docDetails_list.append(self.journal_str)

            self.year_str = self.getYear()
            # console.print(f"\t[bold red][YEAR]: {self.year_str}")
            docDetails_list.append(self.year_str)

            self.ref_list = self.getReferences()
            # console.print(f"\t[bold red][REFERENCES]: {self.ref_list}")
            docDetails_list.append(self.ref_list)

            #######################
            # If the abstract contains a keyword, then keep the article details, otherwise ditch them.

            foundKeyWords_list = (
                []
            )  # contains keywords that were found in the current article

            for kw_str in self.keyword_list:
                # print("\t \U0001f5ff Searching keyword <{}> in abstract: \n".format(kw_str))
                printFlag = 0

                # TODO: are we processing the abstracts or the whole contents?

                searchabletext_str = (
                    ""  # variable to hold the text (abs or whole contents) to scan
                )

                # abstracts only
                if self.abs_only:  # checking only abstracts
                    try:
                        searchabletext_str = self.abstract_str
                    except Exception:
                        pass

                else:  # checking the whole article
                    searchabletext_str = self.contents_str

                # console.print(f"\t [bold red] length of text is : {len(searchabletext_str)}")

                try:
                    # if kw_str.lower() in self.abstract_str.lower():
                    if kw_str.lower() in searchabletext_str.lower():
                        foundKeyWords_list.append(kw_str)  # keep found word in a list
                        console.print(f"[bold yellow] found keyword: {kw_str}")

                except:  # general exception for badly formatted files.
                    # print(f"Error in file... skipping <{self.fileName_str}>")
                    pass

            wordCount_list = (
                []
            )  # keep track of how many counts of each word were found in abstract
            if (
                len(foundKeyWords_list) > 0
            ):  # is there at least one found word in the list?
                for w in foundKeyWords_list:
                    count = searchabletext_str.count(w)
                    # count = self.abstract_str.count(w)
                    wordCount_list.append(count)
                    # console.print(f"\t :rocket: [bold green] Found: {w}, {type(w)}")

                wordlistAs_str = ""  # a sting listing of the found keywords.

                for f in foundKeyWords_list:
                    wordlistAs_str = wordlistAs_str + str(f) + ","
                wordlistAs_str = wordlistAs_str[: len(wordlistAs_str) - 1]

                console.print(f"[bold purple] wordlistAs_str :{wordlistAs_str}")

                docDetails_list.append(wordlistAs_str)  # get the words in the abstract

                docDetails_list.append(
                    wordCount_list  # counts of the keywords themselves?
                )  # get the count of words in abstract

                return docDetails_list  # return the whole set of details and kw counts for this article
            else:
                return None

        else:
            pass
            # print("\t [-] Improper: <{}>".format(self.fileName_str))

    # end of old_getInformationOfKwInDocs()

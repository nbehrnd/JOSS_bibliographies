# name:    bibtool_Joss_bibtex.py
# author:  nbehrnd@yahoo.com
# date:    2019-07-08 (YYYY-MM-DD)
# edit:    2019-07-09 (YYYY-MM-DD)
""" bibTeX / ASCII report about publications accepted for JOSS

Each publication accepted by JOSS [1] is mirrored on [2] by a dedicated
folder, with an .html, .pdf, and .xml file.  It is possible to clone this
freely available.zip archive.  This script will retrieve some of the more
important bibliographic information from the .html files, and report this
into a bibTeX file .bib understood by many literature reference programs,
and may be imported easily e.g. by zotero.  It is expected to deposit this
script into the same folder as the .zip archive by [2], and to launch from
the command line by

python3 bibtool_Joss_bibtex.py joss-papers-master.zip

to yield report.bib and the less verbose semicolon separated report.csv,
suitable for either working with an editor or spreadsheet like gnumeric
or LibreOffice Calc.

The script is written for Python3; not only because Python2 is phasing
out, more importantly, because Python3 works better with unicode characters
which may be a particular problem while dealing with literature references
anyway.

[1] https://joss.theoj.org/
[2] https://github.com/openjournals/joss-papers

(c) Norwid Behrnd, 2019, GPGL v 3.
"""

import fnmatch
import os
import shutil
import sys
import zipfile

from bs4 import BeautifulSoup

global root
root = str(
    os.getcwd())  # directory hosting this script, archive .zip, and reports

article_register = []
pocket_register = []
report_csv = str("pocket_list.csv")
report_txt = str("pocket_list.txt")

try:
    if len(sys.argv[1]) > 1:
        used_archive = sys.argv[1]

except:
    print("")
    print("Expected use: python bibtool_JOSS_pocket.py archive.zip")
    print("Without change of any data, the script closes now.")
    print("")
    sys.exit()


def provide_clearance():
    """ remove possible traces of a previous run by this script """
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "pocket_list.*"):
            os.remove(file)
    try:
        shutil.rmtree("joss-papers-master")
    except:
        pass


def open_archive():
    """ retrieve the .html used for the data extraction """
    archive = zipfile.ZipFile(used_archive)
    content_list = archive.infolist()
    for content in content_list:
        if fnmatch.fnmatch(content.filename, "*.crossref.xml"):
            archive.extract(content.filename)
    archive.close()

    os.chdir("joss-papers-master")
    local = os.getcwd()

    for folderName, subfolders, filenames in os.walk(local):
        for subfolder in subfolders:
            os.chdir(subfolder)

            for file in os.listdir("."):
                if fnmatch.fnmatch(file, "*.crossref.xml"):
                    shutil.move(file, local)
            os.chdir(local)
            shutil.rmtree(subfolder)


def extract_data():
    """ extract just the brief descriptions of the articles """
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.crossref.xml"):
            article_register.append(file)
    article_register.sort()

    global bibtex_register
    bibtex_register = []

    global list_register
    list_register = []
    key = 1

    for article in article_register[:4]:
        stone = open(article)
        soup = BeautifulSoup(stone, "lxml")

        search_title = soup("titles")
        title = str(search_title[0].get_text())[1:].strip()
        print("title: {}".format(title))

        search_publication_doi = soup("doi")
        publication_doi = str(search_publication_doi[1].get_text()).strip()
        print("publication_doi: {}".format(publication_doi))

        search_pdf_url = soup("item")
        url = str(search_pdf_url[0].get_text())[1:].strip()
        print("url: {}".format(url))

        search_year = soup("year")
        year = str(search_year[0].get_text()).strip()
        print("year: {}".format(year))

        search_volume = soup("journal_volume")
        volume = str(search_volume[0].get_text())[1:].strip()
        print("volume: {}".format(volume))

        search_issue = soup("issue")
        issue = str(search_issue[0].get_text()).strip()
        print("issue: {}".format(issue))

        search_first_page = soup("first_page")
        pages = str(search_first_page[0].get_text()).strip()
        print("pages: {}".format(pages))

        search_authors_given_name = soup("given_name")
        search_authors_surname = soup("surname")
        author_register = []
        for given_name, surname in zip(search_authors_given_name,
                                       search_authors_surname):
            retain = str(given_name.get_text()) + str(" ") + str(surname.get_text())
            author_register.append(retain)

        print("author_register: {}".format(author_register))

#         retrieve the title of the publication, the first entry tagged by h1
#        tags = soup('h1')
#        title = str(tags[0].get_text())

#         retrieve the authors of the publication
#        author_list = soup.find('ul', attrs={'author-list'}).get_text()

#         a) preparation for list_authors:
#        list_authors = ""
#        for char in str(author_list)[1:-1]:
#            if char == str("\n"):
#                list_authors += str(", ")
#            else:
#                list_authors += str(char)

#         b) preparation for the bibTeX export
#        bibtex_authors = ""
#        for char in str(author_list)[1:-1]:
#            if char == str("\n"):
#                bibtex_authors += str(" and ")
#            else:
#                bibtex_authors += str(char)

#         retrieve the DOI of the publication (not the one for SI software)
#        doi = soup.find_all('span', attrs={'repo'})

#        list_doi = str(doi[-1].get_text())[4:]
#        bibtex_doi = str(list_doi)[16:]

#         retrieve volume and issue of the publication
#        pocket = soup.find('small').get_text()
#        volume_and_issue = pocket.split(", ")[2]

#         issue = str(pocket.split(", ")[2])
#        volume = str(pocket.split(", ")[2]).split("(")[0]

#         retrieve the starting page.
#        pages = str(pocket.split(" ")[-2])[:-1]

#         retrieve year of publication
#        testing = soup.find('small').get_text()
#        year = str(str(testing).split("(")[1])[:4]

#         retrieve the deposit of the .pdf
#         pdf_paper = str("https://joss.theoj.org/papers/") + \
#                     str(list_doi).split("/")[-1] + str("/") + \
#                     str("10.21105/") + str(list_doi).split("/")[-1] + \
#                     str(".pdf")

#         retrieve the rooting url about the publication
#        url = str("https://joss.theoj.org/papers/") + \
#              str(list_doi).split("/")[-1] + str("/") + \
#              str("10.21105/") + str(list_doi).split("/")[-1]

#         useful (constant) entries for literature referencers (e.g., zotero)
#        journal = str("Journal of Open Source Software")
#        ISSN = str("2475-9066")

#        bibtex_export = str('@article{') + str(key) + str(',\n') +\
#                        str('author = {') + str(bibtex_authors) + str('},\n') +\
#                        str('title = {') + str(title) + str('},\n') +\
#                        str('journal = {') + str(journal) + str('},\n') +\
#                        str('ISSN = {') + str(ISSN) + str('},\n') +\
#                        str('year = {') + str(year) + str('},\n') +\
#                        str('volume = {') + str(volume) + str('},\n') +\
#                        str('number = {') + str() + str('},\n') +\
#                        str('pages = {') + str(pages) + str('},\n') +\
#                        str('doi = {') + str(bibtex_doi) + str('},\n') +\
#                        str('url = {') + str(url) + str('},\n') +\
#                        str("}")
#        bibtex_register.append(bibtex_export)
#        print(bibtex_export)
#        print("")

#        list_export = str(key) + str(";") +\
#                      str(list_authors) + str(";") +\
#                      str(title) + str(";") +\
#                      str(year) + str(";") + str(volume) + str(";") +\
#                      str(pages) + str(";") + str(list_doi)
#        list_register.append(list_export)
#        key += 1


def reporting():
    """ generate the permanent record files """
    with open("report.bib", mode="w") as newfile:
        for entry in bibtex_register:
            output = str(entry) + str("\n\n")
            newfile.write(output)

    with open("report.txt", mode="w") as newfile:
        header = str("key") + str(";") + \
                 str("list_authors") + str(";") +\
                 str("title") + str(";") +\
                 str("year") + str(";") + str("volume") + str(";") +\
                 str("start page") + str(";") + str("list_doi")

        for entry in list_register:
            output = str(entry) + str("\n")
            newfile.write(output)


def space_cleaning():
    """ remove of no longer needed .html, move reporter files """
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "*.html"):
            os.remove(file)
        if fnmatch.fnmatch(file, "pocket_list.*"):
            shutil.move(file, root)

    os.chdir(root)
    shutil.rmtree("joss-papers-master")


# action calls
print("\nScript 'testing.py' started.")

provide_clearance()
open_archive()
extract_data()

# space_cleaning()
# reporting()
print("\nScript 'testing.py' completed its task and closes now.\n")
sys.exit()

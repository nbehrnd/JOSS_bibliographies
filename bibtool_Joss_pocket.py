# name:   bibtool_Joss_pocket.py
# author: nbehrnd@yahoo.com
# date:   2019-07-08 (YYYY-MM-DD)
# edit    2019-07-09 (YYYY-MM-DD)
""" provision of a short pocket list about accepted publications in JOSS

Accepted publications for JOSS [1] may be found mirrored on [2].  After
cloning the corresponding .zip archive into a local folder, this script
will readout the 'cite as' section provided for each of the publication
on its .html and provide this information both as a semicolon-separated
.csv file, as well as a (only linefeed separated) .txt as pocket_list.*

Written for the CLI of Python3 and to be called in the pattern of

python bibtool_Joss_pocket.py [joss-papers-master.zip]

with the cloned archive as sole -- and mandatory -- parameter.  Because
of the announced phasing-out of Python2, the script /does not/ consider
this legacy branch.  Indeed, the script will not work with Python2.

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
    print("Expected use: python bibtool_Joss_pocket.py archive.zip")
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
        if fnmatch.fnmatch(content.filename, "*.html"):
            archive.extract(content.filename)
    archive.close()

    os.chdir("joss-papers-master")
    local = os.getcwd()

    for folderName, subfolders, filenames in os.walk(local):
        for subfolder in subfolders:
            os.chdir(subfolder)

            for file in os.listdir("."):
                if fnmatch.fnmatch(file, "*.html"):
                    shutil.move(file, local)
            os.chdir(local)
            shutil.rmtree(subfolder)


def extract_data():
    """ extract just the brief descriptions of the articles """
    for file in os.listdir("."):
        if fnmatch.fnmatch(file, "10.21105.joss.*.html"):
            article_register.append(file)
    article_register.sort()

    for article in article_register:
        stone = open(article)

        soup = BeautifulSoup(stone, "lxml")

        pocket_entry = str(soup.find("small").get_text())

        pocket_register.append(pocket_entry)

    # report the data as semicolon separated .csv file, with counter
    counter = 1
    with open(report_csv, mode="w") as newfile:
        for entry in pocket_register:
            output = str("{}; {}\n".format(counter, entry))
            newfile.write(output)
            counter += 1

    # report the data as \n separated .txt file, no counter
    with open(report_txt, mode="w") as newfile:
        for entry in pocket_register:
            output = str("{}\n".format(entry))
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
print("\nScript 'bibtool_Joss_pocket.py' started.")

provide_clearance()
open_archive()
extract_data()
space_cleaning()

print("Script 'bibtool_Joss_pocket.py' completed its task and closes now.\n")
sys.exit()

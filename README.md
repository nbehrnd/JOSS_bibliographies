

# Background

Publications of the Journal of Open Source Software (JOSS<sup><a id="fnr.1" class="footref" href="#fn.1">1</a></sup>) are
equally available as `.html` and `.pdf`, altogether with their
corresponding `.xml` files, on a separate public repository<sup><a id="fnr.2" class="footref" href="#fn.2">2</a></sup>.
This not only offers an alternative access to the publications *at
once*, equally, it is possible to retrieve their bibliographic data
rapidly for further processing in literature reference programs like
zotero<sup><a id="fnr.3" class="footref" href="#fn.3">3</a></sup>


# Technique deployed

The uncompressed `.zip` archive is cloned onto a machine running
`Python3`.  The branch was chosen both because of the anticipated
retirement of `Python2`, as well for the better support of Unicode
characters.  Both scripts run from the CLI, and expect the `.zip`
archive in the same folder, e.g.

    python bibtool_Joss_pocket.pt joss-papers-master.zip

and currently will briefly extract the complete content of the
archive.  At present (2019-Jun-08), this requires about 0.3 to
0.4 GB freely accessible space on the hard disk.

The smaller script, `joss-papers-master.zip` retrieves the small
«cite as» block provided on each `.html` of the corresponding
publication, in either `.txt` or `.csv` format.  The larger
`bibtool_Joss_bibtex.py` attempts to retrieve *basic* bibliographic
information and creation of a bibtex file (`.bib`) understood by
many literature reference programs.  In addition, a less verbose
`.csv` (separator: semicolon) is created, offering futher processing
with any editor, or spreadsheet.

After running these scripts, the scripts leave you with the original
`.zip` archive (still containing the `.html` and `.pdf` about the
publications) and the extracted literature data.  Intermediate files
are deleted automatically.


# Copyright

(c) 2019 Norwid Behrnd, GPLv3.


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> <https://joss.theoj.org/>

<sup><a id="fn.2" href="#fnr.2">2</a></sup> <https://github.com/openjournals/joss-papers>

<sup><a id="fn.3" href="#fnr.3">3</a></sup> [http://www.zotero.org](http://www.zotero.org)

#!/usr/bin/env python3

################################################################### 
###  title    : NexusTree2Newick.py                             ###
###  author	  : Holly Ruess (Holly.Ruess@ars.usda.gov)          ###
###  date     : 02-28-2018                                      ###
###  version  : 1                                               ###
###  usage    : ./NexusTree2Newick.py input.tree >output.newick ###
###  reference: https://github.com/HollyRuess/                  ###
###################################################################

### This python 3 program converts the *.tree file from SVDQuartets 
###     (PAUP) to newick file that is readable by figtree.

import fileinput
import re

dictionary = {}
for line in fileinput.input():
    newick = line.rstrip("\n")
    # Find the line containing the data.
    data = re.search('^tree \'PAUP_1\' = \[&U\] (.*)', newick)
    if data:
        founddata = data.group(1)

    # Create a dictionary of the sample name number and sample name.
    if re.match('^\t\t\d+', newick):
        names = newick.replace('\t\t', '').replace(',', '').split()
        dictionary[names[0]] = names[1]

# Replace the number in the data line with the sample name.
for i, j in dictionary.items():
    founddata = founddata.replace("," + i + ":", "," + j + ":", 1) \
                         .replace("(" + i + ":", "(" + j + ":", 1)
print(founddata)

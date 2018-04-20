#! /usr/bin/env python3

###############################################################
###  title    : haplotype_count.py                          ###
###  author	  : Holly Ruess (Holly.Ruess@ars.usda.gov)      ###
###  date     : 04-20-2018                                  ###
###  version  : 1                                           ###
###  usage    : ./haplotype_count.py input.vcf >count.txt   ###
###  reference: https://github.com/HollyRuess/              ###
###############################################################

### This python3 program counts the number of times each haplotype
###    appears in vcf file (per accession). Haplotypes are ./., 0/0,
###    0/1, 1/0, 1/1, or other.
### VCF file can be compressed or uncompressed.

import gzip
import sys
import re


def openfile(filename, mode ='r'):
    """Check if file is compressed; open base on compression"""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'r')

def caculations(inputdata, inputheader):
    """Count the number of each haplotype and print results"""
    countmiss = inputdata.count('./.')
    count00 = inputdata.count('0/0')
    count01 = inputdata.count('0/1')
    count10 = inputdata.count('1/0')
    count11 = inputdata.count('1/1')
    countother = (len(inputdata) - int(countmiss) - int(count00) - 
                  int(count01) - int(count10) - int(count11))
    print(str(inputheader) + "\t" + str(countmiss) + "\t" + 
          str(count00) + "\t" + str(count01) + "\t" + 
          str(count10) + "\t" + str(count11) + "\t" + 
          str(countother))


# Main Body of script
columns = []
for line in openfile(sys.argv[1]):
    if not re.match('^##', line):
        # Process the header line
        if re.match('^#', line):
            hdrcol = line.rstrip("\n").split("\t")[9:]
            for i in range(0,len(hdrcol)):
                columns.append([])
        # Process the data lines.
        else:
            datacol = line.rstrip("\n").split("\t")[9:]
            for i,element in enumerate(datacol):
                splitcol = element.split(":")[0]
                columns[i].append(splitcol)

# Process each column (accession)
print("PI\t./.\t0/0\t0/1\t1/0\t1/1\tother")
for x in range(0,len(hdrcol)):
    caculations(columns[x],hdrcol[x])

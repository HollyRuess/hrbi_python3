#! /usr/bin/env python3

###############################################################
###  title    : SNPcoverage.py                              ###
###  author	  : Holly Ruess (Holly.Ruess@ars.usda.gov)      ###
###  date     : 02-28-2018                                  ###
###  version  : 1                                           ###
###  usage    : ./SNPcoverage.py input.vcf >SNPcoverage.txt ###
###  reference: https://github.com/HollyRuess/              ###
###############################################################

### This python3 program finds the average coverage of the SNPs for
###     each accession (minus missing data) in a vcf file
### VCF file can be compressed or uncompressed.

import gzip
import sys
import re
import statistics


def openfile(filename, mode ='r'):
    """Check if file is compressed; open base on compression"""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'r')


def caculations(inputdata, inputheader):
    """Calculate min, max, mean, and median of SNPs per accession"""
    sortcol = sorted(inputdata)
    minimaldata = min(sortcol)
    maximumdata = max(sortcol)
    meandata = statistics.mean(sortcol)
    mediandata = statistics.median(sortcol)
    countdata = len(sortcol)

    print(str(inputheader) + "\t" + str(minimaldata) + "\t" +
          str(maximumdata) + "\t" + str("%.2f" % meandata) + "\t" +
          str(mediandata) + "\t" + str(countdata))


# Main Body of script
coveragecol = []
for line in openfile(sys.argv[1]):
    if not re.match('^##', line):
        # Process the header line
        if re.match('^#', line):
            hdrcol = line.rstrip("\n").split("\t")[9:]
            for i in range(0,len(hdrcol)):
                coveragecol.append([])
        # Process the data lines. Third division of column is coverage
        else:
            datacol = line.rstrip("\n").split("\t")[9:]
            for i,element in enumerate(datacol):
                if not re.match('^\.\/\.', element):
                    splitcol = int(element.split(":")[2])
                    coveragecol[i].append(splitcol)

# Process each column (accession), and calculate statistics
print("Name\tMin\tMax\tAverage\tMedian\tCount")
for x in range(0,len(hdrcol)):
    caculations(coveragecol[x],hdrcol[x])

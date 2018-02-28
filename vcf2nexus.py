#! /usr/bin/env python3

########################################################## 
###  title    : vcf2nexus.py                           ###
###  author   : Holly Ruess (Holly.Ruess@ars.usda.gov) ###
###  date     : 02-28-2018                             ###
###  version  : 1                                      ###
###  usage    : ./vcf2nexus.py  input.vcf >output.nex  ###
###  reference: https://github.com/HollyRuess/         ###
##########################################################

### This python3 program converts a compressed or uncompressed vcf file
###     to a nexus file for PAUP analysis

import gzip
import sys
import re


def openfile(filename, mode ='r'):
    """Check if file is compressed; open base on compression"""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'r')


def heterozygous_snps(reference, alternate):
    """If the allele is heterozygous, place an ambiguity call"""
    if re.match('A', reference) or re.match('A', alternate):
        if re.match('T', reference) or re.match('T', alternate):
            return("W")
        elif re.match('C', reference) or re.match('C', alternate):
            return("M")
        elif re.match('G', reference) or re.match('G', alternate):
            return("R")
    elif re.match('T', reference) or re.match('T', alternate):
        if re.match('C', reference) or re.match('C', alternate):
            return("Y")
        elif re.match('G', reference) or re.match('G', alternate):
            return("K")
    elif re.match('C', reference) or re.match('C', alternate):
        if re.match('G', reference) or re.match('G', alternate):
            return("S")
    else:
        sys.exit('Bases other than ATCG found in file')


allelecol = []
count=0
for line in openfile(sys.argv[1]):
    if not re.match('^##', line):
        if re.match('^#', line):
            hdrcol = line.rstrip("\n").split("\t")[9:]
            for i in range(0,len(hdrcol)):
                allelecol.append([])
        else:
            count += 1
            datacol = line.rstrip("\n").split("\t")
            for i,element in enumerate(datacol[9:]):
                if re.match('^0\/0', element):
                    allelecol[i].append(datacol[3])
                elif re.match('^1\/1', element):
                    allelecol[i].append(datacol[4])
                elif re.match('^\.\/\.', element):
                    allelecol[i].append("?")
                elif (re.match('^0\/1', element) or 
                    re.match('^1\/0', element)):
                    allelecol[i].append(
                                 heterozygous_snps(datacol[3],datacol[4]))
                else:
                    sys.exit('ERROR: vcf file contains alleles other \
                              than 0/0, 0/1, 1/0, 1/1')

j=""
print("#NEXUS\nBegin data;\nDimensions ntax=" + str(len(hdrcol)) + 
      " nchar=" + str(count) + 
      ";\nFormat datatype=dna missing=? gap=-;\nMatrix\n")

for x in range(0,len(hdrcol)):
    print(hdrcol[x] + "     " + j.join(allelecol[x]))

print(";\nEND;")

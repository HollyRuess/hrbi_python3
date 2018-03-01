#! /usr/bin/env python3

####################################################################################### 
###  title    : vcf2STRUCTURE_reorder.py                                            ###
###  author   : Holly Ruess (Holly.Ruess@ars.usda.gov)                              ###
###  date     : 03-01-2018                                                          ###
###  version  : 1                                                                   ###
###  usage    : ./vcf2STRUCTURE_reorder.py input.vcf <input_order.txt> >output.str  ###
###  reference: https://github.com/HollyRuess/                                      ###
#######################################################################################

# This python3 program converts a vcf file (created by tassel5 and 
#  filtered by vcftools) into a Structure format (STRUCTURE 2 line 
#  format, A=1,C=2,G=3,T=4,missing=-9). 
# vcf can be compressed.
# Reorder file is optional, and is a list of accessions from the 
#  (#CHROM line in the vcf file) in the order that you want the
#  structure output in (i.e. tree order, group order, etc.).

import gzip
import sys
import re


def openfile(filename, mode ='r'):
    """Check if file is compressed; open base on compression"""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'r')


def structure_code(base):
    """Change the nucleotide base into structre number code"""
    if re.match('A', base):
        return("1")
    elif re.match('C', base):
        return("2")
    elif re.match('G', base):
        return("3")
    elif re.match('T', base):
        return("4")
    else:
        sys.exit('Bases other than ATCG. found in file')


alleleA = []
alleleB = []
for line in openfile(sys.argv[1]):
    if not re.match('^##', line):
        if re.match('^#', line):
            hdrcol = line.rstrip("\n").split("\t")[9:]
            for i in range(0,len(hdrcol)):
                alleleA.append([])
                alleleB.append([])
        else:
            datacol = line.rstrip("\n").split("\t")
            for i,element in enumerate(datacol[9:]):
                if re.match('^0\/0', element):
                    alleleA[i].append(structure_code(datacol[3]))
                    alleleB[i].append(structure_code(datacol[3]))
                elif re.match('^1\/1', element):
                    alleleA[i].append(structure_code(datacol[4]))
                    alleleB[i].append(structure_code(datacol[4]))
                elif re.match('^\.\/\.', element):
                    alleleA[i].append("-9")
                    alleleB[i].append("-9")
                elif re.match('^0\/1', element):
                    alleleA[i].append(structure_code(datacol[3]))
                    alleleB[i].append(structure_code(datacol[4]))                   
                elif re.match('^1\/0', element):
                    alleleA[i].append(structure_code(datacol[4]))
                    alleleB[i].append(structure_code(datacol[3]))
                else:
                    sys.exit('ERROR: vcf file contains alleles other \
                              than 0/0, 0/1, 1/0, 1/1, ./.')

j="\t"
if len(sys.argv) == 3: # Check if reorder file is given.
    for line in open(sys.argv[2], 'r'):
        output_order = line.rstrip("\n")
        for x in range(0,len(hdrcol)):
            if (output_order == hdrcol[x]):
                print(hdrcol[x] + "\t.\t.\t.\t.\t.\t" + j.join(alleleA[x]))
                print(hdrcol[x] + "\t.\t.\t.\t.\t.\t" + j.join(alleleB[x]))
else:
    for x in range(0,len(hdrcol)):
        print(hdrcol[x] + "\t.\t.\t.\t.\t.\t" + j.join(alleleA[x]))
        print(hdrcol[x] + "\t.\t.\t.\t.\t.\t" + j.join(alleleB[x]))

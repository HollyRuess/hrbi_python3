#!/usr/bin/env python3

###########################################################
###  title    : SNPfilter4ML.py                         ###
###  author   : Holly Ruess (Holly.Ruess@ars.usda.gov)  ###
###  date     : 02-28-2018                              ###
###  version  : 1                                       ###
###  usage    : ./SNPfilter4ML.py input.vcf >output.vcf ###
###  reference: https://github.com/HollyRuess/          ###
###########################################################

### This python3 program filters a vcf file of SNPs.
### VCF file can be compressed or uncompressed.
### Output is uncompressed; compress by adding " | bgzip >output.vcf.gz"
### Used for the ascertainment bias of Maximum Likelihood (RAxML).
### There are 2 filters:
### 1)at least 1 homozygous reference SNP, atleast 1 homozygous 
###    alternate SNP, an at least and 1 heterozygous SNP
### 2)if no heterozygous SNPs, then at least 2 homozygous reference 
###    SNPs and 2, homozygous alternate SNPs

import gzip
import sys
import re


def openfile(filename, mode='r'):
    """Check if file is compressed; open based on compression."""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'r')


###Main body
for line in openfile(sys.argv[1]):
    data = line.rstrip()
    if re.match('^#', data):
        print(data)
    elif (re.search(r'0/1', data) and
          re.search(r'1/1', data) and
          re.search(r'0/0', data)):
        print(data)
    elif (not re.search(r'0/1', data) and
              re.search('0\/0.*0\/0', data) and
              re.search('1\/1.*1\/1', data)):
        print(data)

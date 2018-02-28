# hrbi_python3

Python3 programs developed as bioinformatics tools.

# vcf2nexus.py
This python3 program converts a vcf file (created by tassel5 and filtered by vcftools) into a NEXUS file. The vcf file can be 
compressed. Missing data is coded as "?".

# SNPfilter4ML.py
This python3 program filters a vcf file of SNPs so that the ascertainment bias of Maximum Likelihood may be applied. The 
filters are either 1) at least 1 homozygous reference SNP, at least 1 homozygous alternate SNP, and at least and 1 
heterozygous SNP, 2) if no heterozygous SNPs, then at least 2 homozygous reference SNPs and 2 homozygous alternate SNPs.

# SNPcoverage.py
This python3 program finds the average coverage of the SNPs for each accession (minus missing data) in a vcf file.

# NexusTree2Newick.py
This python 3 program converts the *.tree file from SVDQuartets (PAUP) to newick file that is readable by figtree.

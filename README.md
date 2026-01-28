This repository contains the coding and data files needed to accompany the manuscript: 

 # Using Environmental DNA (eDNA) and land cover usage to assess fish communities in southwest Ohio
 Authors: Isabella Leisgang and Kenneth Petren 

Data: 

Linux script: 

R script: 
## Dependencies
This pipeline makes use of the following programs: 
1. cutadapt (https://cutadapt.readthedocs.io/en/stable/index.html)
2. vsearch (https://github.com/torognes/vsearch)
3. fastqc (https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
Cutadapt and vsearch must be installed locally. The desktop of fastqc was used to inspect fastq.gz files. This pipeline has only been conducted in a Linux environment (Ubuntu). 
## Usage
The pipeline.py file contains a single script to trim primers and adapters, filter sequences, remove poly-A tails, decompress fast.gz files for vsearch, merge R1 and R2 files, filter post merge, cluster sequences, detect chimeras, and align with a reference database. This pipeline was carried out by opening the .py file and editing as a text file.

For each step, the input_dir and output_dir must be changed to the proper file locations. It is reccomended that an output folder for each step is created, so that each step of the pipeline can be checked if needed.

The reference database must be saved as a fasta file and the location must be written for the query_files_dir. The alignment step will also save the alignment results as a csv file for each sequence wwell/ sample. The R scripts will then be used to combine and organize all of the alignment files into one sheet with the number of reads for each taxa for each sample. 

The filter_species.py file will be used to gather query sequences for certain aligned species for a secondary BLAST alignment. When pulling query sequences for certain species, their reference database code and scientific name will be need to be input into the reference_mapping = {} brackets in the following format: 
    "12sDB_00036962": "Notropis heterolepis",
    "12sDB_00035836": "Catostomus catostomus",
    "12sDB_00036061": "Cyprinus acutidorsalis",
The current filter_species.py script contains these taxa as an example in the reference_mapping brackets. 


-----------------------------------Trim/Filter/Removing poly-A tails---------------------

		To Trim AND filter a folder worth of trimmed reads


This code would be ran to produce summary text files after the code is ran 
#!/bin/bash
input_folder="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/0Raw Sequences/16s"
output_folder="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/1TrimFilter/16s"

# Iterate over all R1 files in the input folder
for file_R1 in "${input_folder}"/*_R1.fastq.gz; do
    file_R2="${file_R1/_R1/_R2}"
    output_file=$(basename "${file_R1}" _R1.fastq.gz)

    # Run cutadapt for each pair of files and save the summary output
    cutadapt -g GTGCCAGCMGCCGCGGTAA -G 	GGACTACHVGGGTWTCTAAT  \
    -o "${output_folder}/${output_file}.trimmed_R1.fastq.gz" \
    -p "${output_folder}/${output_file}.trimmed_R2.fastq.gz" \
    -e 0.25 \
    "${file_R1}" "${file_R2}" > "${output_folder}/${output_file}_summary.txt"

done
-------------------Decompressing fastq.gz----------------------------------
When starting to use VSEARCH, the GZ files must first be decompressed 

#!/bin/bash

# Define input and output directories
input_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/1.5NexteraTrim/16s"
output_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/1.5NexteraTrim/16s"

# Ensure output directory exists
mkdir -p "$output_dir"

# Process each .fastq.gz file
for gz_file in "$input_dir"/*.fastq.gz; do
    # Check if files exist before processing
    if [[ -f "$gz_file" ]]; then
        output_file="$output_dir/$(basename "$gz_file" .gz)"
        echo "Uncompressing: $gz_file -> $output_file"
        gunzip -c "$gz_file" > "$output_file"
    else
        echo "Warning: No .fastq.gz files found in $input_dir"
    fi
done
--------------------------------Merge-------------------------------------------
To merge a bulk amount of files w/ summary txt file 


input_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/1.5NexteraTrim/16s"
output_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/2Merge/16s"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate over all R1 files in the input directory
for R1_file in "$input_dir"/*_R1.fastq; do
    # Construct the corresponding R2 file name
    R2_file="${R1_file/_R1.fastq/_R2.fastq}"

    # Extract the sample name from the R1 file
    sample_name=$(basename -- "$R1_file" | cut -d "_" -f 1-2)

    # Perform the merging using vsearch and create a summary file
    vsearch --fastq_mergepairs "$R1_file" \
            --reverse "$R2_file" \
            --fastqout "$output_dir/${sample_name}_merged.fastq" \
            --fastq_allowmergestagger \
            --label_suffix _merged \
            --log "$output_dir/${sample_name}_log.txt" \
            > "$output_dir/${sample_name}_summary.txt" 2>&1

    echo "Merged file: ${sample_name}_merged.fastq"
done

--------------------------Filtering post Merge-----------------------------------------------------
To filter bulk amount of files with specific error rates and lengths


#!/bin/bash

# Set the input and output directories
input_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/2Merge/16s"
output_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/3MClean/16s"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate over all merged files in the input directory
for file in "$input_dir"/*.fastq; do
    # Extract the filename without the extension
    filename=$(basename -- "$file")
    filename_noext="${filename%.*}"

    # Perform the filtering using vsearch
    vsearch --fastq_filter "$file" \
        --fastaout "$output_dir/${filename_noext}_filtered.fasta" \
        --fastq_minlen 110 \
        --fastq_maxlen 400 \
        --log "$output_dir/${filename_noext}_log.txt"

    echo "Filtered file: ${filename_noext}_filtered.fasta"
done

-----------------------------Clustering-----------------------------------
#!/bin/bash

# Input and output directories
input_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/3MClean/16s"
output_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/4Cluster/16s"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

for file in "$input_dir"/*.fasta; do

    filename=$(basename -- "$file")
    filename_noext="${filename%.*}"

    # Perform clustering with vsearch
    vsearch --cluster_unoise "$file" \
        --centroids "$output_dir/${filename_noext}_centroids.fasta" \
        --unoise_alpha 5 \
        --minsize 1 \
        --log "$output_dir/${filename_noext}_log.txt"

    echo "Clustered file: ${filename_noext}_centroids.fasta"
done

-----------------------------Chimera Detection--------------------------------------

		Chimera detection for a bulk amount of files: 

input_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/4Cluster/16s"
output_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/5ChimeraDetection/16s"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

for file in "$input_dir"/*.fasta; do
    filename=$(basename -- "$file")
    filename_noext="${filename%.*}"
 
    output_file="$output_dir/${filename_noext}_detected.fasta"

    vsearch --uchime3_denovo "$file" --uchimeout "$output_file" \
	    --log "$output_dir/${filename_noext}_log.txt" 

    echo "Chimera Detection: $output_file"
done

------------------------------------Pairwise Alignment---------------------------------------***** Use this one 
Using semi-pairwise global alignment to pair reference sequence file with existing seqeunces as .csv


reference_database="/mnt/c/Users/izzyl/Cornell Sequencing Data/Reference Libraries/SILVA/silva_nr99_v138_wSpecies_train_set.fasta"
output_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/Alignment results/16s"
query_files_dir="/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/4Cluster/16s"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

for query_file in "$query_files_dir"/*.fasta; do
    query_filename=$(basename -- "$query_file")  

    query_filename_noext="${query_filename%.*}"

    # Correct the --blast6out path and the --log path
    vsearch --usearch_global "$query_file" --db "$reference_database" --id 0.97 \
    --blast6out "$output_dir/${query_filename_noext}_alignment_results.csv" \
    --log "$output_dir/${query_filename_noext}_log.txt"
done




###Use this code to gather query sequences for certain aligned species

from Bio import SeqIO
import os
import csv

# Set the directory containing both CSV and FASTA files
alignment_dir = "/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Izzy/Alignment results "
output_fasta = "/mnt/c/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/matched_with_species.fasta"

# Reference mapping
reference_mapping = {
    "12sDB_00036962": "Notropis heterolepis",
    "12sDB_00035836": "Catostomus catostomus",
    "12sDB_00036061": "Cyprinus acutidorsalis",
    # Add additional mappings as needed
}

# Step 1: Parse CSVs to build mapping from query ID to species
query_to_species = {}
print("Processing alignment files...\n")

for csv_file in os.listdir(alignment_dir):
    if csv_file.endswith("_alignment_results.csv"):
        csv_path = os.path.join(alignment_dir, csv_file)
        with open(csv_path, "r") as csv_handle:
            csv_reader = csv.reader(csv_handle, delimiter="\t")
            for row in csv_reader:
                if len(row) < 2:
                    continue  # Skip malformed rows
                query_id = row[0].strip()
                reference_id = row[1].strip()
                if reference_id in reference_mapping:
                    species_name = reference_mapping[reference_id]
                    query_to_species[query_id] = species_name

print(f"Found {len(query_to_species)} sequences matching specified species.")

# Step 2: Extract matching sequences from FASTA files
extracted_sequences = 0
with open(output_fasta, "w") as output_handle:
    for fasta_file in os.listdir(alignment_dir):
        if fasta_file.endswith("_matched_sequences.fasta"):
            fasta_path = os.path.join(alignment_dir, fasta_file)
            for record in SeqIO.parse(fasta_path, "fasta"):
                if record.id in query_to_species:
                    record.description += f" | Species: {query_to_species[record.id]}"
                    SeqIO.write(record, output_handle, "fasta")
                    extracted_sequences += 1

print(f"Extracted {extracted_sequences} sequences for specified species. Results written to {output_fasta}.")

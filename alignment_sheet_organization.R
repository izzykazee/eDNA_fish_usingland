#Make sure folder paths and are set to correct folder locations!
#Make sure column names are properly labeled with what exists in your excel files. blast6out-- should output csv files with the same column titles. 
I reccomend running each step one at a time and not running the entire script at once.


#(1)Code for column separation for multiple files in a folder
#First give the column a heading 
folder_path<- 'C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Stream Group/Alignment results/16s'
file_list<- list.files(folder_path, pattern = '.csv', full.names = TRUE)
print(file_list)
for (file_path in file_list){
  df<- read.csv(file_path)
  colnames(df)<- c("Query Label")
  output_path<- sub('.csv$', '_modified.csv', file_path)
  write.csv(df, file = output_path, row.names = FALSE)
}
#(2)Now we will separate the given column into multiple labeled columns 

# Define the folder path and get the list of files
library(tidyr)
library(dplyr)
folder_path <- 'C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Izzy/Alignment results/'
file_list <- list.files(folder_path, pattern = '_modified.csv', full.names = TRUE)

# Loop over the file list
for (file_path in file_list) {
  df <- read.csv(file_path, header = TRUE)
  
  # Display the column names for checking
  cat("Columns in", file_path, ":\n")
  print(names(df))
  
  # Check if the "Query.Label" column exists (case-insensitive)
  if ("Query.Label" %in% names(df)) {
    
    # Separate the "Query.Label" column into multiple columns
    df <- separate(df, col = "Query.Label", 
                   into = c("Query Label", "Target ID", "Percent match", "Alignment length", "Mismatch", "Gap Open", 
                            "Query start", "Query end", "Target start position", "Target end position", "E-value", "Bit score"), 
                   sep = "\t")
    
    # Save the modified data frame back to a CSV file with a new name
    output_path <- sub('_modified.csv$', '_separated.csv', file_path)
    write.csv(df, file = output_path, row.names = FALSE)
    
    cat("Processed and saved:", output_path, "\n")
    
  } else {
    # If "Query.Label" column not found, print an error message
    cat("Error: 'Query Label' column not found in", file_path, "\n")
  }
}


########
#(3)This code is going to add a new column "Well" and list the well code from each file name
library(dplyr)
folder_path <- "C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Alignment results"
file_list <- list.files(folder_path, pattern = '_separated.csv', full.names = TRUE)
output_folder <- "C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Alignment results"
dir.create(output_folder, showWarnings = FALSE)
for (file_path in file_list){
  df<- read.csv(file_path, header = TRUE)
  well<- gsub("Plate_|_alignment_results_separated.csv","", basename(file_path))
  df<- mutate(df, Well = well)
  output_file_path <- file.path(output_folder, paste0(well, "_modified.csv"))
  write.csv(df, file = file_path, row.names = FALSE)
}

###(4)This code adds on the database information to each spreadsheet
# Load the taxonomy data
library(dplyr)

folder_path <- "C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Izzy/Alignment results"
file_list <- list.files(folder_path, pattern = '_separated.csv', full.names = TRUE)

for (file_path in file_list) {
  df <- read.csv(file_path, header = TRUE)
  
  # Ensure column names are formatted correctly
  colnames(df) <- gsub(" ", ".", colnames(df))
  
  # Merge taxonomy data based on the Target.ID column
  df_merged <- merge(df, taxonomy_df, by.x = "Target.ID", by.y = "Code_12sDB", all.x = TRUE)
  
  # Save the updated file with taxonomic data added
  write.csv(df_merged, file = file_path, row.names = FALSE)
  
  cat("Updated taxonomy info added to:", file_path, "\n")
}

######(5)This code is going to merge all of the spreadsheets in the folder together
#Since it will create a file so large, we will omit some unimportant columns
  library(dplyr)
  
  folder_path <- "C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Izzy/Alignment results"
  file_list <- list.files(folder_path, pattern = '_separated.csv', full.names = TRUE)
  
  merged_data <- data.frame()
  
  for (file_path in file_list) {
    df <- read.csv(file_path, header = TRUE)
    
    # Replace spaces with dots in column names to avoid naming issues
    colnames(df) <- gsub(" ", ".", colnames(df))
    
    # Debug: Print column names to see what exists
    cat("\nProcessing file:", file_path, "\n")
    print(names(df))
    
    # ✅ Select only columns that actually exist in the file
    available_columns <- intersect(names(df), c("Target.ID", "Query.Label", "Percent.match", 
                                                "Phylum", "class", "Order", "Family", 
                                                "Genus", "Scientific.name.GnSP", "Full.name"))
    
    if (length(available_columns) == 0) {
      cat("Skipping", file_path, "- No matching columns found\n")
      next  # Skip this file if no valid columns exist
    }
    
    df_subset <- df %>% select(all_of(available_columns))
    
    # Extract well code from filename
    well <- gsub("_alignment_results_modified_merged.csv", "", basename(file_path))
    df_subset <- mutate(df_subset, Well = well)
    
    # Debugging: Print dimensions before merging
    print(paste("File:", file_path, "Dimensions before merging:", dim(df_subset)))
    
    merged_data <- bind_rows(merged_data, df_subset)
  }
  
  # Debug: Print final merged dimensions
  cat("\nFinal Merged Data Dimensions:\n")
  print(dim(merged_data))
  
  # Save merged data
  write.csv(merged_data, file = "C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/izzy/Alignment results/All_Merged_Sheets.csv", row.names = FALSE)
  

###########(6)This code segregates each location into its own column and counts and summarizes everything else

# Read the merged data
merged_data <- read.csv("C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/Izzy/Alignment results/All_Merged_Sheets.csv", header = TRUE)
# Group by Well, Percent.Match, Target.ID, and other columns, then count occurrences
summarized_data <- merged_data %>%
        group_by(Well, Phylum, class, Order, Family, Genus, Scientific.name.GnSP, Full.name) %>%
       summarise(Count = n()) %>%
       ungroup()
print(unique(merged_data$Well))
# Pivot the data
wide_data <- pivot_wider(
  data = summarized_data,
  names_from = "Well",
  values_from = "Count",
  values_fill = 0
  )
# Write the wide data to CSV
write.csv(wide_data, file = "C:/Users/izzyl/Cornell Sequencing Data/2025 UER and Adam/izzy/Alignment results/Final_FishSheet_No_PM.csv", row.names = FALSE)



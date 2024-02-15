import csv
import os

# Script to split all verilog files from Huggingface database. Modify local parameters 
# accordingly to parse correct CSV and download results to desired folder. 

#========================================================================
# LOCAL PARAMETERS
#========================================================================

CSV_FILE = 'Verilog_bigquery_GitHub.csv'                  # Replace with your CSV file path
output_dir = 'output_files'                               # Replace with your desired output directory


os.makedirs(output_dir, exist_ok=True)                    # Create the output directory if it doesn't exist
csv.field_size_limit(1000000000)

file_counter = 1


with open(CSV_FILE, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:                                                                   # Ensure the row is not empty
            cell_value = row[0]
            text_file_path = os.path.join(output_dir, f"file{file_counter}.v")    # Create a text file with a numbered filename 

            with open(text_file_path, 'w') as text_file:                          # Write the cell value to the text file
                text_file.write(cell_value)

            file_counter += 1

print("Text files have been created in the output directory with numbered names.")
print("Total extracted files: " + str(file_counter))

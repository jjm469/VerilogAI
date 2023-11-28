import csv
import os

# Define the CSV file path and the directory to save the text files
csv_file = 'Verilog_bigquery_GitHub.csv'  # Replace with your CSV file path
output_dir = 'output_files'  # Replace with your desired output directory

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

csv.field_size_limit(1000000000)  # Adjust as needed based on your data

# Initialize a counter
file_counter = 1

# Open the CSV file and process it
with open(csv_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:  # Ensure the row is not empty
            # Extract the cell value from the first column
            cell_value = row[0]

            # Create a text file with a numbered filename
            text_file_path = os.path.join(output_dir, f"file{file_counter}.v")

            # Write the cell value to the text file
            with open(text_file_path, 'w') as text_file:
                text_file.write(cell_value)

            file_counter += 1  # Increment the counter for the next file

print("Text files have been created in the output directory with numbered names.")
print("Total extracted files: " + str(file_counter))

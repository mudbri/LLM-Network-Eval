# In sources type, I did not individually write types for all sources if they were common. For example, if there were three wikipedia links, I would write wikipedia in the types only once. This script fixes that.

import os
import csv
import sys

def correct_csv_files(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return

    # Get list of CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    for file_name in csv_files:
        file_path = os.path.join(folder_path, file_name)
        temp_file_path = os.path.join(folder_path, "temp_" + file_name)

        # Create directory for temporary file if it doesn't exist
        temp_dir = os.path.dirname(temp_file_path)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        with open(file_path, 'r', newline='') as csvfile, open(temp_file_path, 'w', newline='') as temp_csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(temp_csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                new_source_types = []
                if row.get('Source links work(number)') == "":
                    writer.writerow(row)
                    continue
                num_links = int(row.get('Source links work(number)', 0))
                num_source_types = len(row.get('Sources Types', '').split(','))
                source_types = row.get('Sources Types', '')

                if num_source_types != num_links:
                    if num_source_types == 1:
                        for i in range(num_links):
                            new_source_types.append(source_types)
                        row['Sources Types'] = ", ".join(new_source_types)
                    else:
                        print(file_path)
                        print(row.get('Question Number'))
                        print()
                writer.writerow(row)

        # Replace the original file with the corrected one
        os.replace(temp_file_path, file_path)

if __name__ == "__main__":
    # Check if folder path is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    correct_csv_files(folder_path)
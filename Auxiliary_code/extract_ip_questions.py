import csv
import os
import sys
import re
import socket

def valid_ip(address):
    if "." in address and (len(address.split(".")) == 4):
        if address.split(".")[0].isdigit():
            return True
    return False

def is_ip_address(text):
    for word in text.split(" "):
        if valid_ip(word):
            return True
    return False

def extract_rows_with_ip(input_folder, output_file):
    # List all files in the input folder
    files = os.listdir(input_folder)
    # Open output file in write mode
    with open(output_file, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        header_written = False
        # Iterate through each CSV file in the folder
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(input_folder, file_name)
                with open(file_path, 'r', newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    # Write header if not already written
                    if not header_written:
                        writer.writerow(reader.fieldnames)
                        header_written = True
                    # Check if 'Question Text' or 'Choices' contain an IP address
                    for row in reader:
                        if is_ip_address(row.get('Question Text', '')) or is_ip_address(row.get('Choices', '')):
                            writer.writerow(row.values())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_file>")
    else:
        input_folder = sys.argv[1]
        output_file = sys.argv[2]
        extract_rows_with_ip(input_folder, output_file)
        print("Extraction complete. Rows with IP addresses saved to", output_file)

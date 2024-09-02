# This code is used to make sure we have analyzed all wrong answers
import csv
import os
import sys

def check_csv_file(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Correct?"] == "0" and row["QD - Goal clear?(0/1)"] == "":
                return True
    return False

def main(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            if check_csv_file(os.path.join(folder_path, filename)):
                print(filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py folder_path")
        sys.exit(1)
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("Error: Input path is not a directory.")
        sys.exit(1)
    main(folder_path)

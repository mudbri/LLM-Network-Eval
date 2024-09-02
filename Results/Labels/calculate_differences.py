import os
import csv
import sys

categories_to_ignore = ["LLM Confidence", "SM - Description", "logprob Confidence", "SM - Misunderstanding General (secondary)", "SM - Misunderstanding Reasons (secondary)", "Source links work(number)", "Sources Types", "Sources Relevant(number)", "Effect - Subtopics", "Score-right-minus-wrong", "CD - correction knowledgeable(1-8)", "CD - detection knowledgeable(1-3)", "CD - correction student(1-8)"]
def compare_csv_files(folder1, folder2, output_file):
    # Get list of files in both folders
    files1 = {f for f in os.listdir(folder1) if f.endswith('.csv')}
    files2 = {f for f in os.listdir(folder2) if f.endswith('.csv')}

    # Find common files between the two folders
    common_files = files1.intersection(files2)

    with open(output_file, 'w') as out_file:
        for file_name in common_files:
            file1_path = os.path.join(folder1, file_name)
            file2_path = os.path.join(folder2, file_name)

            # Read the CSV files into dictionaries
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                reader1 = csv.DictReader(file1)
                reader2 = csv.DictReader(file2)
                rows1 = {row['Question Number']: row for row in reader1}
                rows2 = {row['Question Number']: row for row in reader2}

                # Find differences between the two files
                for question_number in rows1.keys() & rows2.keys():
                    for column in rows1[question_number]:
                        if column in categories_to_ignore:
                            continue
                        if rows1[question_number][column] != rows2[question_number][column]:
                            out_file.write(f"File: {file_name}, Question: {question_number}, Column: {column}\n")
                            out_file.write(f"  Folder1: {rows1[question_number][column]}\n")
                            out_file.write(f"  Folder2: {rows2[question_number][column]}\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_csv.py <folder1> <folder2>")
        sys.exit(1)

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    output_file = "differences.txt"

    compare_csv_files(folder1, folder2, output_file)
    print(f"Differences saved in {output_file}")
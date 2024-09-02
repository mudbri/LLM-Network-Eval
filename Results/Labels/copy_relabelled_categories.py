import os
import sys
import pandas as pd

# Define the columns that need to be checked for discrepancies
COLUMNS_TO_CHECK = [
    "SM - Misunderstanding General", 
    "SM - Misunderstanding Reasons", 
    "AQ - Inferrable(0-2)?", 
    "AQ - Precise?", 
    "AQ - Explainable?", 
    "Effect - Conceptual error in explanaiton?(0/1)", 
    "CD - detection student(1-3)"
]

def compare_and_update_files(folder1, folder2, report_file):
    with open(report_file, 'w') as report:
        for filename in os.listdir(folder1):
            file1_path = os.path.join(folder1, filename)
            file2_path = os.path.join(folder2, filename)
            
            if os.path.isfile(file1_path) and os.path.isfile(file2_path):
                df1 = pd.read_csv(file1_path, encoding='utf-8')
                df2 = pd.read_csv(file2_path, encoding='utf-8')
                print(filename)
                if "Question Number" not in df1.columns or "Question Number" not in df2.columns:
                    continue
                
                df1.set_index("Question Number", inplace=True)
                df2.set_index("Question Number", inplace=True)
                
                changes_made = False
                
                for question_number in df1.index:
                    if question_number in df2.index:
                        for column in COLUMNS_TO_CHECK:
                            if df1.at[question_number, column] != df2.at[question_number, column]:
                                old_value = df1.at[question_number, column]
                                new_value = df2.at[question_number, column]
                                df1.at[question_number, column] = new_value
                                report.write(f"{filename} - Question {question_number} - Column '{column}': '{old_value}' -> '{new_value}'\n")
                                changes_made = True
                
                if changes_made:
                    df1.reset_index(inplace=True)
                    df1.to_csv(file1_path, index=False)
            else:
                print("File not found:", file2_path)
                exit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <folder1> <folder2>")
        sys.exit(1)

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    report_file = "changes_report.txt"
    
    compare_and_update_files(folder1, folder2, report_file)
    print(f"Changes have been recorded in {report_file}")
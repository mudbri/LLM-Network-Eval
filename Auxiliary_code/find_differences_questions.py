import os
import sys
import pandas as pd

def get_question_numbers(folder):
    question_numbers = set()
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    for file in files:
        df = pd.read_csv(os.path.join(folder, file))
        question_numbers.update(df['Question Number'])
    return question_numbers

def find_missing_rows(folder1, folder2):
    questions_folder1 = get_question_numbers(folder1)
    questions_folder2 = get_question_numbers(folder2)

    missing_in_folder2 = questions_folder1 - questions_folder2
    missing_in_folder1 = questions_folder2 - questions_folder1

    if missing_in_folder2:
        print("Missing questions in folder 2:")
        print(missing_in_folder2)

    if missing_in_folder1:
        print("Missing questions in folder 1:")
        print(missing_in_folder1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py folder1 folder2")
        sys.exit(1)

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    find_missing_rows(folder1, folder2)


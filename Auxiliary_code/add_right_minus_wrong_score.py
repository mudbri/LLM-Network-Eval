import os
import sys
import pandas as pd

def calculate_num_choices(text):
    choices = []
    for line in text.split("\n"):
        if len(line) > 1 and line[1] == ".":
            choices.append(line[0])
    return choices

# Define a custom function getScore
def calculate_score_Right_minus_wrong(correct_answers_arg, student_answers_arg, choices_arg):
    choices = calculate_num_choices(choices_arg)
    num_choices = len(choices)
    correct_answers = correct_answers_arg.strip().split(",")
    if str(student_answers_arg) == "nan":
        return 0
    student_answers = student_answers_arg.strip().split(",")
    num_missing = 0
    num_additional = 0
    for answer in correct_answers:
        if answer not in student_answers:
            num_missing += 1

    for answer in student_answers:
        if answer not in correct_answers:
            num_additional += 1

    num_incorrect = num_additional+num_missing
    num_correct = num_choices-num_incorrect

    score = num_correct / num_choices - num_incorrect / num_choices

    return max(0, score)  # Ensure score is non-negative

def add_right_minus_wrong_score(csv_folder):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    
    # Iterate over each CSV file
    for file in csv_files:
        # Read CSV file into a DataFrame
        df = pd.read_csv(os.path.join(csv_folder, file))
        
        # Add a third column by applying getScore function to columns "A" and "B"
        df['Score-right-minus-wrong'] = df.apply(lambda row: calculate_score_Right_minus_wrong(row['Correct Answer'], row['LLM Answer'], row['Choices']), axis=1)
        # df['Score-right-minus-wrong'] = df.apply(lambda row: calculate_score_Right_minus_wrong(row['Correct Answer'], row['New LLM Answer'], row['Choices']), axis=1)
        
        # Save the modified DataFrame back to CSV
        df.to_csv(os.path.join(csv_folder, file), index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_folder>")
        sys.exit(1)
    
    csv_folder = sys.argv[1]

    if not os.path.isdir(csv_folder):
        print("Error: Invalid folder path.")
        sys.exit(1)

    add_right_minus_wrong_score(csv_folder)
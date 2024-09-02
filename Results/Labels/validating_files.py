import os
import pandas as pd
import sys

# Define valid values for each column
valid_values = {
    "SM - Misunderstanding General": ["Wrong Facts/Concept", "Misinterpreting questions", "Incorrect reasoning/deduction"],
    "SM - Misunderstanding Reasons": ["Corner Case", "Out of date information", "Incorrect information/concept", "Quantifier issue", "Direct vs Indirect Causation", "Misinterpreting a word", "Incorrect copying of the question", "No explanation given", "Incorrect calculation or counting", "An error related to misinterpreting IP addresses", "Contradictory reasoning", "Senseless", "Faulty inference", "Self-aware but still wrong conclusion", "Incorrect Choice"],
    "AQ - Inferrable(0-2)" : [0,1,2],
    "AQ - Precise?" : [0,1],
    "AQ - Explainable?" : [0,1],
    "Effect - Conceptual error in explanation?(0/1)" : [0,1],
    "CD - detection student(1-3)" : [1,2,3]
    # "CD - correction student(1-8)" : [1,2,3,4,5,6,7,8],
    # "CD - detection knowledgeable(1-3)" : [1,2,3],
    # "CD - correction knowledgeable(1-8)" : [1,2,3,4,5,6,7,8]
    # Add similar validations for other columns here
}

def validate_and_correct(df, column, valid_values, file_path):
    # Iterate over the rows in the specified column
    for index, value in df[column].items():
        if "," in str(value):
            new_val = value.split(",")
            correct_values = []
            for val in new_val:
                if val.strip() not in valid_values:
                    if val == "Incorrect choice" or val == "Selecting the wrong choice":
                        correct_value.append("Incorrect Choice")
                    elif val == "Quantifier (universal vs existential)" or val == "Quantifier Issues":
                        correct_value.append("Quantifier issue")
                    elif val == "Not having some information/concept, Having the wrong information/concept":
                        correct_value.append("Incorrect information/concept")
                    elif val == "Wrong Facts/Concepts":
                        correct_value.append("Wrong Facts/Concept")
                    elif val == "Misinterpreting Question":
                        correct_value.append("Misinterpreting questions")
                    else:
                        # Prompt user to correct the invalid entry
                        print()
                        print(f"Invalid value '{val}' found in column '{column}' at row {index + 1} in {file_path}")
                        if column == "SM - Misunderstanding General" or column == "SM - Misunderstanding Reasons":
                            correct_value = input(f"Please enter a valid value ({', '.join(valid_values)}): ").strip()
                        else:
                            correct_value = input(f"Please enter a valid value: ").strip()
                        correct_values.append(correct_value)
                else:
                    correct_values.append(val)
                    # # Keep prompting until a valid value is provided
                    # while correct_value not in valid_values:
                    #     print(f"'{correct_value}' is not a valid value.")
                    #     correct_value = input(f"Please enter a valid value ({', '.join(valid_values)}): ").strip()
                    
                    # Update the DataFrame with the corrected value
            if len(correct_values) > 1:
                # remove duplicates
                if correct_values[0].strip() == correct_values[1].strip():
                    print("Duplicate values, removing: ", correct_values)
                    correct_values.pop(0)
            df.at[index, column] = ", ".join(correct_values)

        elif value not in valid_values:
            if value == "Incorrect choice" or value == "Selecting the wrong choice":
                correct_value = "Incorrect Choice"
            elif value == "Quantifier (universal vs existential)" or value == "Quantifier Issues":
                correct_value = "Quantifier issue"
            elif value == "Not having some information/concept, Having the wrong information/concept" or "incorrect information" in str(value).lower():
                correct_value = "Incorrect information/concept"
            elif value == "Wrong Facts/Concepts" or value == "Wrong facts/concepts" or "wrong facts" in str(value).lower() or "concept" in str(value).lower():
                correct_value = "Wrong Facts/Concept"
            elif value == "Misinterpreting Question" or "misinterpreting question" in str(value).lower():
                correct_value = "Misinterpreting questions"
            elif value == "Incorrect reasoning" or value == "Incorrect Reasoning":
                correct_value = "Incorrect reasoning/deduction"
            elif value == "Incorrecting calculation" or value == "Incorrect calculation":
                correct_value = "Incorrect calculation or counting"
            else:
                # Prompt user to correct the invalid entry
                print()
                print(f"Invalid value '{value}' found in column '{column}' at row {index + 1} in {file_path}")
                correct_value = input(f"Please enter a valid value ({', '.join(valid_values)}): ").strip()
            
            # # Keep prompting until a valid value is provided
            # while correct_value not in valid_values:
            #     print(f"'{correct_value}' is not a valid value.")
            #     correct_value = input(f"Please enter a valid value ({', '.join(valid_values)}): ").strip()
            
            # Update the DataFrame with the corrected value
            df.at[index, column] = correct_value

def validate_csv_file(file_path, valid_values):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Check if the DataFrame is empty
    if df.empty:
        print(f"Skipping empty file: {file_path}")
        return
    # Validate each column
    for column, valid_values in valid_values.items():
        if column in df.columns:
            validate_and_correct(df, column, valid_values, file_path)
    
    # Save the corrected DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print(f"Validation and correction complete for file: {file_path}")

def validate_csv_folder(folder_path, valid_values):
    # Iterate over all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            validate_csv_file(file_path, valid_values)

if __name__ == "__main__":
    # Check if the folder path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    # Validate the CSV files in the folder
    validate_csv_folder(folder_path, valid_values)

import os
import sys
import pandas as pd

def fill_missing_values_and_remove_empty_question_number_rows(folder1, folder2):
    # Get a list of all CSV files in folder 2
    for filename in os.listdir(folder2):
        if filename.endswith(".csv"):
            file1_path = os.path.join(folder1, filename)
            file2_path = os.path.join(folder2, filename)
            
            # Check if the corresponding file exists in folder 1
            if not os.path.exists(file1_path):
                print(f"Warning: {file1_path} does not exist. Skipping.")
                continue
            
            # Load both CSV files
            df1 = pd.read_csv(file1_path)
            df2 = pd.read_csv(file2_path)
            
            # Check if the "Question Number" column exists in both files
            if "Question Number" not in df1.columns or "Question Number" not in df2.columns:
                print(f"Warning: 'Question Number' column is missing in {filename}. Skipping.")
                continue
            
            # Set "Question Number" as the index for both DataFrames
            df1.set_index("Question Number", inplace=True)
            df2.set_index("Question Number", inplace=True)
            
            # Fill missing values in df2 with corresponding values from df1
            df2_filled = df2.fillna(df1)
            
            # Reset the index to turn "Question Number" back into a column
            df2_filled.reset_index(inplace=True)

            # Remove rows where "Question Number" is empty (NaN)
            df2_filled.dropna(subset=["Question Number"], inplace=True)
            
            
            # Save the cleaned and filled DataFrame back to the CSV file in folder 2
            df2_filled.to_csv(file2_path, index=False)
            print(f"Filled missing values and removed rows with empty 'Question Number' in {file2_path}")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <folder1_path> <folder2_path>")
        sys.exit(1)
    
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    
    # Validate the CSV files in the folder
    fill_missing_values_and_remove_empty_question_number_rows(folder1, folder2)
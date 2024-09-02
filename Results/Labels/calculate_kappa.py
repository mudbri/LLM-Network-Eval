import os
import sys
import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Define the valid values for each column
valid_values = {
    "SM - Misunderstanding General": ["Wrong Facts/Concept", "Misinterpreting questions", "Incorrect reasoning/deduction"],
    "SM - Misunderstanding Reasons": ["Corner Case", "Out of date information", "Incorrect information/concept", "Quantifier issue", "Direct vs Indirect Causation", "Misinterpreting a word", "Incorrect copying of the question", "No explanation given", "Incorrect calculation or counting", "An error related to misinterpreting IP addresses", "Contradictory reasoning", "Senseless", "Faulty inference", "Self-aware but still wrong conclusion", "Incorrect Choice"],
    "AQ - Inferrable(0-2)?" : [0, 1, 2],
    # "AQ - Precise?" : [0, 1],
    # "AQ - Explainable?" : [0, 1],
    "Effect - Conceptual error in explanaiton?(0/1)" : [0, 1],
    "CD - detection student(1-3)" : [1, 2, 3]
    # "CD - correction student(1-8)" : [1, 2, 3, 4, 5, 6, 7, 8],
    # "CD - detection knowledgeable(1-3)" : [1, 2, 3],
    # "CD - correction knowledgeable(1-8)" : [1, 2, 3, 4, 5, 6, 7, 8]
}

def load_and_concat_files(folder, valid_values):
    all_data = []
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            print(filename)
            filepath = os.path.join(folder, filename)
            df = pd.read_csv(filepath)
            if df.empty:
                print("Empty file. Skipping:", filename)
                continue
            # Add filename as a new column to ensure uniqueness when merging
            df['filename'] = filename
            
            # Only keep rows with valid "Question Number"
            df = df[df['Question Number'].notna()]
            
            # Convert float columns to int where necessary
            for column in valid_values.keys():
                if column in df.columns and pd.api.types.is_float_dtype(df[column]):
                    df[column] = df[column].astype(int)
                    # df[column] = df[column].astype(str)
            
            # Append the data to the list
            all_data.append(df)
    
    # Concatenate all data into a single DataFrame
    concatenated_df = pd.concat(all_data, ignore_index=True)
    
    return concatenated_df

def calculate_kappa_across_files(folder1, folder2, valid_values):
    # Load and concatenate all files from both folders
    df1 = load_and_concat_files(folder1, valid_values)
    df2 = load_and_concat_files(folder2, valid_values)

    
    # Merge on "Question Number" and "filename" to align the rows for comparison
    merged_df = pd.merge(df1, df2, on=["Question Number", "filename"], suffixes=('_1', '_2'))
    
    # Iterate through each column in the valid_values dictionary
    for column, valid in valid_values.items():
        col_1 = column + '_1'
        col_2 = column + '_2'
        if col_1 in merged_df.columns and col_2 in merged_df.columns:
            # Validate values in both columns
            df_valid = merged_df[merged_df[col_1].isin(valid) & merged_df[col_2].isin(valid)]
            # print(df_valid[col_1])
            # print(df_valid[col_2])
            # print(column)
            
            # Calculate Cohen's Kappa score
            kappa_score = cohen_kappa_score(df_valid[col_1], df_valid[col_2])
            print(f"Cohen's Kappa for '{column}': {kappa_score:.4f}")
        else:
            print(f"Warning: '{column}' column is missing in the merged data.")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <folder1_path> <folder2_path>")
        sys.exit(1)
    
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    
    # Calculate Cohen's Kappa score after concatenating all files in both folders
    calculate_kappa_across_files(folder1, folder2, valid_values)
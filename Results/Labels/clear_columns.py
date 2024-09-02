import os
import pandas as pd
import sys

def clear_columns(folder_path):
    # List of columns to clear
    columns_to_clear = [
        "Effect - Subtopics", 
        "Sources Relevant(number)", 
        "Sources Types", 
        "Source links work(number)", 
        "SM - Misunderstanding Reasons (secondary)", 
        "SM - Misunderstanding General (secondary)", 
        "SM - Description"
    ]
    
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Clear values in the specified columns
            df[columns_to_clear] = df[columns_to_clear].applymap(lambda x: None if pd.notnull(x) else x)
            
            # Save the updated dataframe back to the CSV file
            df.to_csv(file_path, index=False)
            print(f"Updated {filename}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        clear_columns(folder_path)

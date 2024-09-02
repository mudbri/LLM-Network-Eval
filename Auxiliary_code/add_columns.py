import pandas as pd
import os
import sys

def add_columns_to_csv(input_dir, output_dir, new_columns):
    """
    Adds new columns to all CSV files in the input directory and saves the modified files to the output directory.

    Parameters:
    - input_dir: The directory containing the original CSV files.
    - output_dir: The directory where modified CSV files will be saved.
    - new_columns: A list of new columns to add to each CSV file.
    """

    # Check if the output directory exists, and if not, create it.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all CSV files in the input directory.
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            # Load the CSV file into a DataFrame.
            df = pd.read_csv(file_path)

            # Add new columns with NaN values (or you can assign a default value instead of NaN).
            for column in new_columns:
                df[column] = None # Or use a default value like "" for empty string, 0 for an integer column, etc.

            # Construct the path for the output file.
            output_file_path = os.path.join(output_dir, filename)

            # Save the modified DataFrame to a new CSV file in the output directory.
            df.to_csv(output_file_path, index=False)
            print(f"Processed and saved: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_folder>")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        new_columns = ["QD - Goal clear?(0/1)","QD - Context clear?(0/1)","QD - How challenging(1-4)","QD - Level learnt(1-7)","SM - Description", "SM - Goal understood?(0/1)","SM - Context understood?(0/1)","SM - Implied Context understood?(0/1)","SM - Relvant facts identified?(0/1)","SM - Correct facts retieved?(0/1)","SM - No incorrect facts?(0/1)", "SM - Correct reasoning?(0/1)","SM - Misunderstanding General","SM - Misunderstanding Reasons","SM - Misunderstanding General (secondary)", "SM - Misunderstanding Reasons (secondary)","AQ - Inferrable(0-2)?","Source links work(number)","Sources Types","Sources Relevant(number)","Source Problems","AQ - Precise?","AQ - Explainable?","Effect - Description of effects","Effect - Conceptual error in explanaiton?(0/1)","Effect - Subtopics","Effect - Error Type","Effect - Severity","Effect - Who is most effected(1-4)","CD - detection student(1-3)","CD - correction student(1-8)","CD - detection knowledgeable(1-3)","CD - correction knowledgeable(1-8)"] 
        add_columns_to_csv(input_folder, output_folder, new_columns)


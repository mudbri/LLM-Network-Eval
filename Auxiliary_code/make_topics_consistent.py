import pandas as pd
import os
import argparse

# Function to apply the transformations to the "Topic" column
def transform_topic(topic):
    newTopic = topic
    if newTopic.startswith("grad_"):
        newTopic = newTopic[5:]
    if newTopic.startswith("google_"):
        newTopic = newTopic[7:]
    if newTopic.endswith("_random_choice"):
        newTopic =  newTopic[:-14]
    if newTopic.endswith(".txt"):
        newTopic =  newTopic[:-4]
    return newTopic

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process CSV files in a folder and apply transformations to the "Topic" column.')
parser.add_argument('folder', type=str, help='Path to the folder containing CSV files')
args = parser.parse_args()

# Validate folder path
folder_path = args.folder
if not os.path.isdir(folder_path):
    print("Error: The specified folder path does not exist.")
    exit()

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        # Read the CSV file into a DataFrame
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        # Apply the transformations to the "Topic" column
        df["Topic"] = df["Topic"].apply(transform_topic)
        
        # Write the modified DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

print("Processing completed.")

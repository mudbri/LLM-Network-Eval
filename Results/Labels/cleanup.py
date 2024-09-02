import pandas as pd
import os
import argparse

def remove_colms(folder_path):
    # Columns to remove
    columns_to_remove = ["Valid Question?", "Correct Explanation","QD - Goal clear?(0/1)", "QD - Context clear?(0/1)", "QD - How challenging(1-4)", "QD - Level learnt(1-7)", "SM - Goal understood?(0/1)", "SM - Context understood?(0/1)", "SM - Implied Context understood?(0/1)", "SM - Relvant facts identified?(0/1)", "SM - Correct facts retieved?(0/1)", "SM - No incorrect facts?(0/1)", "SM - Correct reasoning?(0/1)", "Source Problems", "Effect - Description of effects", "Effect - Error Type", "Effect - Severity", "Effect - Who is most effected(1-4)"]

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Remove the specified columns
            df = df.drop(columns=columns_to_remove, errors='ignore')

            # Save the modified DataFrame back to a CSV file (overwriting the original file)
            df.to_csv(file_path, index=False)

def remove_rows_where_correct_is_one(folder_path):
    """
    Reads all CSV files in a specified folder and removes rows where the 'Correct?' column is 1.

    Parameters:
    folder_path (str): Path to the folder containing the CSV files.
    """
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Check if the column 'Correct?' exists before attempting to filter
            if "Correct?" in df.columns:
                # Remove rows where 'Correct?' is 1
                df = df[df["Correct?"] != 1]

                # Save the modified DataFrame back to a CSV file (overwriting the original file)
                df.to_csv(file_path, index=False)

    print("Rows with 'Correct?' equal to 1 have been removed from all CSV files in the folder.")



def replace_texts_in_csv(folder_path, old_texts, new_text):
    """
    Reads all CSV files in a specified folder and replaces all occurrences of specified texts with a new text.

    Parameters:
    folder_path (str): Path to the folder containing the CSV files.
    old_texts (list): A list of texts to be replaced.
    new_text (str): The text to replace with.
    """
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Replace all occurrences of old_texts with new_text
            for old_text in old_texts:
                df = df.replace(old_text, new_text)

            # Save the modified DataFrame back to a CSV file (overwriting the original file)
            df.to_csv(file_path, index=False)

    print(f"Text replacement completed for all CSV files in the folder.")

def replace_subtopics_in_csv(folder_path):
    """
    Reads all CSV files in a specified folder and replaces specific values in the 'Effect - Subtopics' column.

    Parameters:
    folder_path (str): Path to the folder containing the CSV files.
    """
    # Define the replacements to be made
    effect_subtopics = {
        # "Configurations": ["Configuring EtherChannel", "WLAN Configuration", "Configuring switches", "Administrative Distances"],
        "Basic networking": ["IP Translation", "IP Ranges", "IP Subnetting", "IP Class Ranges", "Layer 3 Switches", "IP Routing", "CIDR", "DNS Queries", "Packet Switching", "CDNs", "TCP", "Network Architecture", "Internet protocol suite", "OSPF", "IPv4", "ARP", "Routers", "BGP", "NAT/PAT", "Virtual Networks", "BOOTP", "Server", "POTS", "terminology", "IPv6", "Wireless"],

        "Network security": ["ACL mask", "ACL numbers", "ACL rules processing", "CSMA", "DDoS", "Spoofing", "Two-factor Authentication", "Proxies", "Network Attacks", "WAN security", "ACL capabilities"],

        "Network administration": ["CISCO Commands", "Cisco DNA Center", "mininet", "Mininet", "SSH", "Network utilities", "Ethernet Cables", "QoS characteristics", "Router Hardware", "layer-2 MAC topology", "Configuring EtherChannel", "WLAN Configuration", "Configuring switches", "Administrative Distances", "E-Lan Configuration", "Logging", "IEEE 802.11 Wi-Fi standards"],

        "Advanced networking": ["Protocol Independent Forwarding", "P4", "Click", "Ethernet GRE", "OpenFlow Rule Composition", "SDNs", "4D Network Architecture", "OpenFlow Code", "Nicira", "FlowVisor", "Flowspaces", "Pyretic", "NFV", "SwitchBlade", "NetASM", "NVP", "PortLand","Configuration Verification","Data Plane Verification", "OpenFlow", "Routing Control Platform", "SDX", "SDN in Home Networks", "SDN Controllers"]
    }
    replacements = reverse_dictionary(effect_subtopics)
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Check if the column 'Effect - Subtopics' exists before making replacements
            if "Effect - Subtopics" in df.columns:
                # Replace specified values in the 'Effect - Subtopics' column
                df["Effect - Subtopics"] = df["Effect - Subtopics"].replace(replacements)

                # Save the modified DataFrame back to a CSV file (overwriting the original file)
                df.to_csv(file_path, index=False)

    print("Subtopic replacements completed for all CSV files in the folder.")

def count_rows_in_each_csv_file(folder_path):
    """
    Counts the number of rows in each CSV file within a specified folder and prints the count for each file.

    Parameters:
    folder_path (str): Path to the folder containing the CSV files.
    """
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Get the number of rows in the current DataFrame
            row_count = len(df)

            # Print the number of rows for the current CSV file
            print(f"{filename}: {row_count} rows")

def reverse_dictionary(dictionary):
    new_dictionary = {}
    for key, values in dictionary.items():
        for value in values:
            new_dictionary[value] = key
    return new_dictionary

def count_rows_in_csv_files(folder_path):
    """
    Counts the total number of rows in all CSV files within a specified folder.

    Parameters:
    folder_path (str): Path to the folder containing the CSV files.

    Returns:
    int: Total number of rows across all CSV files in the folder.
    """
    total_rows = 0

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Add the number of rows in the current DataFrame to the total count
            total_rows += len(df)

    print(f"Total number of rows across all CSV files: {total_rows}")
    return total_rows

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Replace subtopics in CSV files within a folder.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing the CSV files.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Folder path containing the CSV files
    folder_path = args.folder_path
    # remove_colms(folder_path)
    # remove_rows_where_correct_is_one(folder_path)
    # replace_texts_in_csv(folder_path, ["IP Range Incorrect"], "An error related to misinterpreting IP addresses")
    # replace_texts_in_csv(folder_path, ["Incorrect Choice", "Incorrect Choice"], "Selecting the wrong choice")
    # replace_texts_in_csv(folder_path, ["Interpreted a word or background incorrectly", "Misunderstanding word mapping to meaning","Didn't understand a word or format", "Didn't understand logical syntax"], "Misinterpreting a word")
    # replace_texts_in_csv(folder_path, ["Having the wrong information/concept", "Not having some information/concept"], "Incorrect information/concept")
    # replace_texts_in_csv(folder_path, ["Wrong Information/Hallucinations", "Conceptual Misunderstanding"], "Wrong Facts/Concept")
    # replace_texts_in_csv(folder_path, ["Incorrect copying or not seeing the correct choice"], "Incorrect copying of the question")
    # replace_texts_in_csv(folder_path, ["Misunderstanding context or implied background", "Otherwise didn't understand the goal of the question"], "Misinterpreting questions")
    # replace_texts_in_csv(folder_path, ["Internal inconsistency"], "Contradictory reasoning")
    # replace_texts_in_csv(folder_path, ["Not being able to derive the correct conclusion", "Non Sequitur"], "Faulty inference")
    # replace_texts_in_csv(folder_path, ["trusted article"], "Article")
    # replace_texts_in_csv(folder_path, ["Incorrect calculation", "Incorrect counting"], "Incorrect calculation or counting")

                               
    # replace_subtopics_in_csv(folder_path)
    count_rows_in_csv_files(folder_path)
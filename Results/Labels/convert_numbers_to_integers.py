import os
import csv
import sys

def convert_specific_numbers_to_integers(folder):
    # Define the set of numbers to be converted to integers
    numbers_to_convert = {0, 1, 2, 3, 4, 5, 6, 7, 8}

    # Get a list of all CSV files in the folder
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]

    for file_name in files:
        file_path = os.path.join(folder, file_name)

        # Read the CSV file and convert specific numbers to integers
        with open(file_path, 'r') as file:
            reader = list(csv.reader(file))
            header = reader[0]
            rows = reader[1:]

            # Convert specific numbers to integers in the rows
            converted_rows = []
            for row in rows:
                converted_row = []
                for value in row:
                    try:
                        # Convert the value to float and check if it matches the numbers to convert
                        float_value = float(value)
                        if float_value in numbers_to_convert:
                            converted_row.append(int(float_value))
                        else:
                            converted_row.append(value)
                    except ValueError:
                        # If it's not a number, keep it as is
                        converted_row.append(value)
                converted_rows.append(converted_row)

        # Write the modified data back to the CSV file
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(converted_rows)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_numbers_to_integers.py <folder>")
        sys.exit(1)

    folder = sys.argv[1]
    convert_specific_numbers_to_integers(folder)
    print(f"All occurrences of numbers 0-8 in CSV files in '{folder}' have been converted to integers.")
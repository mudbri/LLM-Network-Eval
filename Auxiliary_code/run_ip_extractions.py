import subprocess
import os

def run_command(command):
    """Run the shell command using subprocess and print output for debugging."""
    try:
        # Execute the command and wait for completion
        subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Successfully executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}")
        print(f"Error output:\n{e.stderr.decode()}")  # Print the error message from stderr

def ensure_directory_exists(path):
    """Ensure that the directory exists, create it if not."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def main():
    # Define the base paths for each set of commands
    models = ['Claude3', 'GPT4', 'GPT3.5']
    runs = [1, 2, 3, 4, 5]
    
    # Loop through each model and run number to construct the command
    for model in models:
        for run in runs:
            input_folder = f"../Results/Multiple_runs/{model}/{run}"
            output_folder = f"../Results/Multiple_runs/IP/{model}/{run}"
            output_file = f"{output_folder}/{model}_ip_ques_{run}.csv"
            
            # Ensure the output directory exists
            ensure_directory_exists(output_folder)
            
            # Construct the command
            command = f"python3 ./extract_ip_questions.py {input_folder} {output_file}"
            run_command(command)

if __name__ == "__main__":
    main()

import pandas as pd
import os
import argparse
import transformers
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import re

choicesLetters = ['a','b','c','d','e','f','g','h','i','j']

def extract_between_answer_and_explanation_Mistral(text):
    # Regular expression to match content between "Answer:" and "Explanation:"
    pattern = re.compile(r'Answer:(.*?)(?=\nExplanation:)', re.DOTALL)
    # Find all matches in the text
    matches = pattern.findall(text)
    # Clean up the matches by stripping any leading/trailing whitespace
    answers = [match.strip() for match in matches]
    if len(answers) == 0:
        print(text)
        answer = input("Please provide the choices")
        return answer
    else:
        return answers[0]
    
def parseFreeAnswersMistral(response, choices):
  response = extract_between_answer_and_explanation_Mistral(response)
  print(response)
  answers = []
  if "," in response:
    print("Comma detected")
    commasplits = response.split(",")
    for split in commasplits:
      for letter in choicesLetters:
        if (split == letter+" " or split == letter or split == " "+letter or split[-2:] == " "+letter or split[0:3] == " " + letter + "\n" or split[0:3] == " " + letter +".") and letter not in answers:
            answers.append(letter)
  for letter in choicesLetters:
    if letter+". " in response or " " + letter +"." in response or ": " + letter in response or " and " + letter + " " in response:
        if letter not in answers:
          answers.append(letter)
    elif letter == response:
       answers.append(letter)
    elif response[-2:] == "\n"+letter:
       answers.append(letter)
       
  if len(answers) == 0:
    print("No response given: ", response)
    print("Choices: ", choices)
    answers = input().split(",")
  print(answers)
  return ",".join(answers)

def infer_mistral(question_text, choices, model):
    # Update model and model_id for Mistral
    model_id = "mistralai/" + model

    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    # Create the pipeline
    pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    message_question = question_text + "\n" + choices

    # Adjust how the messages are input to the model
    # Since this is a text-generation pipeline, we concatenate the messages.
    prompt = "As a virtual assistant specializing in computer networking, your task is to analyze and respond to multiple-choice questions from a course related to computer networking. For each question, you are to identify the correct option(s) from the given choices. Your response should  include the selected option(s) using their corresponding letter(s) in lowercase (e.g., a, b, c, d) or combination thereof if multiple selections are correct and an explanation. Respond with the selected choices and explanation.\nQuestion: " + message_question + "\nAnswer: "
    
    outputs = pipeline(
        prompt,
        max_new_tokens=256,
        do_sample=False,  # If you want non-deterministic generation; set to False for deterministic.

    )
    
    answer = outputs[0]["generated_text"].strip()
    return parseFreeAnswersMistral(answer, choices)

def extract_between_answer_and_explanation(text):
    # Regular expression to match content between "Answer:" and "Explanation:"
    match = re.search(r"(.*?)(?=Explanation:)", text, re.DOTALL)
    
    # If a match is found, return the matched text
    if match:
        return match.group(1).strip()
    else:
        return text  # Return the original text if "Explanation:" is not found
    
def parseFreeAnswers(response, choices):
  response = extract_between_answer_and_explanation(response)
  print(response)
  answers = []
  if "," in response:
    print("Comma detected")
    commasplits = response.split(",")
    for split in commasplits:
      for letter in choicesLetters:
        if (split == letter+" " or split == letter or split == " "+letter or split[-2:] == " "+letter or split[0:3] == " " + letter + "\n" or split[0:3] == " " + letter +".") and letter not in answers:
            answers.append(letter)
  for letter in choicesLetters:
    if letter+". " in response or " " + letter +"." in response or ": " + letter in response or " and " + letter + " " in response:
        if letter not in answers:
          answers.append(letter)
    elif letter == response:
       answers.append(letter)
    elif response[-2:] == "\n"+letter:
       answers.append(letter)
       
  if len(answers) == 0:
    print("No response given: ", response)
    print("Choices: ", choices)
    answers = input().split(",")
  print(answers)
  return ",".join(answers)

def infer_gemma(question_text, choices, model):
    # Update model and model_id for Gemma
    model_id = "google/" + model

    # Load the tokenizer and model
    # tokenizer = AutoTokenizer.from_pretrained(model_id)
    # model = AutoModelForCausalLM.from_pretrained(
    #     model_id, 
    #     torch_dtype=torch.bfloat16,
    #     device_map="auto"
    # )

    # # Create the pipeline
    pipe = pipeline(
        "text-generation",
        model="google/gemma-2-9b-it",
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )
    
    message_question = question_text + "\n" + choices

    # Adjust how the messages are input to the model
    # Since this is a text-generation pipeline, we concatenate the messages.
    prompt = "As a virtual assistant specializing in computer networking, your task is to analyze and respond to multiple-choice questions from a course related to computer networking. For each question, you are to identify the correct option(s) from the given choices. Your response should  include the selected option(s) using their corresponding letter(s) in lowercase (e.g., a, b, c, d) or combination thereof if multiple selections are correct and an explanation. Respond with only the selected choices and \"Explanation\".\nQuestion: " + message_question + "\nCorrect Options: "
    
    messages = [
        {"role": "user", "content": prompt},
    ]
    
    outputs = pipe(messages, max_new_tokens=256)
    assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
    return parseFreeAnswers(assistant_response, choices=choices)

def infer_llama(question_text, choices, model):
    model_id = "meta-llama/" + model

    pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )

    message_question = question_text+"\n"+choices    
    messages = [
        {"role": "system", "content": "As a virtual assistant specializing in computer networking, your task is to analyze and respond to multiple-choice questions from a course related to computer networking. For each question, you are to identify the correct option(s) from the given choices. Your response should only include the selected option(s) using their corresponding letter(s) in lowercase (e.g., a, b, c, d) or combination thereof if multiple selections are correct."},
        {"role": "user", "content": message_question},
    ]
    
    outputs = pipeline(
        messages,
        max_new_tokens=256,
    )
    answer = outputs[0]["generated_text"][-1]["content"]
    answer = answer.replace(", ", ",")
    answer = answer.replace(".", "")
    print(answer)
    return answer

def process_csv_files(folder_path, model_name, hf_token):
    """
    Processes all CSV files in the specified folder as follows:
    - Prints the content of 'Question Text' and 'Choices' columns.
    - Keeps only the columns: 'Question Number', 'Question Text', 'Choices', 'Correct Answer'.
    - Adds a new column named 'LLM Answer' with default values.
    - Saves the modified DataFrame to a new CSV file with 'gpt3.5' replaced by 'llama3' in the filename.
    
    Parameters:
    folder_path (str): Path to the folder containing the CSV files.
    """
    os.environ["HF_TOKEN"] = hf_token
    # Define the columns to keep
    columns_to_keep = ["Question Number", "Question Text", "Choices", "Correct Answer"]
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            # Read the CSV file
            df = pd.read_csv(file_path)
            df = df[columns_to_keep]
            

            llm_answers = []
            # Print and store the content of 'Question Text' and 'Choices' columns for each row
            if "Question Text" in df.columns and "Choices" in df.columns:
                for index, row in df.iterrows():
                    question_text = row['Question Text']
                    choices = row['Choices']
                    if "llama" in model_name.lower():
                        llm_answer = infer_llama(question_text, choices, model_name)
                    elif "gemma" in model_name:
                        llm_answer = infer_gemma(question_text, choices, model_name)
                    elif "Mistral" in model_name or "mistral" in model_name:
                        llm_answer = infer_mistral(question_text, choices, model_name)
                    else:
                       print("Model {} not found".format(model_name))
                       exit()
                    llm_answers.append(llm_answer)
                    
            # Add a new column 'LLM Answer' with default values (e.g., 'Not Answered')
            df["LLM Answer"] = llm_answers
            
            df["Correct?"] = df.apply(lambda row: 1 if str(row["Correct Answer"]) == str(row["LLM Answer"]) else 0, axis=1)

            # Generate new filename by replacing 'gpt3.5' with 'llama3'
            new_filename = filename.replace('_gpt-3.5-turbo-0125', '_'+model_name)
            new_file_path = os.path.join(folder_path, new_filename)

            # Save the modified DataFrame to the new file
            df.to_csv(new_file_path, index=False)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    parser.add_argument("--folder", type=str, help="Path to the folder containing the CSV files that have questions. Use Results/GPT3.5 to make this script work")
    parser.add_argument("--model_name", type=str, help="Name of the model to run. Supported models: Meta-Llama-3.1-8B-Instruct, gemma-2-9b-it, Mistral-7B-Instruct-v0.2")
    parser.add_argument("--HF_TOKEN", type=str, help="Your Hugging Face API token (required for accessing certain models).")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the folder path provided by the user
    process_csv_files(args.folder, args.model_name, args.HF_TOKEN)
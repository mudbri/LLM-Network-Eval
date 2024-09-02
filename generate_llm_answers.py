from openai import OpenAI
import numpy as np
import json
from string import ascii_lowercase as alc
import sys
import os
import glob
import csv
import pandas as pd
import anthropic
import time
from copy import deepcopy
import random
import argparse
import prompts


choicesLetters = ['a','b','c','d','e','f','g','h','i','j']

# model="claude-3-opus-20240229"
# model="claude-2.0"
# model = "gpt-4-1106-preview"

# takes a list of choices as an array and converts them to a string
# [/24, /21, /19, 255.255.255.255, 255.255.240.0, 255.255.224.0] -> a. /24\nb. /21\nc. /19\nd. 255.255.255.255\ne. 255.255.240.0\nf. 255.255.224.0
def convertChoices(choices):
  i = 0
  choiceStr = ""
  while i < len(choices):
    choiceStr += alc[i] + ". " + choices[i]
    i += 1
    if i != len(choices):
       choiceStr += "\n"
  return choiceStr

def answer_question_with_explanation_Claude(user_question, choices, temperature=0.5, max_tokens=500, file="CISCO", model="claude-3-opus-20240229", mode="default", api=""):
  client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=api,
  )
  choiceStr = convertChoices(choices)
  mid = " When answering user questions follow this example:"
  prompt = prompts.Basic_prompt+mid+prompts.SDN_question
  if mode == "one_shot":
    if file == "grad_TCP.txt":
      prompt = prompts.Basic_prompt+mid+prompts.grad_tcp_question # grad prompt and basic prompt are the same
    elif "chapter" in file:
      prompt = prompts.Cisco_prompt+mid+prompts.Cisco_question
    elif "google" in file:
      prompt = prompts.Basic_prompt+mid+prompts.Basic_question
    elif "_" in file and file.split('_')[0].isdigit():
      prompt = prompts.SDN_prompt+mid+prompts.SDN_question
    elif file == "NetSec.txt":
      prompt = prompts.Basic_prompt+mid+prompts.netsec_question
    elif file == "Computer_Networking.txt":
      prompt = prompts.Basic_prompt+mid+prompts.computer_networking_question
    else:
      print("file {} is not one of the valid files".format(file))
      exit()
  else:
    if file == "grad_TCP.txt":
      prompt = prompts.Basic_prompt # grad prompt and basic prompt are the same
    elif "chapter" in file:
      prompt = prompts.Cisco_prompt
    elif "google" in file:
      prompt = prompts.Basic_prompt
    elif "_" in file and file.split('_')[0].isdigit():
      prompt = prompts.SDN_prompt
    elif file == "NetSec.txt":
      prompt = prompts.Basic_prompt
    elif file == "Computer_Networking.txt":
      prompt = prompts.Basic_prompt
    else:
      print("file {} does not exist".format(file))
      exit()
  message = client.messages.create(
      model=model,
      max_tokens=max_tokens,
      stop_sequences=["}"],
      temperature=temperature,
      system=prompt,
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": "Question: {user_question}\nChoices:\n{choiceStr}".format(user_question=user_question, choiceStr=choiceStr)
                  }
              ]
          }
      ]
  )
  time.sleep(5)
  return message.content

def answer_question_with_explanation_GPT(user_question, choices, temperature=0, max_tokens=500, file="CISCO", model="gpt-3.5-turbo-0125", mode="default", api=""):
    client = OpenAI(api_key=api)
    """
    This function takes a computer networking multiple-choice question as input
    and returns the GPT model's answer, explanation, and confidence in JSON format.
    """
    mid = " When answering user questions follow this example:"
    prompt = prompts.Basic_prompt+mid+prompts.SDN_question
    if mode == "one_shot":
      if "grad_TCP.txt" in file:
        prompt = prompts.Basic_prompt+mid+prompts.grad_tcp_question # grad prompt and basic prompt are the same
      elif "chapter" in file:
        prompt = prompts.Cisco_prompt+mid+prompts.Cisco_question
      elif "google" in file:
        prompt = prompts.Basic_prompt+mid+prompts.Basic_question
      elif "_" in file and file.split('_')[0].isdigit():
        prompt = prompts.SDN_prompt+mid+prompts.SDN_question
      elif "NetSec.txt" in file:
        prompt = prompts.Basic_prompt+mid+prompts.netsec_question
      elif "Computer_Networking.txt" in file:
        prompt = prompts.Basic_prompt+mid+prompts.computer_networking_question
      else:
        print("file {} does not exist".format(file))
        exit()
    elif mode == "finetune":
       if "chapter" in file:
          prompt = prompts.Cisco_finetune_prompt
       else: 
          prompt = prompts.finetune_prompt
    else:
      if file == "grad_TCP.txt":
        prompt = prompts.Basic_prompt # grad prompt and basic prompt are the same
      elif "chapter" in file:
        prompt = prompts.Cisco_prompt
      elif "google" in file:
        prompt = prompts.Basic_prompt
      elif "_" in file and file.split('_')[0].isdigit():
        prompt = prompts.SDN_prompt
      elif file == "NetSec.txt":
        prompt = prompts.Basic_prompt
      elif file == "Computer_Networking.txt":
        prompt = prompts.Basic_prompt
      else:
        print("file {} does not exist".format(file))
        exit()
       
    choiceStr = convertChoices(choices)
    if mode=="finetune":
      response = client.chat.completions.create(
        model=model,
        messages=[
          {"role": "system", "content": prompt},
          {"role": "user", "content": "Question: {user_question}\nChoices:\n{choiceStr}".format(user_question=user_question, choiceStr=choiceStr)}
        ],
        temperature=temperature,  # Higher value makes the answers more creative - more random. 0 makes them deterministic
        max_tokens=max_tokens,
        logprobs=True,
        top_logprobs=2,
        seed=123
      )
    else:
        response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
          {"role": "system", "content": prompt},
          {"role": "user", "content": "Question: {user_question}\nChoices:\n{choiceStr}".format(user_question=user_question, choiceStr=choiceStr)}
        ],
        temperature=temperature,  # Higher value makes the answers more creative - more random. 0 makes them deterministic
        max_tokens=max_tokens,
        logprobs=True,
        top_logprobs=2,
        seed=123
      )
    return response

def extract_logprob_confidence(numAnswers, response):
  for i in range(numAnswers):
    top_two_logprobs = response.choices[0].logprobs.content[6+(2*i)].top_logprobs
    logprobsStr = ""
    for i, logprob in enumerate(top_two_logprobs, start=1):
        logprobsStr += logprob.token.strip() + " " + str(np.round(np.exp(logprob.logprob)*100,2)) + ", "

  logprob_confidence = 0
  for i in range(numAnswers):
    top_two_logprobs = response.choices[0].logprobs.content[6+(2*i)].top_logprobs
    logprobTopChoice = top_two_logprobs[0]
    if logprob_confidence == 0:
      logprob_confidence = np.exp(logprobTopChoice.logprob)
    else:
      logprob_confidence *= np.exp(logprobTopChoice.logprob)

  print(logprobsStr)
  return logprob_confidence

def parseFreeAnswers(response, choices):
  answers = []
  if "," in response:
    print("Comma detected")
    commasplits = response.split(",")
    for split in commasplits:
      for letter in choicesLetters:
        if (split == letter+" " or split == letter or split == " "+letter or split[-2:] == " "+letter or split[0:3] == " " + letter + "\n") and letter not in answers:
            answers.append(letter)
  for letter in choicesLetters:
    if letter+". " in response or " " + letter +"." in response or ": " + letter in response:
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
  return answers

def extract_response_details(response, model, mode, choices):
   # print(response.choices[0].message.content)

  if mode=="finetune":
     answers = parseFreeAnswers(response.choices[0].message.content, choices)
     print(response.choices[0].message.content)
     print(answers)
     print()
     return answers, "", 1, 1, []
  if "gpt" in model:
    response_JSON = json.loads(response.choices[0].message.content)
  else: # fixing errors in claude3
    response_msg = response[0].text+"}"
    response_msg = response_msg.replace('\n ',"")
    response_msg = response_msg.replace('\n',"")
    response_msg = response_msg.replace('Sources',"sources")
    response_msg = response_msg.replace('"busy signal"',"busy signal")
    response_msg = response_msg.replace('"sitting duck"',"sitting duck")
    response_msg = response_msg.replace('"erroneous server"',"erroneous server")
    response_msg = response_msg.replace('"target server"',"target server")
    print(response_msg)
    response_JSON = json.loads(response_msg)

  explanation = response_JSON["explanation"]
  URLs = response_JSON["sources"]
  LLM_confidence = response_JSON["confidence"]
  answersUnformatted = response_JSON["answer"].split(",")
  answers = []
  for ans in answersUnformatted:
     answers.append(ans.strip())
  logprob_confidence = 1
  if "gpt" in model:
    logprob_confidence = extract_logprob_confidence(len(answers), response)
  return answers, explanation, LLM_confidence, logprob_confidence, URLs

# user_question = "Which of the following masks, when used within a Class B network, would supply enough subnet bits to support 90 subnets?(Choose two)"
# choices = ["/24", "/21", "/19", "255.255.255.255", "255.255.240.0", "255.255.224.0"]
# response = answer_question_with_explanation(user_question, choices)


# Parses questions and Returns a list of dictionaries. Each dictionary has a question number, question, and choices key
def parse_questions(file_name):
    questions = []
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into questions using the "Question" prefix
    raw_questions = content.split("Question")[1:]  # Skip the first split before the first "Question"

    for raw_question in raw_questions:
        # Further split each question into lines
        lines = raw_question.strip().split('\n')
        question_number, question_text = lines[0].split('.', 1)
        question_text = question_text.strip()
        choices = []
        correct_answers = []
        reading_question = True
        current_choice = -1
        for line in lines[1:]:  # Skip the question part
            line = line.strip()
            if not line.startswith('(') and reading_question:
               question_text += "\n" + line
            elif line.startswith('(') and ')' in line:
                reading_question = False
                # Extract choice letter and text, check if it's marked as correct
                choice_letter, choice_text = line.split(')', 1)
                choice_letter = choice_letter[1:].lower()
                choice_text = choice_text.strip()
                if choice_text.endswith('-*'):
                    correct_answers.append(choice_letter.strip())
                    choice_text = choice_text[:-2].strip()  # Remove the '-*' marker
                choices.append(choice_text)
                current_choice = len(choices)-1
            elif current_choice != -1:
                # Append the line to the current choice
                choice_text = line.strip()
                if choice_text.endswith('-*'):
                  correct_answers.append(choice_letter.strip())
                  choice_text = choice_text[:-2].strip()  # Remove the '-*' marker
                choices[current_choice] += '\n' + choice_text
            # else:
            #     # Start of a new choice
            #     current_choice = len(choices)
            #     choices.append(line)

        questions.append({
            'number': question_number.strip(),
            'text': question_text,
            'choices': choices,
            'correct_answers': correct_answers  # This includes the choices marked as correct
        })

    topic = file_name.split("/")[-1][:-4]
    return questions, topic

# Function to handle file gathering based on command line arguments
def handle_files(folder, file_names):
    if file_names == "all":
        # Use glob to list all files in the folder
        return glob.glob(os.path.join(folder, '*'))
    else:
        # Only include the specified files from the folder
        return [os.path.join(folder, name) for name in file_names.split(',')]

def overwrite_first_three_columns(csv_file_path, data):
    """
    Overwrites the first three columns of an existing CSV file with new data.

    :param csv_file_path: The path to the CSV file to be modified.
    :param data: A list of dictionaries, where each dictionary represents a row of data for the first three columns.
    """
    # Load the existing CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Check if the input data list is empty or if the CSV is empty; exit if true
    if not data or df.empty:
        print("No data provided or CSV file is empty.")
        return

    # Extract column names for the first three columns from the DataFrame
    column_names = df.columns[:3]

    # Prepare new data for the first three columns
    new_data = {col: [] for col in column_names}
    for row in data:
        for col in column_names:
            new_data[col].append(row.get(col, None))  # Use None for missing keys

    # Overwrite the first three columns in the DataFrame
    for col in column_names:
        df[col] = new_data[col]

    # Save the modified DataFrame back to the CSV, overwriting the original file
    df.to_csv(csv_file_path, index=False)
    print(f"Successfully updated the first three columns in '{csv_file_path}'.")

def write_csv_file(file_name, data, fieldnames):
  """
  Write data to a CSV file with specified fieldnames.

  Parameters:
  - file_name: The name of the CSV file to be created.
  - data: A list of dictionaries, where each dictionary represents a row of data.
  - fieldnames: A list of strings representing the column headers in the CSV file.
  """
  with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      # Write the header row
      writer.writeheader()

      # Write the data rows
      writer.writerows(data)

def output_to_csv(topic, questions, output_file="output.csv", file="CISCO", model="gpt-3.5-turbo-0125", mode="default", temp=0.5, api=""):
    data = []
    # Fieldnames for the CSV file
    fieldnames = ['Question Number', 'Question Text', 'Choices', 'Valid Question?', 'Correct Answer', 'LLM Answer', 'Correct Explanation', 'LLM Explanation', 'URLs','Correct?', 'Topic', 'LLM Confidence', 'logprob Confidence']

    for question in questions:
        questionData = {}
        questionData['Question Number'] = question["number"]
        questionData['Question Text'] = question["text"]
        i = 0
        choicesTxt = ""
        for choice in question["choices"]:
           choicesTxt += choicesLetters[i] + ". " + choice + "\n"
           i += 1
        questionData['Choices'] = choicesTxt
        questionData['Correct Answer'] = ",".join(question["correct_answers"])
        if "gpt" in model:
          response = answer_question_with_explanation_GPT(question["text"], question["choices"], file=file, model=model, temperature=temp, mode=mode, api=api)
        else:
          response = answer_question_with_explanation_Claude(question["text"], question["choices"], file=file, model=model, temperature=temp, mode=mode, api=api)
           
        answers, explanation, LLM_confidence, logprob_confidence, URLs = extract_response_details(response, model, mode, question["choices"])

        questionData['LLM Answer'] = ",".join(answers)
        questionData['LLM Explanation'] = explanation
        questionData['URLs'] = URLs # shows URLs
        questionData['Correct?'] = int(sorted(answers) == sorted(question["correct_answers"])) # compares the two sorted lists to see if they are equal
        questionData['Topic'] = topic
        questionData['LLM Confidence'] = LLM_confidence
        questionData['logprob Confidence'] = logprob_confidence
        data.append(questionData)

    # Write data to CSV file
    write_csv_file(output_file, data, fieldnames)

# takes questions as input and randomizes the order of the choices and the correct answers
def randomizeChoices(questions):
  newQuestions = []
  for question in questions:
    newQuestion = deepcopy(question)
    newQuestion["choices"] = []
    newQuestion["correct_answers"] = []
    choiceList = list(range(0, len(question["choices"])))
    random.shuffle(choiceList)
    i = 0
    for choiceNum in choiceList:
      newQuestion["choices"].append(question["choices"][choiceNum])
      oldChoiceLetter = choicesLetters[choiceNum]
      if oldChoiceLetter in question["correct_answers"]:
        newChoiceLetter = choicesLetters[i]
        newQuestion["correct_answers"].append(newChoiceLetter)
      i += 1
    newQuestions.append(newQuestion)
  return newQuestions

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="Process command-line inputs.")

    # Add arguments with default values
    parser.add_argument('--folder', type=str, required=True, help='Path to the folder that contains questions.')
    parser.add_argument('--files', type=str, default='default_files', help='Files to process separated by comma or \'all\'.')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo-0125', help='Model to use. (e.g., claude-3-opus-20240229, gpt-4-1106-preview, gpt-3.5-turbo-0125)')
    parser.add_argument('--temp', type=float, default=0.5, help='Temperature setting.')
    parser.add_argument('--api', type=str, required=True, help='API key for anthropic or OpenAI.')
    parser.add_argument('--mode', type=str, default='default_mode', help='Operation mode (default, finetune, or one_shot).')

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    folder_name = args.folder
    file_names = args.files
    model = args.model # global variable
    temp = args.temp # global variable
    mode = args.mode # global variable
    api = args.api

    print("Using model {} with temperature={}".format(model, temp))
    if mode=="one_shot":
      print("One-shot prompting")
    elif mode=="finetune":
      print("Finetuning prompting")
    else:
      print("Normal prompts")
    # Function mapping

    # Get the list of files based on the command line arguments
    files_to_process = handle_files(folder_name, file_names)

    
    for file in files_to_process: # for each file
      if "csv" in file: # skip csv files
         continue
      # Call the specified function with the list of files
      questions, topic = parse_questions(file)
      output_file = topic+"_"+model+mode+".csv"
      output_to_csv(topic=topic, questions=questions, output_file=output_file, file=file.split("/")[-1].strip(), model=model, mode=mode, temp=temp, api=api)

if __name__ == "__main__":
    main()

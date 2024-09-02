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

choicesLetters = ['a','b','c','d','e','f','g','h','i','j']

# Parses questions taken from the cisco examination. Returns a list of dictionaries. Each dictionary has a question number, question, and choices key
def cisco_file_process(file_name):
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

def storeQuestions(output_file_name, output_folder, questions):
    # Construct the file path
    output_file_path = os.path.join(output_folder, output_file_name)

    # Open the file in write mode and write the word "x"
    with open(output_file_path, 'w') as file:
        for question in questions:
            file.write("Question {number}. {question}\n".format(number=question["number"], question=question["text"]))
            for index, choice in enumerate(question["choices"]):
                choice_letter = choicesLetters[index]
                choice_letter_capital = choice_letter.upper()
                file.write("({letter}) {choice}".format(letter=choice_letter_capital, choice=choice))
                if choice_letter in question['correct_answers']:
                   file.write(" -*\n")
                else:
                   file.write("\n")
            file.write("\n")

def main():
    # Check if the required arguments are passed
    if len(sys.argv) != 5:
        print("Usage: <script> <function_name> <folder_name> <'all' or file_names> <output_folder>")
        sys.exit(1)

    function_name = sys.argv[1]
    folder_name = sys.argv[2]
    file_names = sys.argv[3]
    output_folder = sys.argv[4]

    # Function mapping
    # functions = {'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4}
    functions = {'cisco': cisco_file_process}

    # Validate function name
    if function_name not in functions:
        print(f"Invalid function name. Choose among {list(functions.keys())}.")
        sys.exit(1)

    # Get the list of files based on the command line arguments
    files_to_process = handle_files(folder_name, file_names)
    
    for file in files_to_process: # for each file
        if "txt" not in file: # skip csv files
            continue
        filename = file.split("/")[-1]
        # Call the specified function with the list of files
        questions, topic = functions[function_name](file)
        questions = randomizeChoices(questions)
        output_file = filename+"_random_choice.txt"
        print(questions)
        storeQuestions(output_file, output_folder, questions)

if __name__ == "__main__":
    main()

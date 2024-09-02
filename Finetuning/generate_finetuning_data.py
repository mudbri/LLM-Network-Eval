from bs4 import BeautifulSoup
import json


def getGeneralQuestions(filename="questions_sanfoundry.html"):
    # Load your HTML content
    with open(filename) as f:
        html_content = f.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize lists to store extracted data
    questions = []
    choices = []
    answers = []

    # Find all questions in the HTML
    question_blocks = soup.find_all('p')

    for block in question_blocks:
        if block.find('img'):
            continue  # Skip this question if an image is found

        full_text = block.get_text(strip=True, separator="\n")
        lines = full_text.splitlines()
        
        # The question text should be the first line before the choices
        if lines:
            question_text = lines[0]
        else:
            continue
        
        # Extract the choices
        current_choices = []
        for line in lines[1:]:
            if line.startswith(("a)", "b)", "c)", "d)")):
                current_choices.append(line.strip())
            else:
                break
        
        # If no choices were found, skip this question
        if not current_choices:
            continue
        
        # Extract the answer
        # Find the associated answer block
        # Find the associated answer block
        answer_span = block.find_next('span', class_='collapseomatic')
        if not answer_span:
            continue  # Skip if there's no answer span
        
        answer_id = answer_span.get('id')
        if not answer_id:
            continue  # Skip if the span doesn't have an id

        answer_block = soup.find('div', id=f'target-{answer_id}')
        if not answer_block:
            continue  # Skip if the answer block is not found
        
        # Extract the answer
        answer_text = answer_block.get_text(strip=True, separator=" ").splitlines()[0]
        # Extract just the letter from "Answer: a" format
        correct_answer = answer_text.replace('Answer: ', '').strip().split()[0]
        
        if "img" in correct_answer:
            continue
        new_answer_text = ""
        if len(correct_answer) > 0:
            for c in correct_answer[:-1]:
                new_answer_text += c + ","
            new_answer_text += correct_answer[-1]
            correct_answer = new_answer_text
        
        choice = "\n".join(current_choices)
        choice = choice.replace("a) ", "a. ")
        choice = choice.replace("b) ", "b. ")
        choice = choice.replace("c) ", "c. ")
        choice = choice.replace("d) ", "d. ")
        choice = choice.replace("e) ", "e. ")
        choice = choice.replace("f) ", "f. ")
        
        questions.append(question_text)
        choices.append(choice)
        answers.append(correct_answer)

    return questions, choices, answers

def getCCNAQuestions(filename="questions_ccna.html"):
    # Load your HTML content
    with open(filename) as f:
        html_content = f.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize lists to store extracted data
    questions = []
    choices = []
    answers = []

    # Find all questions in the HTML
    question_blocks = soup.find_all('div', class_='card exam-question-card')

    for block in question_blocks:
        if block.find('img'):
            continue  # Skip this question if an image is found

        # Extract the question text
        question_text = block.find('p', class_='card-text').get_text(strip=True, separator=" ").replace("\n", " ")

        if "drag" in question_text or "DRAG" in question_text or "refer" in question_text or "Refer" in question_text or "exhibit" in question_text:
            continue
        # Extract the choices
        choice_list = block.find('ul').find_all('li', class_='multi-choice-item')
        current_choices = []
        for choice in choice_list:
            choice_text = choice.get_text(strip=True, separator=" ").replace("\n", " ")
            choice_text = choice_text.replace("A. ", "a. ")
            choice_text = choice_text.replace("B. ", "b. ")
            choice_text = choice_text.replace("C. ", "c. ")
            choice_text = choice_text.replace("D. ", "d. ")
            choice_text = choice_text.replace("E. ", "e. ")
            choice_text = choice_text.replace("F. ", "f. ")
            current_choices.append(choice_text)
        
        current_choices = "\n".join(current_choices)
        # Extract the answer
        answer_text = block.find('span', class_='correct-answer').get_text(strip=True).lower()
        if "img" in answer_text:
            continue
        new_answer_text = ""
        if len(answer_text) > 0:
            for c in answer_text[:-1]:
                new_answer_text += c + ","
            new_answer_text += answer_text[-1]
            answer_text = new_answer_text
        questions.append(question_text)
        choices.append(current_choices)
        answers.append(answer_text)

    return questions, choices, answers

def valid_ip(address):
    if "." in address and (len(address.split(".")) == 4):
        if address.split(".")[0].isdigit():
            return True
    return False

def is_ip_address(text):
    for word in text.split(" "):
        if valid_ip(word):
            return True
    return False

def generatejsonl():
    datafiles = []
    n = 0
    # validationfiles = []
    cisco_prompt = "As a virtual assistant specializing in computer networking, your task is to analyze and respond to multiple-choice questions from a course related to Cisco CCNA examinations. For each question, you are to identify the correct option(s) from the given choices. Your response should only include the selected option(s) using their corresponding letter(s) in lowercase (e.g., a, b, c, d) or combination thereof if multiple selections are correct."
    cisco_questions, cisco_choices, cisco_answers = getCCNAQuestions("questions_ccna.html")
    print(len(cisco_questions))
    for i, question in enumerate(cisco_questions):
        datapoint = {}
        messages = []
        if not is_ip_address(question) and not is_ip_address(cisco_choices[i]):
            continue
        messages.append({"role": "system", "content": cisco_prompt})
        messages.append({"role": "user", "content": question+"\n"+cisco_choices[i]})
        messages.append({"role": "assistant", "content": cisco_answers[i]})
        datapoint["messages"] = messages
        datafiles.append(datapoint)
        n += 1
    #     if (i == 50):
    #         break
    # for i, question in enumerate(cisco_questions[51:]):
    #     datapoint = {}
    #     messages = []
    #     messages.append({"role": "system", "content": cisco_prompt})
    #     messages.append({"role": "user", "content": question+"\n"+cisco_choices[i]})
    #     messages.append({"role": "assistant", "content": cisco_answers[i]})
    #     datapoint["messages"] = messages
    #     validationfiles.append(datapoint)
    #     if (i == 60):
    #         break

    general_prompt = "As a virtual assistant specializing in computer networking, your task is to analyze and respond to multiple-choice questions from a course related to a computer networking course.. For each question, you are to identify the correct option(s) from the given choices. Your response should only include the selected option(s) using their corresponding letter(s) in lowercase (e.g., a, b, c, d) or combination thereof if multiple selections are correct."
    general_questions, general_choices, general_answers = getGeneralQuestions("questions_sanfoundry.html")
    print(len(general_questions))

    for i, question in enumerate(general_questions):
        datapoint = {}
        messages = []
        if not is_ip_address(question) and not is_ip_address(general_choices[i]):
            continue
        messages.append({"role": "system", "content": general_prompt})
        messages.append({"role": "user", "content": question+"\n"+general_choices[i]})
        messages.append({"role": "assistant", "content": general_answers[i]})
        datapoint["messages"] = messages
        datafiles.append(datapoint)
        n += 1
    #     if (i == 50):
    #         break

    # for i, question in enumerate(general_questions[51:]):
    #     datapoint = {}
    #     messages = []
    #     messages.append({"role": "system", "content": general_prompt})
    #     messages.append({"role": "user", "content": question+"\n"+general_choices[i]})
    #     messages.append({"role": "assistant", "content": general_answers[i]})
    #     datapoint["messages"] = messages
    #     validationfiles.append(datapoint)
    #     if (i == 60):
    #         break

    with open('data_ip.jsonl', 'w', encoding='utf-8') as f:
        for file in datafiles:
            json.dump(file, f, ensure_ascii=False)
            f.write("\n")

    print("Number of questions:", n)

    # with open('data_small_validation.jsonl', 'w', encoding='utf-8') as f:
    #     for file in validationfiles:
    #         json.dump(file, f, ensure_ascii=False)
    #         f.write("\n")

generatejsonl()
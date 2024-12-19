# LLM-Network-Eval

This repository contains all the necessary code and instructions to reproduce the results presented in our paper. The project involves running large language models (LLMs) to evaluate their performance on various questions related to computer networking, generating data for fine-tuning, and analyzing the results.

## Prerequisites

Before running the code, ensure you have Python 3.8+ installed. This repository has been tested with Python 3.9.6. We recommend using a virtual environment to manage dependencies.

### Setting Up the Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python -m venv llm_env
   ```

2. **Activate the virtual environment:**
   ```bash
   source llm_env/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install pandas scikit-learn openai anthropic transformers torch accelerate beautifulsoup4 matplotlib tabulate
   ```

## Reproducing Results

To reproduce all results from the paper, execute the `LLM_Project.ipynb` notebook. This notebook contains the code for data preparation, model evaluation, and result analysis. It uses the results stored in the Results folder.

1. **Open the notebook:**
   ```bash
   jupyter notebook LLM_Project.ipynb
   ```

2. **Run all cells:**
   Ensure that you run all cells in sequence to reproduce the results.

## Generate answers

The `generate_llm_answers.py` script is used to generate results using OpenAI and Claude LLMs. You need to provide your API keys for both services and specify other parameters using command-line arguments. The output files will be saved in a folder named after the model within the main directory.

### Command-Line Arguments

- `--folder`: Path to the folder that contains questions (required).
- `--files`: Files to process, separated by commas or `'all'` (required).
- `--model`: Model to use (e.g., `claude-3-opus-20240229`, `gpt-4-1106-preview`, `gpt-3.5-turbo-0125`). Default is `'gpt-3.5-turbo-0125'`.
- `--temp`: Temperature setting. Default is `0.5`.
- `--api`: API key for Anthropic or OpenAI (required).
- `--mode`: Operation mode (`default`, `finetune`, or `one_shot`). Default is `'default'`.

### Example Usage

1. **Set your API keys:**

   - OpenAI API Key: Obtain it from the [OpenAI API page](https://platform.openai.com/account/api-keys).
   - Claude API Key: Obtain it from the [Anthropic API page](https://console.anthropic.com/).

2. **Run the script with the desired parameters:**
   ```bash
   python generate_llm_answers.py --folder Questions/Original --files all --model gpt-4-1106-preview --temp 0.5 --api YOUR_API_KEY
   ```

   Replace `YOUR_API_KEY` with your actual API key, and adjust other parameters as needed. The script will generate a csv file for each text file of questions given.

## Running Open-Source LLMs

To evaluate open-source LLMs, you can use the provided `run_open_source_llm.py` script. This script includes an option to pass your Hugging Face (HF) API token for models that require authentication.

### Command-Line Arguments
- `--folder`: Path to the folder containing the CSV files that contain questions. Use Results/GPT3.5 to make this script work for this project.
- `--model_name`: The name of the open-source model to run (e.g., `Meta-Llama-3.1-70B-Instruct`, `gemma-2-9b-it`).
- `--HF_TOKEN`: Your Hugging Face API token (required for accessing certain models).

### Example Usage

1. **Obtain your Hugging Face API token:**

   - Get your token from the [Hugging Face account settings](https://huggingface.co/settings/tokens).

2. **Run the script with the required parameters:**
   ```bash
   python run_open_source_llm.py --folder Results/GPT3.5 --model_name Meta-Llama-3.1-70B-Instruct --HF_TOKEN YOUR_HF_TOKEN
   ```

   Replace `YOUR_HF_TOKEN` with your actual Hugging Face API token. Note that the script may stop to ask answers for which it was not automatically able to parse the choices. The results will be saved in the folder given as command line input.

## Generating Data for Fine-Tuning

To generate data for fine-tuning OpenAI models using networking questions, use the Finetuning folder and run:

   ```bash
   python generate_finetuning_data.py
   ```
The script will generate a `jsonl` file that can be used to fine-tune OpenAI models

## Acknowledgments
We would like to thank the students who contributed their time and effort to help with the labeling process: Taimoor Tariq, Saif ur Rehman, Talha Waheed, Gabriella Xue, Nafis Chaudhary, Aj Grama, Richard Wang, John Wei, Jonathan Ng, Tanay Pareek, Jia Qing Tan, Sahithya Ranjith, Muawiz Feroze Khan, Saad Alam

## Credits
The networking questions are obtained from Cisco CCNA 200-301 Practice Tests by [examsdigest](https://examsdigest.com/courses/cisco-ccna-200-301/) and the quiz questions from multiple courses on Coursera: [Network Security](https://www.coursera.org/learn/network-security) from Cisco’s Cybersecurity Operations Fundamentals Specialization, [Software Defined Networking](https://www.coursera.org/learn/sdn/) from University of Chicago, [TCP/IP and Advanced Topics](https://coursera.org/learn/tcp-ip-advanced) from University of Colorado, [The Bits and Bytes of Computer Networking](https://www.coursera.org/learn/computer-networking) from Google’s IT Support Professional Certificate, and [Computer Networking ](https://www.coursera.org/learn/illinois-tech-computer-networking) from Illinois Tech. For fine-tuning, we used some more practice questions for [Cisco CCNA 200-301](https://www.examtopics.com/exams/cisco/200-301/view/1/) and [computer networking questions](https://www.sanfoundry.com/computer-networks-mcqs-basics/) from an online repository.

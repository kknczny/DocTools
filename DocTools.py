import os
import PyPDF2
import re
import openai
from dotenv import load_dotenv

load_dotenv(verbose=True)

def list_files_in_path(path = None):
    if path is None:
        path = os.getcwd()

    files_extensions = ['pdf']
    files_list = []

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and \
        file.split(".")[1] in files_extensions:
            files_list.append(file)
    return files_list

def summarize_doc():
    pdf_summary_text = ""
    pdf_file_path = "/Users/kuba/Downloads/Wprowadzenie-do-chmury.pdf"
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text().lower()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": f"Summarize this: {page_text}"},
                ],
            )
        
    page_summary = response["choices"][0]["message"]["content"]
    pdf_summary_text+=page_summary + "\n"
    print(pdf_summary_text)

    pdf_file.close()

if __name__ == "__main__":
    print(list_files_in_path("/Users/kuba/Downloads"))
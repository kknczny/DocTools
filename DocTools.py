import os
import PyPDF2
import re
import openai
from dotenv import load_dotenv

load_dotenv(verbose=True)

class DocTools():
    def __init__(self, path=None):
        if path is None:
            path = os.getcwd()
        self.path = path
        self.files_extensions = ['pdf']

    def list_files(self):
        files_list = {}
        assignment_no = 1
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)) and \
            file.split(".")[1] in self.files_extensions:
                files_list[assignment_no] = file
            assignment_no =+ 1
        return files_list

    def summarize_doc():
        pdf_summary_text = ""
        # pdf_file_path = "/Users/kuba/Downloads/Wprowadzenie-do-chmury.pdf"
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
        pdf_file.close()
        return 

    def list_files_with_summary():
        pass

    def run(self):

        new_path = input(f"Welcome to DocTools. The currently set path is {self.path}. If needed, please input another path or 'y' to proceed: ")
        if new_path.lower() != 'y':
            self.path = new_path

        try:
            if self.path.split(".")[1] in self.files_extensions:
                files_list = {1: self.path}
                print(files_list)
        except KeyError:
            files_list = self.list_files()
            print(files_list)

        self.list_files()
        # path can be provided either as argument with execution of python file, or that will be the first input after running the file

        # if provided path ends with one of the extensions, this is a single file, hence we are not listing the contents.
        # if no extension, then we check whether its a file without extension included, if so we are not listing the dir contents
        # else we are listing with assignment numbers

        # now we can refer to the files in further functions by their names (with or without extension), full path, or assginment number

        # then input call whether we want to 1) summarize specific file 2) list all files with summary 3) delete specific file(s)


if __name__ == "__main__":
    runner = DocTools("/Users/kuba/Downloads/")
    print(runner.run())
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
        print("Welcome to DocTools")
        self.select_file()
        

    def list_files(self):
        files_list = {}
        assignment_no = 1
        try:
            for file in os.listdir(self.path):
                if os.path.isfile(os.path.join(self.path, file)) and \
                file.split(".")[1] in self.files_extensions:
                    files_list[assignment_no] = file
                assignment_no =+ 1
        except IndexError:
            pass
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

    def select_file(self):

        while True:
            new_path = input(f"The currently set path is {self.path}. If needed, please input another path or 'y' to proceed: ")
            if new_path.lower() == 'y':
                break
            elif new_path.lower() != 'y' and os.path.exists(new_path):
                self.path = new_path
                break
            else:
                print("Invalid path provided.")
                continue
            
        try:
            if self.path.split(".")[1] in self.files_extensions:
                FileProvided = True
        except IndexError:
                FileProvided = False

        while True:
            if FileProvided:
                files_list = {1: self.path}
                selected_number = 1
                selected_file = files_list[selected_number]
                break
            else:
                try:
                    files_list = self.list_files()
                    print("Which file you want to select?")
                    print(files_list)
                    selected_number = int(input(f"Please type assignment number: "))
                    selected_file = files_list[selected_number]
                    break
                except ValueError:
                    print("Provided value is not an integer.")
                    continue
                except KeyError:
                    print("Provided assignment number out of range.")
                    continue
            
        self.selected_file = selected_file
        print("Selected file is:")
        print(self.selected_file)
        

    def select_action():
        print(f"Please select what action on \"{self.selected_file}\" should be performed (type the corresponding assginment letter/symbol):")
        print("""
        S - Summarize the document using OpenAI
        E - Extract relevant tables and return them as DataFrames (feature not implemented yet)
        D - Delete the File
        . - Return to beginning
        """)
        input("Action to be performed: ")
        # path can be provided either as argument with execution of python file, or that will be the first input after running the file

        # if provided path ends with one of the extensions, this is a single file, hence we are not listing the contents.
        # if no extension, then we check whether its a file without extension included, if so we are not listing the dir contents
        # else we are listing with assignment numbers

        # now we can refer to the files in further functions by their names (with or without extension), full path, or assginment number

        # then input call whether we want to 1) summarize specific file 2) list all files with summary 3) delete specific file(s)


if __name__ == "__main__":
    runner = DocTools("/Users/kuba/Downloads/")

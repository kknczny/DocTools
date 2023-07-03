import os
import PyPDF2
import sys
import openai
from dotenv import load_dotenv

load_dotenv(verbose=True)

class DocTools():
    def __init__(self, path=None):
        if path is None:
            path = os.getcwd()
        self.path = path
        self.files_extensions = ['pdf']
        print("-"*23)
        print("--Welcome to DocTools--")
        print("-"*23)
        print(f"Currently supported document types are:")
        print(self.files_extensions)
        self.select_file()

    def list_files(self):
        files_list = {}
        assignment_no = 1
        try:
            for file in os.listdir(self.path):
                if os.path.isfile(os.path.join(self.path, file)) and \
                file.split(".")[1] in self.files_extensions:
                    files_list[assignment_no] = file
                    assignment_no += 1
                else:
                    continue
        except IndexError:
            pass
        return files_list

    def select_file(self):
        print('\n'+"-"*22)
        print("--Document Selection--")
        print("-"*22)
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
                self.file_path = selected_file
                break
            else:
                try:
                    files_list = self.list_files()
                    print("\nWhich file you want to select?")
                    print(files_list)
                    selected_number = int(input(f"Please type assignment number: "))
                    selected_file = files_list[selected_number]
                    self.file_path = self.path+selected_file
                    break
                except ValueError:
                    print("Provided value is not an integer.")
                    continue
                except KeyError:
                    print("Provided assignment number out of range.")
                    continue
            
        self.selected_file = selected_file

        print("\nSelected file is:")
        print(f"--> {self.selected_file} <--")

        self.exec_action()

    def summarize_doc(self):

        pdf_summary_text = ""
        
        pdf_file = open(self.file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)
        
        new_total_pages = int(input(f"Found {total_pages} pages in selected file. Type how many pages to summarize: "))
        while True:
            try:
                if new_total_pages > total_pages:
                    print(f"Provided number {new_total_pages} is greater than total number of pages - {total_pages}. Program will analyse all {total_pages} pages.")
                    break
                else:
                    total_pages = new_total_pages
                    break
            except ValueError:
                print("Provided input is not valid integer.")
                continue

        for page_num in range(total_pages):
            sys.stdout.write(f"\rAnalyzing page {page_num} out of {total_pages}...   \r")

            page_text = pdf_reader.pages[page_num].extract_text().lower()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": f"Summarize this: {page_text}"},
                    ],
                )
            
            sys.stdout.flush()
            
            page_summary = response["choices"][0]["message"]["content"]
            pdf_summary_text+=page_summary + "\n"

        pdf_file.close()
        return pdf_summary_text
    
    def extract_doc_tables(self):
        print("Feature not yet implemented.")
        pass

    def delete_doc(self):
        os.remove(self.file_path)
        print("File has been deleted")
        
    def exec_action(self):
        while True:
            print(f"Please select what action on \"{self.selected_file}\" should be performed (type the corresponding abbreviation):")
            print("""
            S - Summarize the document using OpenAI
            E - Extract relevant tables and return them as DataFrames (feature not implemented yet)
            D - Delete the document file
            R - Return to document selection
            Q - Quit
            """)
            selected_action = input("Action to be performed:")
            try:
                selected_action = selected_action.lower()
                if selected_action == 's':
                    print('\n')
                    print(self.summarize_doc())
                    continue
                if selected_action == 'e':
                    self.extract_doc_tables()
                    continue
                if selected_action == 'd':
                    self.delete_doc()
                    break
                if selected_action == 'r':
                    self.select_file()
                    break
                if selected_action == 'q':
                    break
                else:
                    print("Value unrecognized. Select corresponding abbreviation once again.")
                    continue
            except ValueError:
                print("Value unrecognized. Select corresponding abbreviation once again.")
                continue

        # path can be provided either as argument with execution of python file, or that will be the first input after running the file

        # if provided path ends with one of the extensions, this is a single file, hence we are not listing the contents.
        # if no extension, then we check whether its a file without extension included, if so we are not listing the dir contents
        # else we are listing with assignment numbers

        # now we can refer to the files in further functions by their names (with or without extension), full path, or assginment number

        # then input call whether we want to 1) summarize specific file 2) list all files with summary 3) delete specific file(s)


if __name__ == "__main__":
    runner = DocTools("/Users/kuba/Downloads/")

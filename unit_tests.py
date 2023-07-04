import unittest
from unittest.mock import patch
from io import StringIO
import os
from DocTools import DocTools

class TestDocTools(unittest.TestCase):
    def setUp(self):
        self.doc_tools = DocTools()
        self.doc_tools.files_extensions = ['pdf']

    def tearDown(self):
        del self.doc_tools

    def test_list_files(self):
        self.doc_tools.path = "test_files"
        expected_files_list = {1: 'file1.pdf', 2: 'file2.pdf'}
        files_list = self.doc_tools.list_files()
        self.assertDictEqual(files_list, expected_files_list)

    @patch('builtins.input', side_effect=['y'])
    def test_select_file_current_path(self, mock_input):
        expected_file_path = os.getcwd() + "/file1.pdf"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.doc_tools.select_file()
            self.assertEqual(self.doc_tools.file_path, expected_file_path)
            self.assertEqual(mock_stdout.getvalue().strip(), "Selected file is:\n--> file1.pdf <--")

    @patch('builtins.input', side_effect=['invalid_path', os.getcwd() + "/file1.pdf"])
    def test_select_file_valid_path(self, mock_input):
        expected_file_path = os.getcwd() + "/file1.pdf"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.doc_tools.select_file()
            self.assertEqual(self.doc_tools.file_path, expected_file_path)
            self.assertEqual(mock_stdout.getvalue().strip(), "Selected file is:\n--> file1.pdf <--")

    @patch('builtins.input', side_effect=['non_existing_path', os.getcwd() + "/file1.pdf"])
    def test_select_file_invalid_path(self, mock_input):
        expected_file_path = os.getcwd() + "/file1.pdf"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.doc_tools.select_file()
            self.assertEqual(self.doc_tools.file_path, expected_file_path)
            self.assertEqual(mock_stdout.getvalue().strip(), "Selected file is:\n--> file1.pdf <--")

    @patch('builtins.input', side_effect=['y'])
    def test_select_file_with_file_path(self, mock_input):
        self.doc_tools.path = "file.pdf"
        expected_file_path = "file.pdf"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.doc_tools.select_file()
            self.assertEqual(self.doc_tools.file_path, expected_file_path)
            self.assertEqual(mock_stdout.getvalue().strip(), "Selected file is:\n--> file.pdf <--")

    @patch('builtins.input', side_effect=[1])
    def test_summarize_doc(self, mock_input):
        expected_summary = "Page 1 summary\nPage 2 summary\nPage 3 summary"
        self.doc_tools.file_path = "test_files/file1.pdf"
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            with patch('PyPDF2.PdfReader') as mock_pdf_reader:
                mock_pdf_reader.return_value.__enter__.return_value.pages.__getitem__.return_value.extract_text.return_value = "Page 1 text\nPage 2 text\nPage 3 text"
                with patch('openai.ChatCompletion.create') as mock_openai:
                    mock_openai.return_value.__getitem__.return_value.__getitem__.return_value = "Page 1 summary"
                    result = self.doc_tools.summarize_doc()
                    self.assertEqual(result, expected_summary)
                    self.assertEqual(mock_stdout.getvalue().strip(), "Page 1 summary\nPage 2 summary\nPage 3 summary")

    def test_extract_doc_tables(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.doc_tools.extract_doc_tables()
            self.assertEqual(mock_stdout.getvalue().strip(), "Feature not yet implemented.")

    @patch('builtins.input', side_effect=['y'])
    def test_delete_doc(self, mock_input):
        self.doc_tools.file_path = "test_files/file1.pdf"
        with patch('os.remove') as mock_remove:
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                self.doc_tools.delete_doc()
                mock_remove.assert_called_once_with(self.doc_tools.file_path)
                self.assertEqual(mock_stdout.getvalue().strip(), "File has been deleted")

if __name__ == '__main__':
    unittest.main()

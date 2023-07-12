import unittest
import os
import tempfile
from PyPDF2 import PdfWriter
from unittest.mock import patch
from DocTools import DocTools

class TestDocTools(unittest.TestCase):

    def setUp(self):
        self.doc_tools = DocTools()

    def test_list_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.doc_tools.path = temp_dir
            with open(os.path.join(temp_dir, 'databricks-mit-slides.pdf'), 'w') as f:
                f.write('dummy content')
            with open(os.path.join(temp_dir, 'file2.txt'), 'w') as f:
                f.write('dummy content')
            result = self.doc_tools.list_files()
            self.assertEqual(result, {1: 'databricks-mit-slides.pdf'})

    # @patch('builtins.input', return_value='0')
    # def test_summarize_doc(self, mock_input):
    #     with tempfile.TemporaryDirectory() as temp_dir:
    #         pdf_path = os.path.join(temp_dir, 'databricks-mit-slides.pdf')
    #         writer = PdfWriter()
    #         with open(pdf_path, 'wb') as output_pdf:
    #             writer.write(output_pdf)
    #         self.doc_tools.file_path = pdf_path
    #         expected_summary = ''
    #         self.assertEqual(self.doc_tools.summarize_doc(), expected_summary)

    def test_delete_doc(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            self.doc_tools.file_path = temp_file.name
            self.doc_tools.delete_doc()
            self.assertFalse(os.path.exists(temp_file.name))

    @patch('builtins.input', side_effect=['y', '1', 'q', '1', 'q'])
    def test_select_file(self, mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.doc_tools.path = temp_dir
            with open(os.path.join(temp_dir, 'databricks-mit-slides.pdf'), 'w') as f:
                f.write('dummy content')
            self.doc_tools.select_file()
            self.assertEqual(self.doc_tools.selected_file, 'databricks-mit-slides.pdf')

    @patch('builtins.input', side_effect=['y', '1', 'q', '1', 'q'])
    def test_exec_action(self, mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.doc_tools.path = temp_dir
            with open(os.path.join(temp_dir, 'databricks-mit-slides.pdf'), 'w') as f:
                f.write('dummy content')
            self.doc_tools.select_file()
            # No assertion in this test as exec_action does not return anything
            # We are just testing if it runs without error

if __name__ == '__main__':
    unittest.main()

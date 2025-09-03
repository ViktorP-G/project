import unittest
from unittest.mock import patch
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import create_parser, run_copy


class TestCopyCommand(unittest.TestCase):

    @patch('sys.stdout.write')
    @patch('sys.exit')
    @patch('shutil.copy2')
    def test_run_copy_success(self, mock_copy2, mock_exit, mock_stdout):
        parser = create_parser()
        args = parser.parse_args(['copy', 'document.txt', '/tmp'])

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.exists', return_value=False):
            run_copy(args)

        mock_exit.assert_not_called()
        mock_copy2.assert_called_once()
        mock_stdout.assert_called()
        self.assertIn("Файл скопирован успешно", mock_stdout.call_args[0][0])

    @patch('sys.stdout.write')
    @patch('sys.exit')
    @patch('shutil.copy2')
    def test_run_copy_with_overwrite(self, mock_copy2, mock_exit, mock_stdout):
        parser = create_parser()
        args = parser.parse_args(['copy', 'data.csv', '/backup', '--overwrite'])

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.exists', return_value=False):
            run_copy(args)

        mock_exit.assert_not_called()
        mock_copy2.assert_called_once()
        mock_stdout.assert_called()
        self.assertIn("Файл скопирован успешно", mock_stdout.call_args[0][0])

    def test_parser_has_correct_args(self):
        parser = create_parser()
        args = parser.parse_args(['copy', 'input.txt', 'output/'])

        self.assertEqual(args.command, 'copy')
        self.assertEqual(args.file, 'input.txt')
        self.assertEqual(args.folder, 'output/')
        self.assertFalse(args.overwrite)

        args = parser.parse_args(['copy', 'file.log', 'logs/', '--overwrite'])
        self.assertTrue(args.overwrite)


if __name__ == '__main__':
    unittest.main()
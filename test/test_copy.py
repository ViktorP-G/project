import unittest
from unittest.mock import patch
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import create_parser, run_copy
from core.copy import copy_file


class TestCopyCommand(unittest.TestCase):

    @patch('builtins.print')
    def test_run_copy_success(self, mock_print):
        parser = create_parser()
        args = parser.parse_args(['copy', 'document.txt', '/tmp'])

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.exists', return_value=False), \
             patch('shutil.copy2') as mock_copy2:
            success, message = copy_file(args.file, args.folder, args.overwrite)
            self.assertTrue(success)
            self.assertIn("успешно скопирован", message)
            mock_copy2.assert_called_once()
            run_copy(args)
            mock_print.assert_called_once_with(message)

    @patch('builtins.print')
    def test_run_copy_with_overwrite(self, mock_print):
        parser = create_parser()
        args = parser.parse_args(['copy', 'data.csv', '/backup', '--overwrite'])

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.exists', return_value=True), \
             patch('shutil.copy2') as mock_copy2:
            success, message = copy_file(args.file, args.folder, args.overwrite)
            self.assertTrue(success)
            mock_copy2.assert_called_once()
            run_copy(args)
            mock_print.assert_called_once_with(message)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_run_copy_file_not_found(self, mock_exit, mock_print):
        parser = create_parser()
        args = parser.parse_args(['copy', 'missing.txt', '/tmp'])

        with patch('os.path.isfile', return_value=False):
            success, message = copy_file(args.file, args.folder, False)
            self.assertFalse(success)
            self.assertIn("не найден", message)
            run_copy(args)
            mock_print.assert_called_once_with(message, file=sys.stderr)
            mock_exit.assert_called_once_with(1)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_run_copy_folder_not_found(self, mock_exit, mock_print):
        parser = create_parser()
        args = parser.parse_args(['copy', 'document.txt', '/nonexistent'])

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=False):
            success, message = copy_file(args.file, args.folder, False)
            self.assertFalse(success)
            self.assertIn("не существует", message)
            run_copy(args)
            mock_print.assert_called_once_with(message, file=sys.stderr)
            mock_exit.assert_called_once_with(1)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_run_copy_file_exists_no_overwrite(self, mock_exit, mock_print):
        parser = create_parser()
        args = parser.parse_args(['copy', 'document.txt', '/tmp'])

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.path.exists', return_value=True):
            success, message = copy_file(args.file, args.folder, False)
            self.assertFalse(success)
            self.assertIn("уже существует", message)
            run_copy(args)
            mock_print.assert_called_once_with(message, file=sys.stderr)
            mock_exit.assert_called_once_with(1)

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
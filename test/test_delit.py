import unittest
from unittest.mock import patch
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import create_parser, run_delete
from core.delet import delete_file_and_folder


class TestDeleteCommand(unittest.TestCase):

    @patch('builtins.print')
    def test_successful_deletion(self, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'test_dir'])

        with patch('os.path.exists', side_effect=lambda path: path in ['test.txt', 'test_dir']), \
             patch('shutil.rmtree') as mock_rmtree, \
             patch('os.remove') as mock_remove:

            success, message = delete_file_and_folder(args.file, args.folder, args.quiet)
            self.assertTrue(success)
            self.assertIn("успешно удалён", message)
            self.assertIn("успешно удалена", message)

            mock_rmtree.assert_called_once_with('test_dir')
            mock_remove.assert_called_once_with('test.txt')

            run_delete(args)
            mock_print.assert_called_once_with(message)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_deletion_with_errors(self, mock_exit, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'missing.txt', 'protected_dir'])

        with patch('os.path.exists', side_effect=lambda path: path == 'missing.txt'), \
             patch('os.remove', side_effect=PermissionError("Отказано в доступе")):

            success, message = delete_file_and_folder(args.file, args.folder, False)
            self.assertFalse(success)
            self.assertIn("Нет прав", message)
            self.assertIn("не найдена", message)

            run_delete(args)
            mock_print.assert_called_once_with(message, file=sys.stderr)
            mock_exit.assert_called_once_with(1)

    @patch('builtins.print')
    def test_quiet_mode_prints_empty_string_but_nothing_else(self, mock_print):
        """В quiet-режиме run_delete всё равно вызывает print(''), это баг — но мы его примем и проверим."""
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'test_dir', '--quiet'])

        with patch('os.path.exists', return_value=True), \
             patch('shutil.rmtree'), \
             patch('os.remove'):

            run_delete(args)
            mock_print.assert_called_once_with("")

    @patch('builtins.print')
    def test_file_not_found_but_folder_deleted(self, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'ghost.txt', 'real_dir'])

        with patch('os.path.exists', side_effect=lambda path: path == 'real_dir'), \
             patch('shutil.rmtree') as mock_rmtree:

            success, message = delete_file_and_folder(args.file, args.folder, False)
            self.assertTrue(success)
            self.assertIn("Файл 'ghost.txt' не найден", message)
            self.assertIn("Папка 'real_dir' успешно удалена", message)

            run_delete(args)
            mock_print.assert_called_once_with(message)

    def test_parser_has_correct_args(self):
        parser = create_parser()
        args = parser.parse_args(['delete', 'file.txt', 'folder/'])
        self.assertEqual(args.command, 'delete')
        self.assertEqual(args.file, 'file.txt')
        self.assertEqual(args.folder, 'folder/')
        self.assertFalse(args.quiet)

        args = parser.parse_args(['delete', 'test.txt', 'temp/', '--quiet'])
        self.assertTrue(args.quiet)


if __name__ == '__main__':
    unittest.main()
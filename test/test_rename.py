import unittest
from unittest.mock import patch
import sys
import os
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import create_parser, run_rename
from core.rename import rename_file_with_date


class TestRenameCommand(unittest.TestCase):

    @patch('builtins.print')
    def test_rename_success(self, mock_print):
        parser = create_parser()
        args = parser.parse_args(['rename', 'test.txt', '/some/folder'])

        mock_stat_result = type('MockStat', (), {'st_ctime': time.mktime(time.strptime("2024-06-15", "%Y-%m-%d"))})

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.stat', return_value=mock_stat_result), \
             patch('os.rename') as mock_rename, \
             patch('os.path.exists', return_value=False), \
             patch('os.listdir', return_value=[]):

            success, message = rename_file_with_date(args.file, args.folder, args.recursive)
            self.assertTrue(success)
            self.assertIn("test_2024-06-15.txt", message)
            mock_rename.assert_called_once()

            run_rename(args)
            mock_print.assert_called_once_with(message)

    @patch('builtins.print')
    def test_rename_recursive(self, mock_print):
        parser = create_parser()
        args = parser.parse_args(['rename', 'test.txt', '/some/folder', '--recursive'])

        mock_stat_result = type('MockStat', (), {'st_ctime': time.mktime(time.strptime("2024-06-15", "%Y-%m-%d"))})

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.stat', return_value=mock_stat_result), \
             patch('os.rename') as mock_rename, \
             patch('os.path.exists', return_value=False), \
             patch('os.walk', return_value=[
                 ('/some/folder', [], ['file1.txt', 'file2.log']),
                 ('/some/folder/sub', [], ['readme.md'])
             ]), \
             patch('os.listdir', side_effect=[
                 ['file1.txt', 'file2.log'],
                 ['readme.md']
             ]):

            success, message = rename_file_with_date(args.file, args.folder, args.recursive)
            self.assertTrue(success)
            self.assertIn("test_2024-06-15.txt", message)
            self.assertIn("file1_2024-06-15.txt", message)
            self.assertIn("readme_2024-06-15.md", message)
            self.assertEqual(mock_rename.call_count, 4)

            run_rename(args)
            mock_print.assert_called_once_with(message)

    @patch('builtins.print')
    @patch('sys.exit')
    def test_rename_os_error(self, mock_exit, mock_print):
        parser = create_parser()
        args = parser.parse_args(['rename', 'test.txt', '/some/folder'])

        mock_stat_result = type('MockStat', (), {'st_ctime': time.mktime(time.strptime("2024-06-15", "%Y-%m-%d"))})

        with patch('os.path.isfile', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('os.stat', return_value=mock_stat_result), \
             patch('os.rename', side_effect=OSError("Доступ запрещён")), \
             patch('os.path.exists', return_value=False), \
             patch('os.listdir', return_value=[]), \
             patch('core.rename.process_folder', return_value=[]):

            success, message = rename_file_with_date(args.file, args.folder, args.recursive)
            self.assertFalse(success)
            self.assertIn("Ошибка", message)

            run_rename(args)
            mock_print.assert_called_once_with(message, file=sys.stderr)
            mock_exit.assert_called_once_with(1)

    def test_parser_has_correct_args(self):
        parser = create_parser()
        args = parser.parse_args(['rename', 'file.txt', 'folder/'])
        self.assertEqual(args.command, 'rename')
        self.assertEqual(args.file, 'file.txt')
        self.assertEqual(args.folder, 'folder/')
        self.assertFalse(args.recursive)

        args = parser.parse_args(['rename', 'test.txt', 'photos/', '--recursive'])
        self.assertTrue(args.recursive)


if __name__ == '__main__':
    unittest.main()
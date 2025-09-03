import unittest
import os
import tempfile
import shutil
import time
import stat
from unittest.mock import patch, MagicMock
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import create_parser, run_rename


class TestRenameCommand(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)

        self.fixed_timestamp = int(time.mktime(time.strptime("2024-06-15", "%Y-%m-%d")))

    def create_mock_stat(self):
        mock_result = MagicMock()
        mock_result.st_mode = stat.S_IFREG | 0o644
        mock_result.st_ctime = self.fixed_timestamp
        mock_result.st_mtime = self.fixed_timestamp
        mock_result.st_atime = self.fixed_timestamp
        return mock_result

    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=False)
    @patch("os.stat")
    @patch("os.rename")
    @patch("builtins.print")
    def test_add_date_to_file_success(self, mock_print, mock_rename, mock_stat, mock_exists, mock_isfile):
        mock_stat.return_value = self.create_mock_stat()

        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        parser = create_parser()
        args = parser.parse_args(['rename', test_file, self.test_dir])

        with patch('os.path.isfile', side_effect=[True, True, False]), \
             patch('os.path.isdir', return_value=True), \
             patch('os.listdir', return_value=[]):
            run_rename(args)

        expected = os.path.join(self.test_dir, "test_2024-06-15.txt")
        mock_rename.assert_called_once_with(test_file, expected)

    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=True)
    @patch("os.stat")
    @patch("os.rename")
    @patch("builtins.print")
    def test_add_date_to_file_already_exists(self, mock_print, mock_rename, mock_stat, mock_exists, mock_isfile):
        mock_stat.return_value = self.create_mock_stat()

        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        parser = create_parser()
        args = parser.parse_args(['rename', test_file, self.test_dir])

        with patch('os.path.isfile', side_effect=[True, True, False]), \
             patch('os.path.isdir', return_value=True), \
             patch('os.listdir', return_value=[]):
            run_rename(args)

        mock_rename.assert_not_called()

    @patch("os.path.isfile", return_value=True)
    @patch("os.path.exists", return_value=False)
    @patch("os.stat")
    @patch("builtins.print")
    def test_add_date_to_file_handles_error(self, mock_print, mock_stat, mock_exists, mock_isfile):
        mock_stat.return_value = self.create_mock_stat()

        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        parser = create_parser()
        args = parser.parse_args(['rename', test_file, self.test_dir])

        with patch('os.path.isfile', side_effect=[True, True, False]), \
             patch('os.path.isdir', return_value=True), \
             patch('os.listdir', return_value=[]), \
             patch("os.rename", side_effect=OSError("No access")):
            run_rename(args)
            mock_print.assert_any_call(f"Ошибка при обработке {test_file}: No access")

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
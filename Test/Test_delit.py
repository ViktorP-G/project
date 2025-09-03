import unittest
from unittest.mock import patch
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import create_parser, run_delete


class TestDeleteCommand(unittest.TestCase):

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_successful_deletion(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'test_dir'])

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('test_dir')
        mock_os_remove.assert_called_once_with('test.txt')

        mock_print.assert_any_call("Папка test_dir успешно удалена.")
        mock_print.assert_any_call("Файл test.txt успешно удален.")

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_file_not_found(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'missing.txt', 'test_dir'])

        mock_os_remove.side_effect = FileNotFoundError()

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('test_dir')
        mock_os_remove.assert_called_once_with('missing.txt')

        mock_print.assert_any_call("Папка test_dir успешно удалена.")
        mock_print.assert_any_call("Файл missing.txt не найден.")

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_folder_not_found(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'missing_dir'])

        mock_shutil_rmtree.side_effect = FileNotFoundError()

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('missing_dir')
        mock_os_remove.assert_called_once_with('test.txt')

        mock_print.assert_any_call("Папка missing_dir не найдена.")
        mock_print.assert_any_call("Файл test.txt успешно удален.")

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_permission_error_folder(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'protected_dir'])

        mock_shutil_rmtree.side_effect = PermissionError()

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('protected_dir')
        mock_os_remove.assert_called_once_with('test.txt')

        mock_print.assert_any_call("Нет прав для удаления папки protected_dir.")
        mock_print.assert_any_call("Файл test.txt успешно удален.")

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_permission_error_file(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'protected.txt', 'test_dir'])

        mock_os_remove.side_effect = PermissionError()

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('test_dir')
        mock_os_remove.assert_called_once_with('protected.txt')

        mock_print.assert_any_call("Папка test_dir успешно удалена.")
        mock_print.assert_any_call("Нет прав для удаления файла protected.txt.")

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_quiet_mode_no_output(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'test_dir', '--quiet'])

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('test_dir')
        mock_os_remove.assert_called_once_with('test.txt')

        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_general_exception_folder(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'test.txt', 'broken_dir'])

        mock_shutil_rmtree.side_effect = Exception("Unknown error")

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('broken_dir')
        mock_os_remove.assert_called_once_with('test.txt')

        mock_print.assert_any_call("Произошла ошибка при удалении папки broken_dir: Unknown error.")
        mock_print.assert_any_call("Файл test.txt успешно удален.")

    @patch('builtins.print')
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_general_exception_file(self, mock_os_remove, mock_shutil_rmtree, mock_print):
        parser = create_parser()
        args = parser.parse_args(['delete', 'broken.txt', 'test_dir'])

        mock_os_remove.side_effect = Exception("Read-only filesystem")

        run_delete(args)

        mock_shutil_rmtree.assert_called_once_with('test_dir')
        mock_os_remove.assert_called_once_with('broken.txt')

        mock_print.assert_any_call("Папка test_dir успешно удалена.")
        mock_print.assert_any_call("Произошла ошибка при удалении файла broken.txt: Read-only filesystem.")

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